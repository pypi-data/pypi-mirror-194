"""Library defining the interface to a project."""
from datetime import timedelta
from http import HTTPStatus
from typing import Dict, Iterator, List, NamedTuple, Optional

from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.json_format import MessageToDict

from rime_sdk.data_collector import DataCollector
from rime_sdk.firewall import Firewall
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.internal.swagger_utils import get_data_location_swagger, timedelta_to_rest
from rime_sdk.internal.utils import (
    assert_and_get_none_or_all_none,
    convert_dict_to_html,
    make_link,
)
from rime_sdk.registry import Registry
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import (
    ApiClient,
    CreateFirewallRequestScheduledCTParameters,
    RimeCreateFirewallRequest,
    RimeUUID,
)
from rime_sdk.swagger.swagger_client.models import (
    DigestConfigDigestFrequency,
    NotificationDigestConfig,
    NotificationJobActionConfig,
    NotificationMonitoringConfig,
    NotificationNotificationType,
    NotificationObjectType,
    NotificationWebhookConfig,
    ProjectProject,
    RimeCreateNotificationRequest,
    RimeLicenseLimit,
    RimeLimitStatusStatus,
    RimeListNotificationsResponse,
    SchemanotificationConfig,
)
from rime_sdk.swagger.swagger_client.rest import ApiException
from rime_sdk.test_run import TestRun

NOTIFICATION_TYPE_JOB_ACTION_STR: str = "Job_Action"
NOTIFICATION_TYPE_MONITORING_STR: str = "Monitoring"
NOTIFICATION_TYPE_DIGEST_STR: str = "Daily_Digest"
NOTIFICATION_TYPE_UNSPECIFIED_STR: str = "Unspecified"
NOTIFICATION_TYPES_STR_LIST: List[str] = [
    NOTIFICATION_TYPE_JOB_ACTION_STR,
    NOTIFICATION_TYPE_MONITORING_STR,
    NOTIFICATION_TYPE_DIGEST_STR,
]


class ProjectInfo(NamedTuple):
    """This object contains static information that describes a project."""

    project_id: str
    """How to refer to the project in the backend."""
    name: str
    """Name of the project."""
    description: str
    """Description of the project."""
    use_case: Optional[str] = None
    """Description of the use case of the project."""
    ethical_consideration: Optional[str] = None
    """Description of ethical consideration(s) for this project."""


