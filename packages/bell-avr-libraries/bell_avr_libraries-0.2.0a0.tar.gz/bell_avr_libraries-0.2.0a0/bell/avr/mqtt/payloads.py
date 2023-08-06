# This file is automatically @generated. DO NOT EDIT!
# fmt: off

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Literal, Optional, Protocol, Tuple, Type, Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra, Field, conlist, validator


def _convert_type(iter: Union[list, tuple], convert_to: Union[Type[int], Type[float]]) -> Union[tuple, int, float]:
    if isinstance(iter, (tuple, list)):
        return tuple(_convert_type(x, convert_to) for x in iter)
    else:
        return convert_to(iter)


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid


class AVREmptyMessage(BaseModel):
    pass

class AVRPCMColorSetWrgbItem(BaseModel):
    __root__: int = Field(..., ge=0, le=255)

    def __int__(self) -> int:
        return self.__root__


class AVRPCMColorSet(BaseModel):
    if TYPE_CHECKING:
        wrgb: Tuple[int, int, int, int]
    else:
        wrgb: conlist(AVRPCMColorSetWrgbItem, min_items=4, max_items=4)
    """
    Color values for the white, red, green, and blue channels, respectively.
    """
    @validator('wrgb')
    def validate_wrgb(cls, v):
        return _convert_type(v, int)


class AVRPCMColorTimedWrgbItem(BaseModel):
    __root__: int = Field(..., ge=0, le=255)

    def __int__(self) -> int:
        return self.__root__


class AVRPCMColorTimed(BaseModel):
    if TYPE_CHECKING:
        wrgb: Tuple[int, int, int, int]
    else:
        wrgb: conlist(AVRPCMColorTimedWrgbItem, min_items=4, max_items=4)
    """
    Color values for the white, red, green, and blue channels, respectively.
    """
    @validator('wrgb')
    def validate_wrgb(cls, v):
        return _convert_type(v, int)

    time: float = Field(default=0.5, ge=0)
    """
    Number of seconds the color should be set for. Default is 0.5.
    """

