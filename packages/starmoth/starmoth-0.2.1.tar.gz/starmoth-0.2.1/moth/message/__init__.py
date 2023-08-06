from __future__ import annotations
import abc
from ast import Dict
import io
import time
from dataclasses import dataclass
from typing import Optional, Type
import uuid
import msgpack
from PIL import Image

from moth.message.exceptions import FailedToParseMessage, UnknownMessageType


def parse_message(msg: bytes) -> Msg:
    try:
        envelope = msgpack.unpackb(msg)
        message_type = envelope["msgType"]

        if message_type not in _MESSAGE_CLASSES:
            raise UnknownMessageType(f"Cannot parse message of type: {message_type}")

        message_class = _MESSAGE_CLASSES[message_type]
        return message_class.deserialize(envelope["payload"])

    except msgpack.exceptions.ExtraData:
        raise FailedToParseMessage("Invalid message format")


class Msg(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError()

    @classmethod
    def msg_type_name(cls):
        return cls.__name__

    def serialize_envelope(self) -> bytes:
        """
        Serialize the message and wrap it in an envelope so the recipient can check the
        message type and route the payload to the appropriate message parser.
        Use the `parse_message` function to unpack the message.
        """
        payload = self.serialize()
        envelope = {"msgType": self.msg_type_name(), "payload": payload}
        return msgpack.packb(envelope)

    @staticmethod
    def deserialize(data: bytes) -> Msg:
        raise NotImplementedError()


class HeartbeatMsg(Msg):
    def __init__(self, timestamp: Optional[int] = None):
        if timestamp == None:
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp

    def serialize(self):
        obj = {
            "t": self.timestamp,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(data: bytes) -> HeartbeatMsg:
        obj = msgpack.unpackb(data)
        return HeartbeatMsg(obj["t"])


class ImagePromptMsg(Msg):
    def __init__(self, image: Image.Image, id: Optional[str] = None):
        self.image = image
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def serialize(self):
        # Convert the image to bytes
        with io.BytesIO() as output:
            self.image.save(output, format="JPEG")
            img_bytes = output.getvalue()

        obj = {
            "id": self.id,
            "imageBytes": img_bytes,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(bytes) -> ImagePromptMsg:
        obj = msgpack.unpackb(bytes)
        id = obj.get("id")
        img = Image.open(io.BytesIO(obj["imageBytes"]))
        return ImagePromptMsg(img, id)


@dataclass
class PromptResultMsg(Msg):
    prompt_id: str
    class_index: Optional[int] = None
    class_name: Optional[str] = None

    def serialize(self):
        obj = {
            "promptId": self.prompt_id,
            "classIndex": self.class_index,
            "className": self.class_name,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(bytes) -> PromptResultMsg:
        obj = msgpack.unpackb(bytes)
        return PromptResultMsg(
            prompt_id=obj["promptId"],
            class_index=obj.get("classIndex"),
            class_name=obj.get("className"),
        )


@dataclass
class HandshakeMsg(Msg):
    name: str
    handshake_token: str
    version: str = "v0"

    def serialize(self) -> bytes:
        obj = {
            "name": self.name,
            "token": self.handshake_token,
            "version": self.version,
        }
        return msgpack.packb(obj)

    @staticmethod
    def deserialize(data: bytes) -> HandshakeMsg:
        obj = msgpack.unpackb(data)
        return HandshakeMsg(
            name=obj["name"], handshake_token=obj["token"], version=obj["version"]
        )


_MESSAGE_CLASSES: Dict[str, Type[Msg]] = {
    HandshakeMsg.msg_type_name(): HandshakeMsg,
    ImagePromptMsg.msg_type_name(): ImagePromptMsg,
    HeartbeatMsg.msg_type_name(): HeartbeatMsg,
    PromptResultMsg.msg_type_name(): PromptResultMsg,
}