class Project:
    """An interface to a RIME project.

    This object provides an interface for editing, updating, and deleting projects.

    Attributes:
        api_client: ApiClient
                The client used to query about the status of the job.
        project_id: str
            The identifier for the RIME project that this object monitors.
    """

    def __init__(self, api_client: ApiClient, project_id: str) -> None:
        """Contains information about a RIME Project.

        Args:
            api_client: ApiClient
                The client used to query about the status of the job.
            project_id: str
                The identifier for the RIME project that this object monitors.
        """
        self._api_client = api_client
        self._project_id = project_id
        self._registry = Registry(self._api_client)
        self._data_collector = DataCollector(self._api_client, self._project_id)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Project({self._project_id})"

    def _repr_html_(self) -> str:
        """Return HTML representation of the object."""
        info = {
            "Project ID": self._project_id,
            "Link": make_link("https://" + self.get_link(), link_text="Project Page"),
        }
        return convert_dict_to_html(info)

    @property
    def project_id(self) -> str:
        """Return the id of this project."""
        return self._project_id

    def _check_firewall_creation_limit(self) -> None:
        """Check if creating another firewall would be within license limits.

        Raises:
            ValueError if another firewall cannot be created as it would
            exceed license limits.
        """
        api = swagger_client.RIMEInfoApi(self._api_client)
        with RESTErrorHandler():
            rime_info_response = api.r_ime_info_get_rime_info()

        feature_flag_api = swagger_client.FeatureFlagApi(self._api_client)
        with RESTErrorHandler():
            feature_flag_response = feature_flag_api.feature_flag_get_limit_status(
                customer_name=rime_info_response.customer_name,
                limit=RimeLicenseLimit.FIREWALL,
            )

        limit_status = feature_flag_response.limit_status.limit_status
        limit_value = feature_flag_response.limit_status.limit_value
        if limit_status == RimeLimitStatusStatus.WARN:
            curr_value = int(feature_flag_response.limit_status.current_value)
            print(
                f"You are approaching the limit ({curr_value + 1}"
                f"/{limit_value}) of models monitored. Contact the"
                f" Robust Intelligence team to upgrade your license."
            )
        elif limit_status == RimeLimitStatusStatus.ERROR:
            # could be either within grace period or exceeded grace period
            # if the latter, let the create firewall call raise the
            # error
            print(
                "You have reached the limit of models monitored."
                " Contact the Robust Intelligence team to"
                " upgrade your license."
            )
        elif limit_status == RimeLimitStatusStatus.OK:
            pass
        else:
            raise ValueError("Unexpected status value.")

    def _get_project(self) -> ProjectProject:
        """Get the project info from the backend.

        Returns:
            A ``GetProjectResponse`` object.
        """
        api = swagger_client.ProjectServiceApi(self._api_client)
        with RESTErrorHandler():
            response = api.project_service_get_project(self._project_id)
            return response.project.project

    @property
    def info(self) -> ProjectInfo:
        """Return information about this project."""
        project = self._get_project()
        return ProjectInfo(
            self._project_id,
            project.name,
            project.description,
            project.use_case,
            project.ethical_consideration,
        )

    def get_link(self) -> str:
        """Get the web app URL to the project.

        This link directs to your organization's deployment of RIME.
        You can view more detailed information in the web app, including
        information on your test runs, comparisons of those results,
        and models that are monitored.

        Note: this is a string that should be copy-pasted into a browser.
        """
        # TODO(ketan): attach the right ticket to this
        return "beast.rime.dev"

    @property
    def name(self) -> str:
        """Return the name of this project."""
        return self.info.name

    @property
    def description(self) -> str:
        """Return the description of this project."""
        return self.info.description

    def list_test_runs(self) -> Iterator[TestRun]:
        """List the stress test runs associated with the project."""
        api = swagger_client.ResultsReaderApi(self._api_client)
        # Iterate through the pages of projects and break at the last page.
        page_token = ""
        while True:
            if page_token == "":
                res = api.results_reader_list_test_runs(project_id=self._project_id)
            else:
                res = api.results_reader_list_test_runs(page_token=page_token)
            if res.test_runs is not None:
                for test_run in res.test_runs:
                    yield TestRun(self._api_client, test_run.test_run_id)
            # Advance to the next page of test cases.
            page_token = res.next_page_token
            # we've reached the last page of test cases.
            if not res.has_more:
                break

    def create_firewall(
        self,
        model_id: str,
        ref_data_id: str,
        bin_size: timedelta,
        scheduled_ct_eval_data_location: Optional[Dict] = None,
        scheduled_ct_eval_prediction_location: Optional[Dict] = None,
        scheduled_ct_rolling_window_size: Optional[timedelta] = None,
    ) -> Firewall:
        """Create a Firewall in the current Project.

        Args:
            model_id: str
                The ID of the model in the registry that this Firewall is testing.
            ref_data_id: str
                The ID of the reference data in the registry that this Firewall compares
                against during testing.
            bin_size: timedelta
                The length of each time bin to test on as a `timedelta` object.
                Must have a minimum value of 1 hour.
            scheduled_ct_eval_data_location: Optional[Dict]
                The location of the data to be used for scheduled CT evaluation.
            scheduled_ct_eval_prediction_location: Optional[Dict]
                The location of the predictions to be used for scheduled CT evaluation.
            scheduled_ct_rolling_window_size: Optional[timedelta]
                The size of the rolling window to be used for scheduled CT evaluation.

        Returns:
            A ``Firewall`` object that can be used to monitor the model.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:
        .. code-block:: python
            from datetime import timedelta
            # Create FW based on registered model and data
            fw = project.create_firewall(model_id, ref_data_id, timedelta(days=2))
        """
        self._check_firewall_creation_limit()
        api = swagger_client.FirewallServiceApi(self._api_client)
        req = RimeCreateFirewallRequest(
            project_id=RimeUUID(uuid=self._project_id),
            model_id=RimeUUID(uuid=model_id),
            ref_data_id=ref_data_id,
            bin_size=timedelta_to_rest(bin_size),
        )
        if assert_and_get_none_or_all_none(
            scheduled_ct_eval_data_location,
            scheduled_ct_eval_prediction_location,
            scheduled_ct_rolling_window_size,
        ):
            if (
                scheduled_ct_eval_data_location is None
                or scheduled_ct_eval_prediction_location is None
                or scheduled_ct_rolling_window_size is None
            ):
                raise ValueError("Invalid code path.")
            req.scheduled_ct_parameters = CreateFirewallRequestScheduledCTParameters(
                eval_data_location=get_data_location_swagger(
                    scheduled_ct_eval_data_location
                ),
                eval_pred_location=get_data_location_swagger(
                    scheduled_ct_eval_prediction_location
                ),
                rolling_window=timedelta_to_rest(scheduled_ct_rolling_window_size),
            )
        with RESTErrorHandler():
            resp = api.firewall_service_create_firewall(body=req)
        return Firewall(self._api_client, resp.firewall_id.uuid)

    def _get_firewall_ids(self) -> List[RimeUUID]:
        api = swagger_client.ProjectServiceApi(self._api_client)
        with RESTErrorHandler():
            response = api.project_service_get_project(project_id_uuid=self._project_id)
            return response.project.project.firewall_ids

    def get_firewall(self) -> Firewall:
        """Get the active Firewall for a project if it exists.

        Query the backend for an active `Firewall` in this project which
        can be used to perform Firewall operations. If there is no active
        Firewall for the project, this call will error.

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the Firewall does not exist.

        Example:

        .. code-block:: python

            # Get FW if it exists.
            firewall = project.get_firewall()
        """
        firewall_ids = self._get_firewall_ids()
        if len(firewall_ids) == 0 or firewall_ids[0] is None:
            raise ValueError("No firewall found for given project.")
        return Firewall(self._api_client, firewall_ids[0].uuid)

    def has_firewall(self) -> bool:
        """Check whether a project has a firewall or not."""
        firewall_ids = self._get_firewall_ids()
        return len(firewall_ids) > 0 and firewall_ids[0] is not None

    def delete_firewall(self) -> None:
        """Delete firewall for this project if exists."""
        firewall = self.get_firewall()
        firewall.delete_firewall()

    def _list_notification_settings(self) -> RimeListNotificationsResponse:
        """Get list of notifications associated with the current project."""
        api = swagger_client.NotificationSettingApi(self._api_client)
        with RESTErrorHandler():
            response = api.notification_setting_list_notifications(
                list_notifications_query_object_ids=[self._project_id]
            )
            return response

    def _set_create_notification_setting_config_from_type(
        self, req: RimeCreateNotificationRequest, notif_type: str
    ) -> None:
        if notif_type == NotificationNotificationType.JOB_ACTION:
            req.config.job_action_config = NotificationJobActionConfig()
        elif notif_type == NotificationNotificationType.MONITORING:
            req.config.monitoring_config = NotificationMonitoringConfig()
        elif notif_type == NotificationNotificationType.DIGEST:
            req.config.digest_config = NotificationDigestConfig(
                frequency=DigestConfigDigestFrequency.DAILY
            )

    def _get_notification_type_from_str(self, notif_type: str) -> str:
        if notif_type == NOTIFICATION_TYPE_JOB_ACTION_STR:
            return NotificationNotificationType.JOB_ACTION
        elif notif_type == NOTIFICATION_TYPE_MONITORING_STR:
            return NotificationNotificationType.MONITORING
        elif notif_type == NOTIFICATION_TYPE_DIGEST_STR:
            return NotificationNotificationType.DIGEST
        else:
            raise ValueError(
                f"Notification type must be one of {NOTIFICATION_TYPES_STR_LIST}"
            )

    def _get_notification_type_str(self, notif_type: str) -> str:
        if notif_type == NotificationNotificationType.JOB_ACTION:
            return NOTIFICATION_TYPE_JOB_ACTION_STR
        elif notif_type == NotificationNotificationType.MONITORING:
            return NOTIFICATION_TYPE_MONITORING_STR
        elif notif_type == NotificationNotificationType.DIGEST:
            return NOTIFICATION_TYPE_DIGEST_STR
        else:
            # This function is called only to show the user notification types
            # as string as defined in NOTIFICATION_TYPES_STR_LIST. We will have
            # to update this if we add more notification types in the future.
            # Making it unspecified will not break any SDK/BE mismatch and still
            # show users the new notification type with unspecified tag.
            # This situation should not happen ideally
            return NOTIFICATION_TYPE_UNSPECIFIED_STR

    def get_notification_settings(self) -> Dict:
        """Get the list of notifications for the project.

        Queries the backend to get a list of notifications
        added to the project. The notifications are grouped by the type
        of the notification and each type contains a list of emails and webhooks
        which are added to the notification setting

        Returns:
            A Dictionary of notification type and corresponding
            emails and webhooks added for that notification type.

        Example:

        .. code-block:: python

            notification_settings = project.list_notification_settings()
        """
        notif_list = self._list_notification_settings()
        out: Dict = {}
        for notif in notif_list.notifications:
            notif_type_str = self._get_notification_type_str(notif.notification_type)
            out[notif_type_str] = {}
            out[notif_type_str]["emails"] = notif.emails
            out[notif_type_str]["webhooks"] = []
            for webhook in notif.webhooks:
                out[notif_type_str]["webhooks"].append(webhook.webhook)
        return out

    def _add_notif_entry(
        self,
        notif_type_str: str,
        email: Optional[str],
        webhook_config: Optional[NotificationWebhookConfig],
    ) -> None:
        """Add the email or webhook in the notification settings of notif_type.

        This function should be called with either one of an email or a webhook
        to be added in a single call. emails are checked first and we add a
        webhook only when email is set to None. The function first checks if
        a notification object exists for the give notification type and appends
        the email/webhook if found, else it creates a new notification object
        """
        api = swagger_client.NotificationSettingApi(self._api_client)
        if email is not None and webhook_config is not None:
            raise ValueError(
                "_add_notif_entry expects exactly one of email or "
                "webhook config to be set"
            )
        notif_setting_list = self._list_notification_settings()
        notif_type = self._get_notification_type_from_str(notif_type_str)
        mask = FieldMask()
        for notif_setting in notif_setting_list.notifications:
            if notif_setting.notification_type == notif_type:
                if email is not None:
                    for existing_email in notif_setting.emails:
                        if existing_email == email:
                            print(
                                f"Email: {email} already exists in notification "
                                f"settings for notification type: {notif_type_str}"
                            )
                            return
                    mask.paths.append("emails")
                    notif_setting.emails.append(email)
                elif webhook_config is not None:
                    for existing_webhook in notif_setting.webhooks:
                        if existing_webhook.webhook == webhook_config.webhook:
                            print(
                                f"Webhook: {webhook_config.webhook} "
                                "already exists in notification settings "
                                f"for notification type: {notif_type_str}"
                            )
                            return
                    mask.paths.append("webhooks")
                    notif_setting.webhooks.append(webhook_config)
                with RESTErrorHandler():
                    # Note: the FieldMask object is not a Swagger model so we must
                    # serialize it to a dictionary before invoking Swagger API methods.
                    serialized_mask = MessageToDict(mask)
                    body = {"notification": notif_setting, "mask": serialized_mask}
                    api.notification_setting_update_notification(
                        body=body, notification_id_uuid=notif_setting.id.uuid,
                    )
                    return
        # Notification setting does not exist for the notif_type.
        req = RimeCreateNotificationRequest(
            object_type=NotificationObjectType.PROJECT,
            object_id=self.project_id,
            config=SchemanotificationConfig(),
            emails=[],
            webhooks=[],
        )
        self._set_create_notification_setting_config_from_type(req, notif_type)
        notif_entry_str = ""
        if email is not None:
            req.emails.append(email)
            notif_entry_str = "Email " + email
        elif webhook_config is not None:
            req.webhooks.append(webhook_config)
            notif_entry_str = "Webhook " + webhook_config.webhook
        with RESTErrorHandler():
            api.notification_setting_create_notification(body=req)
            print(f"{notif_entry_str} added for notification type {notif_type_str}")
            return

    def _remove_notif_entry(
        self,
        notif_type_str: str,
        email: Optional[str],
        webhook_config: Optional[NotificationWebhookConfig],
    ) -> None:
        """Remove the email or webhook in the notification settings of notif_type.

        This function should be called with either one of an email or a webhook
        to be removed in a single call. emails are checked first and we remove
        webhook only when email is set to None. In case a delete operation
        leads to the notification object having no email or webhook, that
        notification object is deleted as well.
        """
        if email is not None and webhook_config is not None:
            raise ValueError(
                "_remove_notif_entry expects exactly one of email "
                "or webhook config to be set"
            )
        notif_setting_list = self._list_notification_settings()
        notif_type = self._get_notification_type_from_str(notif_type_str)
        mask = FieldMask()
        for notif_setting in notif_setting_list.notifications:
            if notif_setting.notification_type == notif_type:
                found = False
                if email is not None:
                    for existing_email in notif_setting.emails:
                        if existing_email == email:
                            notif_setting.emails.remove(existing_email)
                            mask.paths.append("emails")
                            found = True
                elif webhook_config is not None:
                    for existing_webhook in notif_setting.webhooks:
                        if existing_webhook.webhook == webhook_config.webhook:
                            notif_setting.webhooks.remove(existing_webhook)
                            mask.paths.append("webhooks")
                            found = True
                if found:
                    api = swagger_client.NotificationSettingApi(self._api_client)
                    with RESTErrorHandler():
                        if (
                            len(notif_setting.emails) == 0
                            and len(notif_setting.webhooks) == 0
                        ):
                            api.notification_setting_delete_notification(
                                id_uuid=notif_setting.id.uuid,
                            )
                        else:
                            # Note: the FieldMask object is not a Swagger model, so we
                            # must serialize it to a dictionary before invoking Swagger
                            # API methods.
                            serialized_mask = MessageToDict(mask)
                            body = {
                                "notification": notif_setting,
                                "mask": serialized_mask,
                            }
                            api.notification_setting_update_notification(
                                body=body, notification_id_uuid=notif_setting.id.uuid,
                            )
                        return
        notif_entry_str = ""
        if email is not None:
            notif_entry_str = "Email " + email
        elif webhook_config is not None:
            notif_entry_str = "Webhook " + webhook_config.webhook
        print(f"{notif_entry_str} not found for notification type {notif_type_str}")

    def add_email(self, email: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Add an email to the notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.add_email("<email>", "<notification type>")
        """
        if email == "":
            raise ValueError("Email must be a non empty string")
        return self._add_notif_entry(
            notif_type_str=notif_type_str, email=email, webhook_config=None
        )

    def remove_email(self, email: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Remove an email from notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.remove_email("<email>", "<notification type>")
        """
        if email == "":
            raise ValueError("Email must be a non empty string")
        return self._remove_notif_entry(
            notif_type_str=notif_type_str, email=email, webhook_config=None
        )

    def add_webhook(self, webhook: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Add a webhook to the notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.add_webhook("<webhook>", "<notification type>")
        """
        if webhook == "":
            raise ValueError("Webhook must be a non empty string")
        webhook_config = NotificationWebhookConfig(webhook=webhook)
        return self._add_notif_entry(
            notif_type_str=notif_type_str, email=None, webhook_config=webhook_config
        )

    def remove_webhook(self, webhook: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long,
        """Remove a webhook from notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.remove_webhook("<webhook>", "<notification type>")
        """
        if webhook == "":
            raise ValueError("Webhook must be a non empty string")
        webhook_config = NotificationWebhookConfig(webhook=webhook)
        return self._remove_notif_entry(
            notif_type_str=notif_type_str, email=None, webhook_config=webhook_config
        )

    def delete(self) -> None:
        """Delete project in RIME's backend."""
        api = swagger_client.ProjectServiceApi(self._api_client)
        try:
            api.project_service_delete_project(self._project_id)
        except ApiException as e:
            if e.status == HTTPStatus.NOT_FOUND:
                raise ValueError(
                    f"project with this id {self._project_id} does not exist"
                )
            raise ValueError(e.reason)

    def register_dataset(
        self,
        name: str,
        data_config: dict,
        integration_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """Register dataset for this project."""
        return self._registry.register_dataset(
            self.project_id,
            name,
            data_config,
            integration_id=integration_id,
            tags=tags,
            metadata=metadata,
        )

    def register_model(
        self,
        name: str,
        model_config: Optional[dict] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
        external_id: Optional[str] = None,
    ) -> str:
        """Register model for this project."""
        return self._registry.register_model(
            self.project_id,
            name,
            model_config=model_config,
            tags=tags,
            metadata=metadata,
            external_id=external_id,
        )

    def register_predictions(
        self,
        dataset_id: str,
        model_id: str,
        pred_config: dict,
        integration_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """Register predictions for this project."""
        self._registry.register_predictions(
            self.project_id,
            dataset_id,
            model_id,
            pred_config,
            integration_id=integration_id,
            tags=tags,
            metadata=metadata,
        )

    def list_datasets(self) -> Iterator[Dict]:
        """Return a list of datasets for this project, each as a dictionary."""
        return self._registry.list_datasets(self.project_id)

    def list_models(self) -> Iterator[Dict]:
        """Return a list of models for this project, each as a dictionary."""
        return self._registry.list_models(self.project_id)

    def get_data_collector(self) -> DataCollector:
        """Get Data Collector, create if None."""
        if self._data_collector is None:
            self._data_collector = DataCollector(self._api_client, self._firewall_id)
        return self._data_collector
