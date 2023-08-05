import voluptuous as vol
from collections.abc import Awaitable, Callable as Callable, Iterable
from homeassistant.auth.permissions.const import CAT_ENTITIES as CAT_ENTITIES, POLICY_CONTROL as POLICY_CONTROL
from homeassistant.const import ATTR_AREA_ID as ATTR_AREA_ID, ATTR_DEVICE_ID as ATTR_DEVICE_ID, ATTR_ENTITY_ID as ATTR_ENTITY_ID, CONF_ENTITY_ID as CONF_ENTITY_ID, CONF_SERVICE as CONF_SERVICE, CONF_SERVICE_DATA as CONF_SERVICE_DATA, CONF_SERVICE_TEMPLATE as CONF_SERVICE_TEMPLATE, CONF_TARGET as CONF_TARGET, ENTITY_MATCH_ALL as ENTITY_MATCH_ALL, ENTITY_MATCH_NONE as ENTITY_MATCH_NONE
from homeassistant.core import Context as Context, HomeAssistant as HomeAssistant, ServiceCall as ServiceCall, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError, TemplateError as TemplateError, Unauthorized as Unauthorized, UnknownUser as UnknownUser
from homeassistant.helpers import area_registry as area_registry, device_registry as device_registry, entity_registry as entity_registry, template as template
from homeassistant.helpers.entity import Entity as Entity
from homeassistant.helpers.entity_platform import EntityPlatform as EntityPlatform
from homeassistant.helpers.typing import ConfigType as ConfigType, TemplateVarsType as TemplateVarsType
from homeassistant.loader import Integration as Integration, MAX_LOAD_CONCURRENTLY as MAX_LOAD_CONCURRENTLY, async_get_integration as async_get_integration, bind_hass as bind_hass
from homeassistant.util.async_ import gather_with_concurrency as gather_with_concurrency
from homeassistant.util.yaml import load_yaml as load_yaml
from homeassistant.util.yaml.loader import JSON_TYPE as JSON_TYPE
from typing import Any, TypedDict

CONF_SERVICE_ENTITY_ID: str
CONF_SERVICE_DATA_TEMPLATE: str
_LOGGER: Any
SERVICE_DESCRIPTION_CACHE: str

class ServiceParams(TypedDict):
    domain: str
    service: str
    service_data: dict[str, Any]
    target: Union[dict, None]

class ServiceTargetSelector:
    entity_ids: Any
    device_ids: Any
    area_ids: Any
    def __init__(self, service_call: ServiceCall) -> None: ...
    @property
    def has_any_selector(self) -> bool: ...

class SelectedEntities:
    referenced: set[str]
    indirectly_referenced: set[str]
    missing_devices: set[str]
    missing_areas: set[str]
    referenced_devices: set[str]
    def log_missing(self, missing_entities: set[str]) -> None: ...

def call_from_config(hass: HomeAssistant, config: ConfigType, blocking: bool = ..., variables: TemplateVarsType = ..., validate_config: bool = ...) -> None: ...
async def async_call_from_config(hass: HomeAssistant, config: ConfigType, blocking: bool = ..., variables: TemplateVarsType = ..., validate_config: bool = ..., context: Union[Context, None] = ...) -> None: ...
def async_prepare_call_from_config(hass: HomeAssistant, config: ConfigType, variables: TemplateVarsType = ..., validate_config: bool = ...) -> ServiceParams: ...
def extract_entity_ids(hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...) -> set[str]: ...
async def async_extract_entities(hass: HomeAssistant, entities: Iterable[Entity], service_call: ServiceCall, expand_group: bool = ...) -> list[Entity]: ...
async def async_extract_entity_ids(hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...) -> set[str]: ...
def _has_match(ids: Union[str, list, None]) -> bool: ...
async def async_extract_referenced_entity_ids(hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...) -> SelectedEntities: ...
async def async_extract_config_entry_ids(hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...) -> set: ...
def _load_services_file(hass: HomeAssistant, integration: Integration) -> JSON_TYPE: ...
def _load_services_files(hass: HomeAssistant, integrations: Iterable[Integration]) -> list[JSON_TYPE]: ...
async def async_get_all_descriptions(hass: HomeAssistant) -> dict[str, dict[str, Any]]: ...
def async_set_service_schema(hass: HomeAssistant, domain: str, service: str, schema: dict[str, Any]) -> None: ...
async def entity_service_call(hass: HomeAssistant, platforms: Iterable[EntityPlatform], func: Union[str, Callable[..., Any]], call: ServiceCall, required_features: Union[Iterable[int], None] = ...) -> None: ...
async def _handle_entity_call(hass: HomeAssistant, entity: Entity, func: Union[str, Callable[..., Any]], data: Union[dict, ServiceCall], context: Context) -> None: ...
def async_register_admin_service(hass: HomeAssistant, domain: str, service: str, service_func: Callable[[ServiceCall], Union[Awaitable, None]], schema: vol.Schema = ...) -> None: ...
def verify_domain_control(hass: HomeAssistant, domain: str) -> Callable[[Callable[[ServiceCall], Any]], Callable[[ServiceCall], Any]]: ...

class ReloadServiceHelper:
    _service_func: Any
    _service_running: bool
    _service_condition: Any
    def __init__(self, service_func: Callable[[ServiceCall], Awaitable]) -> None: ...
    async def execute_service(self, service_call: ServiceCall) -> None: ...
