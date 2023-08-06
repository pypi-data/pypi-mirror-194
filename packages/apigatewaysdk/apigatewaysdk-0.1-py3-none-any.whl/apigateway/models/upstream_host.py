class UpstreamHost(object):
    def __init__(self, host=None, port=None, weight=None):
        self._host = None
        self._port = None
        self._weight = None

        if host:
            self._host = host
        if port:
            self._port = port
        if weight:
            self._weight = weight

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def weight(self):
        return self._weight

    @host.setter
    def host(self, host):
        self._host = host

    @port.setter
    def port(self, port):
        self._port = port

    @weight.setter
    def weight(self, weight):
        self._weight = weight






