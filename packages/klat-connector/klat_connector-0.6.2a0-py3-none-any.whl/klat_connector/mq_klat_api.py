import time

from .klat_api_abc import KlatApiABC
from neon_utils import LOG
from neon_utils.socket_utils import b64_to_dict, dict_to_b64
from neon_mq_connector import MQConnector


class KlatAPIMQ(KlatApiABC, MQConnector):

    def __init__(self, config: dict, service_name: str, vhost: str):
        super(MQConnector).__init__(config, service_name)
        self.current_conversations = set()
        self.vhost = vhost
        self.is_running = False

    @property
    def connected(self) -> bool:
        return self.is_running

    @property
    def nick(self) -> str:
        return self.service_name + '-' + self.service_id

    def handle_incoming_shout(self, message_data: dict):
        """Handles incoming request to chat bot"""
        LOG.info(f'Received message data: {message_data}')

    def _on_user_message(self, channel, method, _, body):
        body_data = b64_to_dict(body)
        if body_data.get('cid', None) in self.current_conversations \
                and (body_data.get('is_broadcast', False) or body_data.get('receiver', None) == self.nick):
            self.handle_incoming_shout(body_data)

    def _send_shout(self, queue_name: str, message_body: dict, exchange: str = ''):
        with self.create_mq_connection(vhost=self.vhost) as mq_connection:
            self.emit_mq_message(connection=mq_connection,
                                 queue=queue_name,
                                 request_data=dict_to_b64(data=message_body),
                                 exchange=exchange)

    def _start_connection(self):
        self.run_consumers()
        self._on_connect()

    def _stop_connection(self):
        self.stop_consumers()
        self._on_disconnect()

    def _on_connect(self):
        self._send_shout('connection', {'nick': self.nick,
                                        'service_name': self.service_name,
                                        'time': time.time()})
        self.is_running = True

    def _on_disconnect(self):
        self._send_shout('disconnection', {'nick': self.nick,
                                           'service_name': self.service_name,
                                           'time': time.time()})
        self.is_running = False

    def _on_reconnect(self):
        self._stop_connection()
        self._start_connection()

    def _setup_listeners(self):
        self.register_consumer('user message', self.vhost, 'user_message', self._on_user_message,
                               self.default_error_handler)
