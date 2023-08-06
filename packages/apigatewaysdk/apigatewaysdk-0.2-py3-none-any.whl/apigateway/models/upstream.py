class Upstream(object):
    def __init__(self, name=None, description=None, scheme=None, type=None, retries=None, retry_timeout=None,
                 connect_timeout=None, send_timeout=None, read_timeout=None, host_list=None):
        self._name = None
        self._api = None
        self._description = None
        self._scheme = None
        self._type = None
        self._retries = None
        self._retry_timeout = None
        self._connect_timeout = None
        self._send_timeout = None
        self._read_timeout = None
        self._host_list = None

        if name:
            self._name = name
        if description:
            self._description = description
        if scheme:
            self._scheme = scheme
        if type:
            self._type = type
        if retries:
            self._retries = retries
        if retry_timeout:
            self._retry_timeout = retry_timeout
        if connect_timeout:
            self._connect_timeout = connect_timeout
        if send_timeout:
            self._send_timeout = send_timeout
        if read_timeout:
            self._read_timeout = read_timeout
        if host_list != None:
            self._host_list = host_list

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def scheme(self):
        return self._scheme

    @property
    def type(self):
        return self._type

    @property
    def retries(self):
        return self._retries

    @property
    def retry_timeout(self):
        return self._retry_timeout

    @property
    def connect_timeout(self):
        return self._connect_timeout

    @property
    def send_timeout(self):
        return self._send_timeout

    @property
    def read_timeout(self):
        return self._read_timeout

    @property
    def host_list(self):
        return self._host_list

    @name.setter
    def name(self, name):
        self._name = name

    @description.setter
    def description(self, description):
        self._description = description

    @scheme.setter
    def scheme(self, scheme):
        self._scheme = scheme

    @type.setter
    def type(self, type):
        self._type = type

    @retries.setter
    def retries(self, retries):
        self._retries = retries

    @retry_timeout.setter
    def retry_timeout(self, retry_timeout):
        self._retry_timeout = retry_timeout

    @connect_timeout.setter
    def connect_timeout(self, connect_timeout):
        self._connect_timeout = connect_timeout

    @send_timeout.setter
    def send_timeout(self, send_timeout):
        self._send_timeout = send_timeout

    @read_timeout.setter
    def read_timeout(self, read_timeout):
        self._read_timeout = read_timeout

    @host_list.setter
    def host_list(self, host_list):
        self._host_list = host_list
