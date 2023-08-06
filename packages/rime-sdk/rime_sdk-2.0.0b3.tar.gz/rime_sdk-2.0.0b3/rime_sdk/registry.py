"""Library defining the interface to the Registry."""
import json
import logging
from typing import Dict, Iterator, List, Optional, cast

from rime_sdk.internal.config_parser import (
    convert_model_info_to_swagger,
    convert_single_data_info_to_swagger,
    convert_single_pred_info_to_swagger,
)
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import ApiClient
from rime_sdk.swagger.swagger_client.models import (
    DatasetProjectIdUuidBody,
    ModelIdUuidDatasetIdBody,
    ModelProjectIdUuidBody,
    RimeListDatasetsResponse,
    RimeListModelsResponse,
    RimeRegisterDatasetResponse,
    RimeRegisterModelResponse,
    RimeUUID,
    SchemaregistryMetadata,
)

logger = logging.getLogger(__name__)


class Registry:
    """Registry object wrapper with helpful methods for working with the Registry.

    Attributes:
        api_client: ApiClient
                The client used to query about the status of the job.
    """

    def __init__(self, api_client: ApiClient) -> None:
        """Create a new Registry wrapper object.

        Arguments:
            api_client: ApiClient
                The client used to query about the status of the job.
        """
        self._api_client = api_client

    def register_dataset(
        self,
        project_id: str,
        name: str,
        data_config: dict,
        integration_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """Register a new dataset."""
        data_info_swagger = convert_single_data_info_to_swagger(data_config)
        req = DatasetProjectIdUuidBody(
            project_id=RimeUUID(uuid=project_id), name=name, data_info=data_info_swagger
        )

        metadata_str: Optional[str] = None
        if metadata is not None:
            metadata_str = json.dumps(metadata)
        if tags is not None or metadata_str is not None:
            req.metadata = SchemaregistryMetadata(tags=tags, extra_info=metadata_str)

        if integration_id is not None:
            req.integration_id = integration_id

        with RESTErrorHandler():
            api = swagger_client.RegistryServiceApi(self._api_client)
            res = api.registry_service_register_dataset(
                body=req, project_id_uuid=project_id,
            )

            res = cast(RimeRegisterDatasetResponse, res)

        return res.dataset_id

    def register_model(
        self,
        project_id: str,
        name: str,
        model_config: Optional[dict] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
        external_id: Optional[str] = None,
    ) -> str:
        """Register a new model."""
        req = ModelProjectIdUuidBody(project_id=RimeUUID(uuid=project_id), name=name,)

        if model_config is not None:
            model_info = convert_model_info_to_swagger(model_config)
            req.model_info = model_info

        metadata_str: Optional[str] = None
        if metadata:
            metadata_str = json.dumps(metadata)
        if tags or metadata_str:
            req.metadata = SchemaregistryMetadata(tags=tags, extra_info=metadata_str)
        if external_id:
            req.external_id = external_id

        with RESTErrorHandler():
            api = swagger_client.RegistryServiceApi(self._api_client)
            res = api.registry_service_register_model(
                body=req, project_id_uuid=project_id,
            )

            res = cast(RimeRegisterModelResponse, res)

        return cast(RimeUUID, res.model_id).uuid

    def register_predictions(
        self,
        project_id: str,
        dataset_id: str,
        model_id: str,
        pred_config: dict,
        integration_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """Register a new prediction."""
        pred_info_swagger = convert_single_pred_info_to_swagger(pred_config)

        req = ModelIdUuidDatasetIdBody(
            project_id=RimeUUID(uuid=project_id),
            model_id=RimeUUID(uuid=model_id),
            pred_info=pred_info_swagger,
        )

        metadata_str: Optional[str] = None
        if metadata is not None:
            metadata_str = json.dumps(metadata)
        if tags is not None or metadata_str is not None:
            req.metadata = SchemaregistryMetadata(tags=tags, extra_info=metadata_str)

        if integration_id is not None:
            req.integration_id = integration_id

        with RESTErrorHandler():
            api = swagger_client.RegistryServiceApi(self._api_client)
            _ = api.registry_service_register_prediction_set(
                body=req,
                project_id_uuid=project_id,
                model_id_uuid=model_id,
                dataset_id=dataset_id,
            )

    def list_datasets(self, project_id: str) -> Iterator[Dict]:
        """Return a list of datasets, each as a dictionary."""
        api = swagger_client.RegistryServiceApi(self._api_client)
        # Iterate through the pages of datasets and break at the last page.
        page_token = ""
        with RESTErrorHandler():
            while True:
                if page_token == "":
                    res: RimeListDatasetsResponse = api.registry_service_list_datasets(
                        project_id_uuid=project_id
                    )
                else:
                    res = api.registry_service_list_datasets(
                        project_id_uuid=project_id, page_token=page_token
                    )
                if res.datasets is not None:
                    for dataset in res.datasets:
                        yield dataset.to_dict()
                # Advance to the next page of datasets.
                page_token = res.next_page_token
                # we've reached the last page of datasets.
                if not res.has_more:
                    break

    def list_models(self, project_id: str) -> Iterator[Dict]:
        """Return a list of models, each as a dictionary."""
        api = swagger_client.RegistryServiceApi(self._api_client)
        # Iterate through the pages of datasets and break at the last page.
        page_token = ""
        with RESTErrorHandler():
            while True:
                if page_token == "":
                    res: RimeListModelsResponse = api.registry_service_list_models(
                        project_id_uuid=project_id
                    )
                else:
                    res = api.registry_service_list_models(
                        project_id_uuid=project_id, page_token=page_token
                    )
                if res.models is not None:
                    for model in res.models:
                        yield model.model.to_dict()
                # Advance to the next page of models.
                page_token = res.next_page_token
                # we've reached the last page of models.
                if not res.has_more:
                    break
