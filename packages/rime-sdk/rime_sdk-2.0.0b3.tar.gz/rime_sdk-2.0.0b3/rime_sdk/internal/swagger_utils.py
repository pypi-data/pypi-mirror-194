"""Utility functions for converting between SDK args and proto objects."""

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TypeVar

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from rime_sdk.swagger.swagger_client import (
    FirewallCustomLoaderLocation,
    FirewallDataCollectorLocation,
    FirewallDeltaLakeLocation,
    FirewallLocationArgs,
    FirewallLocationParams,
    RimeUUID,
    TestrunDataInfoParams,
    TestrunPredictionParams,
)
from rime_sdk.swagger.swagger_client.models import (
    RimeModelTask,
    RimeThresholdDirection,
    RimeThresholdInfo,
    SchemafirewallDataLocation,
)


def swagger_is_empty(swagger_val: Any) -> bool:
    """Check if a swagger object is empty."""
    return not bool(swagger_val)


TYPE_KEY = "enum_type"
PROTO_FIELD_KEY = "proto_field"
PROTO_TYPE_KEY = "proto_type"

BASE_TYPES = ["str", "float", "int", "bool"]

T = TypeVar("T")


def parse_dict_to_swagger(obj_dict: Optional[Dict], new_obj: T) -> T:
    """Parse non-nested dicts into a new object."""
    if obj_dict:
        for key, value in obj_dict.items():
            setattr(new_obj, key, value)
    return new_obj


THRESHOLD_INFO_TO_ENUM_MAP = {
    "above": RimeThresholdDirection.ABOVE,
    "below": RimeThresholdDirection.BELOW,
    None: RimeThresholdDirection.UNSPECIFIED,
}


def get_threshold_direction_swagger(direction: Optional[str]) -> str:
    """Get the threshold direction protobuf."""
    _direction = THRESHOLD_INFO_TO_ENUM_MAP.get(direction)
    if _direction is None:
        # TODO: Handle "both" cases
        raise ValueError(
            f"Invalid threshold direction {direction}. Expected 'above' or 'below'."
        )
    return _direction


def get_threshold_info_swagger(metric_threshold_info: dict) -> RimeThresholdInfo:
    """Return the threshold info map."""
    info_copy = deepcopy(metric_threshold_info)
    info_copy["direction"] = get_threshold_direction_swagger(
        metric_threshold_info.get("direction")
    )
    return parse_dict_to_swagger(info_copy, RimeThresholdInfo())


def threshold_infos_to_map(
    threshold_infos: List[RimeThresholdInfo],
) -> Dict[str, RimeThresholdInfo]:
    """Return map of metric name to RimeThresholdInfo."""
    threshold_info_map = {}
    for threshold_info in threshold_infos:
        info_without_metric = RimeThresholdInfo(
            direction=threshold_info.direction,
            low=threshold_info.low,
            high=threshold_info.high,
            disabled=threshold_info.disabled,
        )
        threshold_info_map[threshold_info.metric_name] = info_without_metric
    return threshold_info_map


DEFAULT_THRESHOLD_INFO_KEY_ORDER = list(RimeThresholdInfo.swagger_types.keys())
# Put metric_name at the beginning
DEFAULT_THRESHOLD_INFO_KEY_ORDER.remove("metric_name")
DEFAULT_THRESHOLD_INFO_KEY_ORDER = ["metric_name"] + DEFAULT_THRESHOLD_INFO_KEY_ORDER


