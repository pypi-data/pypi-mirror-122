import pika

from iuye_utils import config_utils

rabbitmq_config = config_utils.get_config_data('rabbitmq')
rabbitmq_host = rabbitmq_config['host']
rabbitmq_port = rabbitmq_config['port']


class RabbitMqHelper():
    def __init__(self):
        self._default_connection = None

    def get_default_connection(self):
        if self._default_connection is None or self._default_connection.is_closed:
            self._default_connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
        return self._default_connection


mq_helper = RabbitMqHelper()


def get_default_connection():
    return mq_helper.get_default_connection()


def get_new_connection(self, host=None, port=None):
    if host is None:
        _host = rabbitmq_host
    else:
        _host = host
    if port is None:
        _port = rabbitmq_port
    else:
        _port = port
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=_host, port=_port))
    return connection
