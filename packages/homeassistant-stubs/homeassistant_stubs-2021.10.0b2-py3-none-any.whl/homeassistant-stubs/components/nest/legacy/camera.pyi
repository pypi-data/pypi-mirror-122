from .const import DATA_NEST as DATA_NEST, DOMAIN as DOMAIN
from homeassistant.components.camera import Camera as Camera, PLATFORM_SCHEMA as PLATFORM_SCHEMA, SUPPORT_ON_OFF as SUPPORT_ON_OFF
from homeassistant.util.dt import utcnow as utcnow
from typing import Any

_LOGGER: Any
NEST_BRAND: str

def setup_platform(hass, config, add_entities, discovery_info: Any | None = ...) -> None: ...
async def async_setup_legacy_entry(hass, entry, async_add_entities) -> None: ...

class NestCamera(Camera):
    structure: Any
    device: Any
    _location: Any
    _name: Any
    _online: Any
    _is_streaming: Any
    _is_video_history_enabled: bool
    _time_between_snapshots: Any
    _last_image: Any
    _next_snapshot_at: Any
    def __init__(self, structure, device) -> None: ...
    @property
    def name(self): ...
    @property
    def unique_id(self): ...
    @property
    def device_info(self): ...
    @property
    def should_poll(self): ...
    @property
    def is_recording(self): ...
    @property
    def brand(self): ...
    @property
    def supported_features(self): ...
    @property
    def is_on(self): ...
    def turn_off(self) -> None: ...
    def turn_on(self) -> None: ...
    def update(self) -> None: ...
    def _ready_for_snapshot(self, now): ...
    def camera_image(self, width: Union[int, None] = ..., height: Union[int, None] = ...) -> Union[bytes, None]: ...
