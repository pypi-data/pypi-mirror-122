from datetime import datetime

from iuye_utils import rabbitmq_utils


def m1(message='hello'):
    connection = rabbitmq_utils.get_default_connection()
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='task_queue', body=message)
    print(" [x] Sent %r" % message)
    print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    connection.close()


if __name__ == '__main__':
    m1('abc')
    m1('abcd')
