import socket
import time
from collections import defaultdict


class ClientError(Exception):
    pass


class Client:

    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        self.timeout = timeout

    def put(self, metric_name, metric_value, timestamp=None):
        if not timestamp:
            timestamp = str(int(time.time()))
        else:
            timestamp = str(timestamp)
        timestamp += '\n'
        metric_value = str(metric_value)

        message = ' '.join(['put', metric_name, metric_value, timestamp])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            sock.settimeout(self.timeout)
            sock.send(message.encode())
            data = sock.recv(1024).decode()

        if data == 'error\nwrong command\n\n':
            raise ClientError()

    def get(self, metric_name):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            sock.settimeout(self.timeout)
            key = 'get {}\n'.format(metric_name)
            sock.send(key.encode())
            data = sock.recv(1024).decode()

        if data == 'ok\n\n':
            return {}
        if data == 'error\nwrong command\n\n':
            raise ClientError()

        if 'ok\n' in data and '\n\n' in data:
            metric_items = data.lstrip('ok\n').rstrip('\n\n')
            metric_items = [x.split() for x in metric_items.split('\n')]
        else:
            raise ClientError()

        metric_dict = defaultdict(list)
        try:
            for key, metric, timestamp in metric_items:
                metric_dict[key].append((int(timestamp), float(metric)))
        except (ValueError, IndexError):
            raise ClientError()
        for k, v in metric_dict.items():
            v.sort(key=lambda x: x[0])
        return metric_dict
