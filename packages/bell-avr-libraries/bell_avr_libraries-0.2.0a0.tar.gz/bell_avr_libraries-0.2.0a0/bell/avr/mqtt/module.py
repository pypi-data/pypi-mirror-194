# This file is automatically @generated. DO NOT EDIT!
# fmt: off

from __future__ import annotations
import copy
from typing import Any, Literal, Union, overload

import paho.mqtt.client as paho_mqtt
import pydantic
from loguru import logger

from bell.avr.mqtt.client import MQTTClient
from bell.avr.mqtt.constants import _MQTTTopicPayloadTypedDict
from bell.avr.mqtt.dispatcher import dispatch_message
from bell.avr.mqtt.payloads import (
    AVRPCMColorSet,
    AVRPCMColorTimed,
    AVREmptyMessage,
    AVRPCMServo,
    AVRPCMServoPWM,
    AVRPCMServoPercent,
    AVRPCMServoAbsolute,
    AVRFCMHILGPSStats,
    AVRFCMAirborne,
    AVRFCMLanded,
    AVRFCMBattery,
    AVRFCMArmed,
    AVRFCMFlightMode,
    AVRFCMPositionLocal,
    AVRFCMPositionGlobal,
    AVRFCMPositionHome,
    AVRFCMAttitudeEulerDegrees,
    AVRFCMVelocity,
    AVRFCMGPSInfo,
    AVRFusionPositionLocal,
    AVRFusionVelocity,
    AVRFusionPositionGlobal,
    AVRFusionGroundspeed,
    AVRFusionCourse,
    AVRFusionHeading,
    AVRFusionClimbRate,
    AVRFusionAttitudeQuaternion,
    AVRFusionAttitudeEulerRadians,
    AVRFusionHILGPSMessage,
    AVRVIOResync,
    AVRVIOPositionLocal,
    AVRVIOVelocity,
    AVRVIOAttitudeEulerRadians,
    AVRVIOAttitudeQuaternion,
    AVRVIOHeading,
    AVRVIOConfidence,
    AVRAprilTagsVehiclePosition,
    AVRAprilTagsRaw,
    AVRAprilTagsVisible,
    AVRAprilTagsStatus,
    AVRThermalReading,
    AVRAutonomousBuildingEnable,
    AVRAutonomousBuildingDisable,
)
from bell.avr.mqtt.serializer import deserialize_payload, serialize_payload


class MQTTModule(MQTTClient):
    """
    Generic MQTT Module class that should be inherited by other modules.
    The `topic_callbacks` attribute should be a dictionary of topics to functions
    that will be called with a payload.
    """
    def __init__(self):
        super().__init__()

        # maintain a cache of the last message sent on a topic by this client
        self.message_cache: _MQTTTopicPayloadTypedDict = {}

    def on_message(self, client: paho_mqtt.Client, userdata: Any, msg: paho_mqtt.MQTTMessage) -> None:
        """
        Process and dispatch an incoming message.
        """
        payload = deserialize_payload(msg.topic, msg.payload)

        if self.enable_verbose_logging:
            logger.debug(f"Recieved {msg.topic}: {msg.payload}")

        dispatch_message(self.topic_callbacks, msg.topic, payload)

    @overload
    def send_message(self, topic: Literal["avr/pcm/color/set"], payload: Union[AVRPCMColorSet, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/color/timed"], payload: Union[AVRPCMColorTimed, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/fire"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/on"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/off"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/open"], payload: Union[AVRPCMServo, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/close"], payload: Union[AVRPCMServo, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/pwm/min"], payload: Union[AVRPCMServoPWM, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/pwm/max"], payload: Union[AVRPCMServoPWM, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/percent"], payload: Union[AVRPCMServoPercent, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/absolute"], payload: Union[AVRPCMServoAbsolute, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/hil_gps/stats"], payload: Union[AVRFCMHILGPSStats, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/airborne"], payload: Union[AVRFCMAirborne, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/landed"], payload: Union[AVRFCMLanded, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/battery"], payload: Union[AVRFCMBattery, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/armed"], payload: Union[AVRFCMArmed, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/flight_mode"], payload: Union[AVRFCMFlightMode, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/local"], payload: Union[AVRFCMPositionLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/global"], payload: Union[AVRFCMPositionGlobal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/home"], payload: Union[AVRFCMPositionHome, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/attitude/euler/degrees"], payload: Union[AVRFCMAttitudeEulerDegrees, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/velocity"], payload: Union[AVRFCMVelocity, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/gps/info"], payload: Union[AVRFCMGPSInfo, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/position/local"], payload: Union[AVRFusionPositionLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/velocity"], payload: Union[AVRFusionVelocity, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/position/global"], payload: Union[AVRFusionPositionGlobal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/groundspeed"], payload: Union[AVRFusionGroundspeed, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/course"], payload: Union[AVRFusionCourse, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/heading"], payload: Union[AVRFusionHeading, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/climb_rate"], payload: Union[AVRFusionClimbRate, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/quaternion"], payload: Union[AVRFusionAttitudeQuaternion, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/euler/radians"], payload: Union[AVRFusionAttitudeEulerRadians, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/hil_gps/message"], payload: Union[AVRFusionHILGPSMessage, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/resync"], payload: Union[AVRVIOResync, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/position/local"], payload: Union[AVRVIOPositionLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/velocity"], payload: Union[AVRVIOVelocity, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/attitude/euler/radians"], payload: Union[AVRVIOAttitudeEulerRadians, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/attitude/quaternion"], payload: Union[AVRVIOAttitudeQuaternion, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/heading"], payload: Union[AVRVIOHeading, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/confidence"], payload: Union[AVRVIOConfidence, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/vehicle_position"], payload: Union[AVRAprilTagsVehiclePosition, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/raw"], payload: Union[AVRAprilTagsRaw, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/visible"], payload: Union[AVRAprilTagsVisible, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/status"], payload: Union[AVRAprilTagsStatus, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/pcm"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/vio"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/apriltags"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/fcm"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/thermal"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/thermal/reading"], payload: Union[AVRThermalReading, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/enable"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/disable"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/enable"], payload: Union[AVRAutonomousBuildingEnable, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/disable"], payload: Union[AVRAutonomousBuildingDisable, dict], force_write: bool = False) -> None: ...

    def send_message(self, topic: str, payload: Union[pydantic.BaseModel, dict, None] = None, force_write: bool = False) -> None:
        """
        Sends a message to the MQTT broker. Enabling `force_write` will
        forcefully send the message, bypassing threading mutex. Only use this
        if you know what you're doing.
        """
        str_payload = serialize_payload(topic, payload)
        self._publish(topic, str_payload, force_write)
        self.message_cache[topic] = copy.deepcopy(payload)