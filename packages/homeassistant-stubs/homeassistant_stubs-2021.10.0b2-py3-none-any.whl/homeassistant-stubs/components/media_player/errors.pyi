from homeassistant.exceptions import HomeAssistantError as HomeAssistantError

class MediaPlayerException(HomeAssistantError): ...
class BrowseError(MediaPlayerException): ...