class AVRPCMServo(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """

class AVRPCMServoPWM(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """
    pulse: int = Field(..., ge=0, le=1000)
    """
    Pulse width.
    """

class AVRPCMServoPercent(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """
    percent: int = Field(..., ge=0, le=100)
    """
    Servo percent. 0 is closed, and 100 is open.
    """

class AVRPCMServoAbsolute(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """
    position: int
    """
    Absolute position of the servo.
    """

class AVRFCMHILGPSStats(BaseModel):
    frames: int
    """
    The number of messages that have been sent to the flight controller since the software has started.
    """

class AVRFCMAirborne(BaseModel):
    airborne: bool
    """
    Whether the drone is currently airborne or not.
    """

class AVRFCMLanded(BaseModel):
    landed: Literal["UNKNOWN", "ON_GROUND", "IN_AIR", "TAKING_OFF", "LANDING"]
    """
    Landed state of the drone.
    """

class AVRFCMBattery(BaseModel):
    voltage: float
    """
    Battery voltage.
    """
    state_of_charge: float = Field(..., ge=0, le=100)
    """
    Battery state of charge as a percentage
    """

class AVRFCMArmed(BaseModel):
    armed: bool
    """
    Indicates if the drone is currently armed
    """

class AVRFCMFlightMode(BaseModel):
    flight_mode: Literal["UNKNOWN", "READY", "TAKEOFF", "HOLD", "MISSION", "RETURN_TO_LAUNCH", "LAND", "OFFBOARD", "FOLLOW_ME", "MANUAL", "ALTCTL", "POSCTL", "ACRO", "STABILIZED", "RATTITUDE"]
    """
    Active flight mode
    """

class AVRFCMPositionLocal(BaseModel):
    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRFCMPositionGlobal(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    alt: float
    """
    Altitude relative to takeoff altitude in meters.
    """
    hdg: float
    """
    Heading in degrees.
    """

class AVRFCMPositionHome(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    alt: float
    """
    Altitude relative to the home position in meters.
    """

class AVRFCMAttitudeEulerDegrees(BaseModel):
    roll: float = Field(..., ge=-360, le=360)
    """
    Roll in degrees.
    """
    pitch: float = Field(..., ge=-360, le=360)
    """
    Pitch in degrees.
    """
    yaw: float = Field(..., ge=-360, le=360)
    """
    Yaw in degrees.
    """

class AVRFCMVelocity(BaseModel):
    Vn: float
    """
    X velocity in a North/East/Down coordinate system in meters per second.
    """
    Ve: float
    """
    Y velocity in a North/East/Down coordinate system in meters per second.
    """
    Vd: float
    """
    Z velocity in a North/East/Down coordinate system in meters per second.
    """

class AVRFCMGPSInfo(BaseModel):
    visible_satellites: int
    """
    Number of visible satellites in use. HIL GPS will appear as 13.
    """
    fix_type: Literal["NO_GPS", "NO_FIX", "FIX_2D", "FIX_3D", "FIX_DGPS", "RTK_FLOAT", "RTK_FIXED"]
    """
    GPS fix type
    """

class AVRFusionPositionLocal(BaseModel):
    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRFusionVelocity(BaseModel):
    Vn: float
    """
    X velocity in a North/East/Down coordinate system in meters per second.
    """
    Ve: float
    """
    Y velocity in a North/East/Down coordinate system in meters per second.
    """
    Vd: float
    """
    Z velocity in a North/East/Down coordinate system in meters per second.
    """

class AVRFusionPositionGlobal(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    alt: float
    """
    Altitude relative to takeoff altitude in meters.
    """

class AVRFusionGroundspeed(BaseModel):
    groundspeed: float
    """
    Groundspeed of the drone in meters per second. This is a normal vector of the N and E velocities.
    """

class AVRFusionHeading(BaseModel):
    hdg: float
    """
    Heading in degrees.
    """

class AVRFusionCourse(BaseModel):
    course: float = Field(..., ge=0, le=360)
    """
    Course in degrees.
    """

class AVRFusionClimbRate(BaseModel):
    climb_rate: float
    """
    Rate of climb in feet per minute.
    """

class AVRFusionAttitudeQuaternion(BaseModel):
    x: float = Field(..., ge=-1, le=1)
    """
    Quaternion x value.
    """
    y: float = Field(..., ge=-1, le=1)
    """
    Quaternion y value.
    """
    z: float = Field(..., ge=-1, le=1)
    """
    Quaternion z value.
    """
    w: float = Field(..., ge=-1, le=1)
    """
    Quaternion w value.
    """

class AVRFusionAttitudeEulerRadians(BaseModel):
    psi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Roll in radians.
    """
    theta: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Pitch in radians.
    """
    phi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Yaw in radians.
    """

class AVRFusionHILGPSMessage(BaseModel):
    time_usec: int
    """
    UNIX epoch timestamp in microseconds
    """
    fix_type: int = Field(..., ge=0, le=3)
    """
    0-1: no fix, 2: 2D fix, 3: 3D fix
    """
    lat: int
    """
    WGS84 Latitude * 10000000
    """
    lon: int
    """
    WGS84 Longitude * 10000000
    """
    alt: int
    """
    Altitude from sea level in mm. Positive for up.
    """
    eph: int
    """
    GPS HDOP (horizontal dilution of position)
    """
    epv: int
    """
    GPS VDOP (vertical dilution of position)
    """
    vel: int
    """
    GPS ground speed in centimeters per second
    """
    vn: int
    """
    GPS velocity in north direction in centimeters per second
    """
    ve: int
    """
    GPS velocity in east direction in centimeters per second
    """
    vd: int
    """
    GPS velocity in down direction in centimeters per second
    """
    cog: int
    """
    Course over ground in degrees
    """
    satellites_visible: int = Field(..., ge=0)
    """
    Number of satellites visible. This is hardcoded to 13 for our HIL GPS.
    """
    heading: int
    """
    Custom heading field. This is the heading in degrees * 100.
    """

class AVRVIOResync(BaseModel):
    hdg: float
    """
    Heading in degrees.
    """
    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRVIOPositionLocal(BaseModel):
    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRVIOVelocity(BaseModel):
    Vn: float
    """
    X velocity in a North/East/Down coordinate system in meters per second.
    """
    Ve: float
    """
    Y velocity in a North/East/Down coordinate system in meters per second.
    """
    Vd: float
    """
    Z velocity in a North/East/Down coordinate system in meters per second.
    """

class AVRVIOAttitudeEulerRadians(BaseModel):
    psi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Roll in radians.
    """
    theta: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Pitch in radians.
    """
    phi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Yaw in radians.
    """

class AVRVIOAttitudeQuaternion(BaseModel):
    x: float = Field(..., ge=-1, le=1)
    """
    Quaternion x value.
    """
    y: float = Field(..., ge=-1, le=1)
    """
    Quaternion y value.
    """
    z: float = Field(..., ge=-1, le=1)
    """
    Quaternion z value.
    """
    w: float = Field(..., ge=-1, le=1)
    """
    Quaternion w value.
    """

class AVRVIOHeading(BaseModel):
    hdg: float
    """
    Heading in degrees.
    """

class AVRVIOConfidence(BaseModel):
    tracking: float = Field(..., ge=0, le=100)
    """
    Tracking confidence percentage. Higher number is better.
    """

class AVRAprilTagsVehiclePosition(BaseModel):
    tag_id: int = Field(..., ge=0)
    """
    AprilTag ID.
    """
    x: float
    """
    X position in a North/East/Down coordinate system in centimeters.
    """
    y: float
    """
    Y position in a North/East/Down coordinate system in centimeters.
    """
    z: float
    """
    Z position in a North/East/Down coordinate system in centimeters.
    """
    hdg: float
    """
    Heading in degrees.
    """

class AVRAprilTagsRawApriltagsRotationItem(BaseModel):
    __root__: float = Field(..., ge=-1, le=1)

    def __float__(self) -> float:
        return self.__root__


class AVRAprilTagsRawApriltags(BaseModel):
    tag_id: int = Field(..., ge=0)
    """
    AprilTag ID.
    """
    x: float
    """
    The position in meters of the camera relative to the AprilTag's X frame.
    """
    y: float
    """
    The position in meters of the camera relative to the AprilTag's Y frame.
    """
    z: float
    """
    The position in meters of the camera relative to the AprilTag's Z frame.
    """
    if TYPE_CHECKING:
        rotation: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
    else:
        rotation: conlist(conlist(AVRAprilTagsRawApriltagsRotationItem, min_items=3, max_items=3), min_items=3, max_items=3)
    """
    3x3 rotation matrix.
    """
    @validator('rotation')
    def validate_rotation(cls, v):
        return _convert_type(v, float)


class AVRAprilTagsRaw(BaseModel):
    apriltags: List[AVRAprilTagsRawApriltags]

class AVRAprilTagsVisibleApriltagsAbsolutePosition(BaseModel):
    x: float
    """
    X position in a North/East/Down coordinate system in centimeters.
    """
    y: float
    """
    Y position in a North/East/Down coordinate system in centimeters.
    """
    z: float
    """
    Z position in a North/East/Down coordinate system in centimeters.
    """

class AVRAprilTagsVisibleApriltagsRelativePosition(BaseModel):
    x: float
    """
    X position in a North/East/Down coordinate system in centimeters.
    """
    y: float
    """
    Y position in a North/East/Down coordinate system in centimeters.
    """
    z: float
    """
    Z position in a North/East/Down coordinate system in centimeters.
    """

class AVRAprilTagsVisibleApriltags(BaseModel):
    tag_id: int = Field(..., ge=0)
    """
    AprilTag ID.
    """
    horizontal_distance: float
    """
    The horizontal scalar distance from the drone to AprilTag, in centimeters.
    """
    vertical_distance: float
    """
    The horizontal scalar distance from the drone to AprilTag, in centimeters.
    """
    angle: float
    """
    The angle formed by the vector pointing from the drones body to the AprilTag in world frame relative to world-north.
    """
    hdg: float
    """
    Heading in degrees.
    """
    relative_position: AVRAprilTagsVisibleApriltagsRelativePosition
    """
    The relative position of the drone relative to the AprilTag in world frame in centimeters.
    """
    absolute_position: Optional[AVRAprilTagsVisibleApriltagsAbsolutePosition]
    """
    The position of the drone in world frame in centimeters. If the tag has no truth data, this will not be present in the output.
    """

class AVRAprilTagsVisible(BaseModel):
    apriltags: List[AVRAprilTagsVisibleApriltags]

class AVRAprilTagsStatus(BaseModel):
    frames_per_second: int = Field(..., ge=0)
    """
    Number of frames of video data processed in the last second
    """

class AVRThermalReading(BaseModel):
    data: str
    """
    The raw data from the thermal camera are integer values from an 8x8 grid of pixels. This data is then converted into a `bytearray` and base64 encoded. Any example of how to unpack this data:

```python
import base64
import json

data = json.loads(payload)["data"]
base64_decoded = data.encode("utf-8")
as_bytes = base64.b64decode(base64_decoded)
pixel_ints = list(bytearray(as_bytes))
```

    """

class AVRAutonomousBuildingEnable(BaseModel):
    building: int = Field(..., ge=0, le=15)
    """
    Building ID. This is 0-indexed.
    """

class AVRAutonomousBuildingDisable(BaseModel):
    building: int = Field(..., ge=0, le=15)
    """
    Building ID. This is 0-indexed.
    """

class _AVRFCMPositionGlobalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMPositionGlobal) -> Any:
        ...

class _AVRVIOAttitudeQuaternionCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOAttitudeQuaternion) -> Any:
        ...

class _AVRPCMColorSetCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMColorSet) -> Any:
        ...

class _AVRVIOResyncCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOResync) -> Any:
        ...

class _AVRFCMAttitudeEulerDegreesCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMAttitudeEulerDegrees) -> Any:
        ...

