from abc import ABC, abstractmethod

class KlatApiABC(ABC):
    """Abstract class declaring the basic properties any inherited API should implement"""

    @property
    @abstractmethod
    def connected(self) -> bool:
        """
            Checks if instance is connected
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def nick(self) -> str:
        """Unique nickname for API instance in network"""
        raise NotImplementedError

    # Handlers to be overridden
    @abstractmethod
    def handle_incoming_shout(self, *args, **kwargs):
        """
        This function should be overridden to handle incoming messages
        """
        pass

    # Socket Listeners
    def _on_connect(self):
        """
        Handler for socket connection
        """
        LOG.info("Chat Server Socket Connected!")

    @staticmethod
    def _on_disconnect():
        """
        Handler for socket disconnection
        """
        # self.connected = False
        LOG.warning("Chat Server Socket Disconnected!")

    @staticmethod
    def _on_reconnect():
        """
        Handler for socket reconnection
        """
        # self.connected = True
        LOG.warning("SocketIO Reconnected")

    @abstractmethod
    def _on_user_message(self, *args):
        """
        Handler for "user message" (incoming shouts)
        :param args: Socket Arguments
        """
        pass

    @abstractmethod
    def _send_shout(self, *args, **kwargs):
        """
            Internal function that sends a shout into the conversation
        """
        pass

    @abstractmethod
    def _start_connection(self):
        """
        Initializes a new connection to the Klat server
        """
        pass

    @abstractmethod
    def _stop_connection(self):
        """
        Initializes a new connection to the Klat server
        """
        pass

    @abstractmethod
    def _setup_listeners(self):
        """
        Starts all Klat event listeners
        """
        pass
