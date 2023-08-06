from typing import Callable, Dict
import zmq
from moth.driver import ModelDriver
from moth.message import HandshakeMsg, PromptResultMsg, Msg, parse_message
from moth.message.exceptions import MothMessageError


class IdentityPool:
    def __init__(self):
        self._ids = []

    def add_identity(self, name: str, token: str):
        self._ids.append((name, token))

    def validate_handshake(self, identity: str, msg: HandshakeMsg) -> bool:
        if identity != msg.name:
            return False

        id_ = [i for i in self._ids if i[1] == msg.handshake_token]
        if len(id_) != 1:
            return False

        if id_[0][0] == identity and id_[0][1] == msg.handshake_token:
            return True


class MessageHandler:
    def onMessage(self, msg: Msg):
        pass


class Server:
    def __init__(self, port: 7171):
        self.port = port
        self._stop = False
        self._driver_factory = None
        self._drivers: Dict[str, ModelDriver] = {}

    def driver_factory(self, func: Callable[[HandshakeMsg], ModelDriver]):
        """
        Annotation to provide driver factory function.
        For every incoming model connection, this factory is called to get a driver for
        that model.
        """
        self._driver_factory = func
        return func

    def start(self):
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        socket.bind(f"tcp://*:{self.port}")
        self._recv_loop(socket)

    def stop(self):
        self._stop = True

    def _recv_loop(self, socket):
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        while not self._stop:
            # handle input
            events = dict(poll.poll(1000))
            if events:
                identity = socket.recv()
                msg_bytes = socket.recv()

                try:
                    message = parse_message(msg_bytes)
                    if isinstance(message, HandshakeMsg) and self._driver_factory:
                        self._drivers[identity] = self._driver_factory(message)

                    if isinstance(message, PromptResultMsg):
                        if identity in self._drivers:
                            self._drivers[identity].on_model_result(message)

                except MothMessageError as err:
                    print(err)
                except Exception as err:
                    print(err)

            for identity in self._drivers:
                next_prompt = self._drivers[identity].next_model_prompt()
                if next_prompt is not None:
                    socket.send(identity, zmq.SNDMORE)
                    socket.send(next_prompt.serialize_envelope())
