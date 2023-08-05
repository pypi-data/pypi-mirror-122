from homeassistant.components.sensor import SensorEntityDescription as SensorEntityDescription
from homeassistant.const import CONF_CLIENT_ID as CONF_CLIENT_ID, CONF_CLIENT_SECRET as CONF_CLIENT_SECRET, LENGTH_FEET as LENGTH_FEET, MASS_KILOGRAMS as MASS_KILOGRAMS, MASS_MILLIGRAMS as MASS_MILLIGRAMS, PERCENTAGE as PERCENTAGE, TIME_MILLISECONDS as TIME_MILLISECONDS, TIME_MINUTES as TIME_MINUTES
from typing import Any, Final

ATTR_ACCESS_TOKEN: Final[str]
ATTR_REFRESH_TOKEN: Final[str]
ATTR_LAST_SAVED_AT: Final[str]
ATTR_DURATION: Final[str]
ATTR_DISTANCE: Final[str]
ATTR_ELEVATION: Final[str]
ATTR_HEIGHT: Final[str]
ATTR_WEIGHT: Final[str]
ATTR_BODY: Final[str]
ATTR_LIQUIDS: Final[str]
ATTR_BLOOD_GLUCOSE: Final[str]
ATTR_BATTERY: Final[str]
CONF_MONITORED_RESOURCES: Final[str]
CONF_CLOCK_FORMAT: Final[str]
ATTRIBUTION: Final[str]
FITBIT_AUTH_CALLBACK_PATH: Final[str]
FITBIT_AUTH_START: Final[str]
FITBIT_CONFIG_FILE: Final[str]
FITBIT_DEFAULT_RESOURCES: Final[list[str]]
DEFAULT_CONFIG: Final[dict[str, str]]
DEFAULT_CLOCK_FORMAT: Final[str]

class FitbitRequiredKeysMixin:
    unit_type: Union[str, None]

class FitbitSensorEntityDescription(SensorEntityDescription, FitbitRequiredKeysMixin): ...

FITBIT_RESOURCES_LIST: Final[tuple[FitbitSensorEntityDescription, ...]]
FITBIT_RESOURCE_BATTERY: Any
FITBIT_RESOURCES_KEYS: Final[list[str]]
FITBIT_MEASUREMENTS: Final[dict[str, dict[str, str]]]
BATTERY_LEVELS: Final[dict[str, int]]