def get_model_task_enum_swagger(model_task: str) -> str:
    """Get the model task enum from string."""
    if model_task == "Binary Classification":
        return RimeModelTask.BINARY_CLASSIFICATION
    elif model_task == "Multi-class Classification":
        return RimeModelTask.MULTICLASS_CLASSIFICATION
    elif model_task == "Regression":
        return RimeModelTask.REGRESSION
    elif model_task == "Ranking":
        return RimeModelTask.RANKING
    elif model_task == "Named Entity Recognition":
        return RimeModelTask.NAMED_ENTITY_RECOGNITION
    elif model_task == "Natural Language Inference":
        return RimeModelTask.NATURAL_LANGUAGE_INFERENCE
    elif model_task == "Text Classification":
        return RimeModelTask.TEXT_CLASSIFICATION
    elif model_task == "Object Detection":
        return RimeModelTask.OBJECT_DETECTION
    elif model_task == "Image Classification":
        return RimeModelTask.IMAGE_CLASSIFICATION
    elif model_task == "Fill Mask":
        return RimeModelTask.FILL_MASK
    else:
        raise ValueError(f"Got unknown model task ({model_task}).")


def get_data_location_swagger(data_location: Dict) -> SchemafirewallDataLocation:
    """Get the data location enum from string."""
    return SchemafirewallDataLocation(
        integration_id=RimeUUID(uuid=data_location["integration_id"]),
        location_args=get_firewall_location_args_swagger(
            data_location["location_args"]
        ),
        location_params=get_firewall_location_params_swagger(
            data_location["location_params"]
        ),
    )


def get_firewall_location_args_swagger(location_args: Dict) -> FirewallLocationArgs:
    """Get the firewall location args enum from string."""
    key = select_oneof(
        location_args,
        ["data_collector_location", "delta_lake_location", "custom_location"],
    )
    if key == "data_collector_location":
        return FirewallLocationArgs(
            delta_lake_location=parse_dict_to_swagger(
                location_args[key], FirewallDataCollectorLocation()
            )
        )
    elif key == "delta_lake_location":
        return FirewallLocationArgs(
            delta_lake_location=parse_dict_to_swagger(
                location_args[key], FirewallDeltaLakeLocation()
            )
        )
    elif key == "custom_location":
        return FirewallLocationArgs(
            custom_location=parse_dict_to_swagger(
                location_args[key], FirewallCustomLoaderLocation()
            )
        )
    else:
        raise ValueError(f"Got unknown firewall location args ({location_args}).")


def get_firewall_location_params_swagger(
    location_params: Dict,
) -> FirewallLocationParams:
    """Get the firewall location params enum from string."""
    key = select_oneof(location_params, ["data_params", "pred_params"])
    if key == "data_params":
        return FirewallLocationParams(
            data_params=parse_dict_to_swagger(
                location_params[key], TestrunDataInfoParams()
            )
        )
    elif key == "pred_params":
        return FirewallLocationParams(
            pred_params=parse_dict_to_swagger(
                location_params[key], TestrunPredictionParams()
            )
        )
    else:
        raise ValueError(f"Got unknown firewall location params ({location_params}).")


def serialize_datetime_to_proto_timestamp(date: datetime) -> Dict:
    """Convert datetime to swagger compatible grpc timestamp."""
    timestamp = Timestamp()
    timestamp.FromDatetime(date)
    # Swagger serialize datetime to iso8601 format, convert to
    # protobuf compatible serialization
    return MessageToDict(timestamp)


def rest_to_timedelta(delta: str) -> timedelta:
    """Convert a REST API compatible string to a time delta."""
    # REST API returns a string in seconds; e.g. one day is represented as "86400s"
    return timedelta(seconds=int(delta[:-1]))


def timedelta_to_rest(delta: timedelta) -> str:
    """Convert a time delta to a REST API compatible string."""
    return f"{int(delta.total_seconds())}s"


def select_oneof(oneof_map: Dict[str, Any], key_list: List[str]) -> Any:
    """Select one of the keys in the map.

    Args:
        oneof_map: The map to select from.
        key_list: The list of keys to select from.

    Returns:
        The key that was selected.

    Raises:
        ValueError: If more than one of the keys are provided in the map.
    """
    selected_key = None
    for key in key_list:
        if key in oneof_map:
            if selected_key is not None:
                raise ValueError(
                    f"More than one of the keys {key_list} were provided in the map."
                )
            selected_key = key
    if selected_key is None:
        raise ValueError(f"None of the keys {key_list} were provided in the map.")
    return selected_key