class _AVRFCMAirborneCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMAirborne) -> Any:
        ...

class _AVRAutonomousBuildingDisableCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAutonomousBuildingDisable) -> Any:
        ...

class _AVRPCMServoAbsoluteCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServoAbsolute) -> Any:
        ...

class _AVRFCMPositionLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMPositionLocal) -> Any:
        ...

class _AVRFusionGroundspeedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionGroundspeed) -> Any:
        ...

class _AVRFusionAttitudeEulerRadiansCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionAttitudeEulerRadians) -> Any:
        ...

class _AVRVIOHeadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOHeading) -> Any:
        ...

class _AVRFusionHILGPSMessageCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionHILGPSMessage) -> Any:
        ...

class _AVRFCMBatteryCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMBattery) -> Any:
        ...

class _AVRFCMFlightModeCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMFlightMode) -> Any:
        ...

class _AVRFCMGPSInfoCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMGPSInfo) -> Any:
        ...

class _AVRFusionAttitudeQuaternionCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionAttitudeQuaternion) -> Any:
        ...

class _AVRAprilTagsVehiclePositionCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsVehiclePosition) -> Any:
        ...

class _AVRFCMHILGPSStatsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMHILGPSStats) -> Any:
        ...

class _AVRVIOAttitudeEulerRadiansCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOAttitudeEulerRadians) -> Any:
        ...

class _AVRAutonomousBuildingEnableCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAutonomousBuildingEnable) -> Any:
        ...

class _AVREmptyMessageCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self) -> Any:
        ...

class _AVRThermalReadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRThermalReading) -> Any:
        ...

class _AVRAprilTagsStatusCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsStatus) -> Any:
        ...

class _AVRFusionCourseCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionCourse) -> Any:
        ...

class _AVRFusionClimbRateCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionClimbRate) -> Any:
        ...

class _AVRFusionPositionLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionPositionLocal) -> Any:
        ...

class _AVRFusionVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionVelocity) -> Any:
        ...

class _AVRFCMArmedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMArmed) -> Any:
        ...

class _AVRFusionHeadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionHeading) -> Any:
        ...

class _AVRVIOPositionLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOPositionLocal) -> Any:
        ...

class _AVRFCMLandedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMLanded) -> Any:
        ...

class _AVRPCMColorTimedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMColorTimed) -> Any:
        ...

class _AVRPCMServoPWMCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServoPWM) -> Any:
        ...

class _AVRVIOConfidenceCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOConfidence) -> Any:
        ...

class _AVRPCMServoCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServo) -> Any:
        ...

class _AVRFCMPositionHomeCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMPositionHome) -> Any:
        ...

class _AVRFCMVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMVelocity) -> Any:
        ...

class _AVRVIOVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOVelocity) -> Any:
        ...

class _AVRAprilTagsVisibleCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsVisible) -> Any:
        ...

class _AVRFusionPositionGlobalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionPositionGlobal) -> Any:
        ...

class _AVRPCMServoPercentCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServoPercent) -> Any:
        ...

class _AVRAprilTagsRawCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsRaw) -> Any:
        ...
