import zmq

from moth.message import HandshakeMsg, ImagePromptMsg, parse_message
from moth.message.exceptions import MothMessageError


class Moth:
    _PROMPT_FUNCTIONS = []
    _MATH_FUNCTIONS = []

    def __init__(self, name: str, token: str = ""):
        self.name = name
        self._token = token
        self.stop = False

    def run(self, url="tcp://localhost:7171"):
        self.stop = False
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.setsockopt_string(zmq.IDENTITY, self.name)

        try:
            socket.connect(url)
            # This is a handshake call to prove our identity
            handshake = HandshakeMsg(self.name, self._token, "v0.0.0")
            socket.send(handshake.serialize_envelope())
            self._req_loop(socket)
        except KeyboardInterrupt:
            print("\nExit...")
            self.stop = True

    def prompt(self, func):
        self._PROMPT_FUNCTIONS.append(func)
        return func

    def math(self, func):
        self._MATH_FUNCTIONS.append(func)
        return func

    def _req_loop(self, socket):
        while not self.stop:
            try:
                msg_bytes = socket.recv()
                message = parse_message(msg_bytes)
                if isinstance(message, ImagePromptMsg):
                    func = self._PROMPT_FUNCTIONS[0]
                    result = func(message)

                socket.send(result.serialize_envelope())
            except MothMessageError as err:
                print("Failed to parse this message: ", err)


def main():
    print(
        """
    ███╗░░░███╗░█████╗░████████╗██╗░░██╗
    ████╗░████║██╔══██╗╚══██╔══╝██║░░██║
    ██╔████╔██║██║░░██║░░░██║░░░███████║
    ██║╚██╔╝██║██║░░██║░░░██║░░░██╔══██║
    ██║░╚═╝░██║╚█████╔╝░░░██║░░░██║░░██║
    ╚═╝░░░░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝
    """
    )
