"""Library defining the interface to firewall."""
from datetime import timedelta
from typing import Any, Dict, Iterator, List, Optional

from rime_sdk.internal.constants import (
    MONITOR_TYPE_TO_SWAGGER,
    RISK_CATEGORY_TO_SWAGGER,
)
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.internal.swagger_utils import rest_to_timedelta
from rime_sdk.internal.throttle_queue import ThrottleQueue
from rime_sdk.internal.utils import convert_dict_to_html, make_link
from rime_sdk.job import ContinuousTestJob
from rime_sdk.monitor import Monitor
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import (
    ApiClient,
    FirewallFirewall,
    FirewallFirewallFirewallIdUuidBody,
    RimeStartContinuousTestRequest,
    RimeUpdateFirewallResponse,
    RimeUUID,
    RuntimeinfoResourceRequest,
    RuntimeinfoRunTimeInfo,
    TestrunTestRunIncrementalConfig,
    V1firewallfirewallFirewallIdUuidFirewall,
)
from rime_sdk.swagger.swagger_client.models import RimeJobMetadata

# 30 days in seconds
# 1 day = 86400 seconds
LIST_TEST_RUNS_INTERVAL_LENGTH_SECONDS = 30 * 86400


class Firewall:
    """Firewall object wrapper with helpful methods for working with RIME Firewall.

    Attributes:
        api_client: ApiClient
                The client used to query about the status of the job.
        firewall_id: str
            How to refer to the FW in the backend.
            Use this attribute to specify the Firewall for tasks in the backend.
    """

    # A throttler that limits the number of model tests to roughly 20 every 5 minutes.
    # This is a static variable for Client.
    _throttler = ThrottleQueue(desired_events_per_epoch=20, epoch_duration_sec=300)

    def __init__(self, api_client: ApiClient, firewall_id: str) -> None:
        """Create a new Firewall wrapper object.

        Arguments:
            api_client: ApiClient
                The client used to query about the status of the job.
            firewall_id: str
                The identifier for the RIME job that this object monitors.
        """
        self._api_client = api_client
        self._firewall_id = firewall_id

    def __eq__(self, obj: Any) -> bool:
        """Check if this FWInstance is equivalent to 'obj'."""
        return isinstance(obj, Firewall) and self._firewall_id == obj._firewall_id

    def __repr__(self) -> str:
        """Return string representation of the object."""
        return f"Firewall({self._firewall_id})"

    def update_firewall(
        self, model_id: Optional[str] = None, ref_data_id: Optional[str] = None
    ) -> RimeUpdateFirewallResponse:
        """Update the firewall with the model and reference data.

        Arguments:
            model_id: Optional[str]
                The model to use for the firewall.
            ref_data_id: Optional[str]
                The reference data to use for the firewall.

        Returns:
            The response from the backend.

        Raises:
            ValueError
                If no fields to be updated were submitted
                If the request to the Firewall service failed.

        Example:
        .. code-block:: python
            response = fw.update_firewall(ref_data_id="New reference data ID")
        """
        api = swagger_client.FirewallServiceApi(self._api_client)
        field_mask_list = []
        if model_id is not None:
            field_mask_list.append("modelId")
        if ref_data_id is not None:
            field_mask_list.append("refDataId")
        if len(field_mask_list) == 0:
            raise ValueError(
                "User must provide at least one of model_id or ref_data_id."
            )
        req = FirewallFirewallFirewallIdUuidBody(
            firewall_id=RimeUUID(self._firewall_id),
            firewall=V1firewallfirewallFirewallIdUuidFirewall(
                model_id=RimeUUID(model_id) if model_id is not None else None,
                ref_data_id=ref_data_id,
            ),
            mask=",".join(field_mask_list),
        )
        with RESTErrorHandler():
            resp = api.firewall_service_update_firewall(
                firewall_firewall_id_uuid=self._firewall_id, body=req,
            )
        return resp

    def _repr_html_(self) -> str:
        """Return HTML representation of the object."""
        info = {
            "Firewall ID": self._firewall_id,
            "Link": make_link(
                "https://" + self.get_link(),
                link_text="Continuous Testing Overview Page",
            ),
        }
        return convert_dict_to_html(info)

    def get_link(self) -> str:
        """Return the link to the firewall."""
        api = swagger_client.FirewallServiceApi(self._api_client)
        with RESTErrorHandler():
            resp = api.firewall_service_get_url(firewall_id_uuid=self._firewall_id,)
        return resp.url.url

    def get_bin_size(self) -> timedelta:
        """Return the bin size of this Firewall."""
        firewall = self._get_firewall()
        return rest_to_timedelta(firewall.bin_size)

    def get_ref_data_id(self) -> str:
        """Return the ID of the firewall's current reference set."""
        firewall = self._get_firewall()
        return firewall.ref_data_id

    def get_model_id(self) -> str:
        """Return the ID of the firewall's current model."""
        firewall = self._get_firewall()
        return firewall.model_id

    @property
    def project_id(self) -> str:
        """Return the unique identifier of the parent project."""
        fw = self._get_firewall()
        return fw.project_id.uuid

    def delete_firewall(self) -> None:
        """Delete firewall."""
        api = swagger_client.FirewallServiceApi(self._api_client)
        with RESTErrorHandler():
            api.firewall_service_delete_firewall(firewall_id_uuid=self._firewall_id)

    def _get_firewall(self) -> FirewallFirewall:
        api = swagger_client.FirewallServiceApi(self._api_client)
        with RESTErrorHandler():
            res = api.firewall_service_get_firewall(firewall_id_uuid=self._firewall_id)
        return res.firewall

    def list_monitors(
        self,
        monitor_types: Optional[List[str]] = None,
        risk_category_types: Optional[List[str]] = None,
    ) -> Iterator[Monitor]:
        """List monitors for the given Firewall.

        Monitors are the interface for interacting with time series in the RI platform.
        The built-in Monitors track degradations in model performance metrics, attacks
        on your model in production, and so on.
        You can filter monitors with this method to narrow down on those you are
        interested in.

        Arguments:
            monitor_types: Optional[List[str]]
                Return the set of built-in monitors or user-created custom monitors.
                Accepted values: ["Default", "Custom"]
            risk_category_types: Optional[List[str]]
                Return monitors pertaining to certain categories of AI Risk.
                For instance, monitors that track model performance help you track
                down Operational Risk.
                Accepted values: [
                    "Operational", "Bias_and_Fairness", "Security", "Custom"
                ]

        Returns:
            A generator of Monitor objects.

        Raises:
            ValueError
                If you provide unrecognized filtering parameters.
        """
        swagger_monitor_types = []
        swagger_risk_types = []
        if monitor_types is not None:
            try:
                swagger_monitor_types = [
                    MONITOR_TYPE_TO_SWAGGER[m] for m in monitor_types
                ]
            except KeyError as e:
                raise ValueError(
                    f"{e.args[0]} is not a valid monitor type,"
                    + f" {list(MONITOR_TYPE_TO_SWAGGER.keys())}"
                    + " are the accepted monitor types."
                )
        if risk_category_types is not None:
            try:
                swagger_risk_types = [
                    RISK_CATEGORY_TO_SWAGGER[r] for r in risk_category_types
                ]
            except KeyError as e:
                raise ValueError(
                    f"{e.args[0]} is not a valid risk category type,"
                    + f" {list(RISK_CATEGORY_TO_SWAGGER.keys())}"
                    + " are the accepted risk category types."
                )
        project_id = self._get_firewall().project_id.uuid
        api = swagger_client.MonitorServiceApi(self._api_client)
        next_page_token = ""
        has_more = True
        while has_more:
            kwargs: Dict[str, Any] = {}
            if len(next_page_token) > 0:
                kwargs["page_token"] = next_page_token
            else:
                kwargs["first_page_req_included_monitor_types"] = swagger_monitor_types
                kwargs[
                    "first_page_req_included_risk_category_types"
                ] = swagger_risk_types
            with RESTErrorHandler():
                res = api.monitor_service_list_monitors(
                    firewall_id_uuid=self._firewall_id, **kwargs,
                )
            for monitor in res.monitors:
                yield Monitor(
                    self._api_client, monitor.id.uuid, self._firewall_id, project_id
                )
            next_page_token = res.next_page_token
            has_more = res.has_more

    def start_continuous_test(
        self,
        eval_data_id: str,
        override_existing_bins: bool = False,
        agent_id: Optional[str] = None,
        ram_request_megabytes: Optional[int] = None,
        cpu_request_millicores: Optional[int] = None,
        random_seed: Optional[int] = None,
        **exp_fields: Dict[str, object],
    ) -> ContinuousTestJob:
        """Start a RIME model firewall test on the backend's ModelTesting service.

        This allows you to run Firewall Test job on the RIME
        backend. This will run firewall on a batch of tabular data.

        Arguments:
            eval_data_id: str
                ID of the evaluation data.
            override_existing_bins: bool
                Whether to override existing bins.
            ram_request_megabytes: Optional[int]
                Megabytes of RAM requested for the stress test job. If none
                specified, will default to 4000MB. The limit is equal to the megabytes
                requested.
            cpu_request_millicores: Optional[int]
                Millicores of CPU requested for the stress test job. If none
                specified, will default to 1500mi. The limit is equal to millicores
                requested.
            agent_id: Optional[str]
                Identifier for the agent where the continuous test will be run.
                If not specified, the workspace's default agent is used.
            exp_fields: Dict[str, object]
                Fields for experimental features that should not be set in production.

        Returns:
            A ``Job`` providing information about the model continuous test job.

        Raises:
            ValueError
                If invalid arguments are provided.
                If the request to the ModelTest service failed.

        Example:

        .. code-block:: python
            firewall = project.get_firewall()
            eval_data_id = client.register_dataset("example dataset", data_config)
            job = firewall.run_firewall_incremental_data(
                eval_data_id=eval_data_id,
                ram_request_megabytes=8000,
                cpu_request_millicores=2000,
            )
        """
        if ram_request_megabytes is not None and ram_request_megabytes <= 0:
            raise ValueError(
                "The requested number of megabytes of RAM must be positive"
            )

        if cpu_request_millicores is not None and cpu_request_millicores <= 0:
            raise ValueError(
                "The requested number of millicores of CPU must be positive"
            )

        req = RimeStartContinuousTestRequest(
            firewall_id=RimeUUID(self._firewall_id),
            test_run_incremental_config=TestrunTestRunIncrementalConfig(
                eval_dataset_id=eval_data_id,
                run_time_info=RuntimeinfoRunTimeInfo(
                    agent_id=RimeUUID(agent_id) if agent_id else None,
                    resource_request=RuntimeinfoResourceRequest(
                        ram_request_megabytes=ram_request_megabytes,
                        cpu_request_millicores=cpu_request_millicores,
                    ),
                    random_seed=random_seed,
                ),
            ),
            override_existing_bins=override_existing_bins,
            experimental_fields=exp_fields if exp_fields else None,
        )
        with RESTErrorHandler():
            Firewall._throttler.throttle(  # pylint: disable=W0212
                throttling_msg="Your request is throttled to limit # of model tests."
            )
            api = swagger_client.ModelTestingApi(self._api_client)
            job: RimeJobMetadata = api.model_testing_start_continuous_test(body=req).job
        return ContinuousTestJob(self._api_client, job.job_id)
