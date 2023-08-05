from typing import Final


CLASSIC_PORT: Final = 8080
AVATAR_PORT: Final = 9090
USERNAME: Final = "admin"
AUTH_USERNAME: Final = "username"
AUTH_PASSWORD: Final = "password"
AUTH_GRANT_TYPE: Final = "grant_type"
REQUEST_TIMEOUT: Final = 2000

ON_STATE: Final = "onState"
POINT_TEMPERATURE: Final = "pointTemperature"
SET_POINT_TEMPERATURE: Final = "setpointTemperature"
TEMPERATURE: Final = "temperature"
HUMIDITY: Final = "humidity"
IS_REACHABLE: Final = "isReachable"
LOCATION: Final = "location"
CAPABILITY_MAP: Final = "capabilityMap"

AUTHENTICATION_HEADERS: Final = {
    "Authorization": "Basic Y2xpZW50SWQ6Y2xpZW50UGFzcw==",
    "Content-type": "application/json",
    "Accept": "application/json",
}
