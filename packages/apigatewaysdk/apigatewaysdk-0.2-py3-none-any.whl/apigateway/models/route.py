class Route(object):
    def __init__(self, name=None, upstream_id=None, description=None, paths=None, methods=None, hosts=None, plugins=None):
        self._name = None
        self._upstream_id = None
        self._description = None
        self.paths = None
        self.methods = None
        self.hosts = None
        self.plugins = None

        if name:
            self._name = name
        if upstream_id:
            self._upstream_id = upstream_id
        if description:
            self._description = description
        if paths:
            self._paths = paths
        if methods:
            self._methods = methods
        if hosts:
            self._hosts = hosts
        if plugins != None:
            self._plugins = plugins

    @property
    def name(self):
        return self._name

    @property
    def upstream_id(self):
        return self._upstream_id

    @property
    def description(self):
        return self._description

    @property
    def paths(self):
        return self._paths

    @property
    def methods(self):
        return self._methods

    @property
    def hosts(self):
        return self._hosts

    @property
    def plugins(self):
        return self._plugins

    @name.setter
    def name(self, name):
        self._name = name

    @upstream_id.setter
    def upstream_id(self, upstream_id):
        self._upstream_id = upstream_id

    @description.setter
    def description(self, description):
        self._description = description

    @paths.setter
    def paths(self, paths):
        self._paths = paths

    @methods.setter
    def methods(self, methods):
        self._methods = methods

    @hosts.setter
    def hosts(self, hosts):
        self._hosts = hosts

    @plugins.setter
    def plugins(self, plugins):
        self._plugins = plugins



