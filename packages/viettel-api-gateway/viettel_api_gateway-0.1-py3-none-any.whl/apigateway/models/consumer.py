class Consumer(object):
    def __init__(self, username=None, description=None, plugins=None):
        self._username = None
        self._description = None
        self._plugins = None

        if username:
            self._username = username
        if description:
            self._description = description
        if plugins != None:
            self._plugins = plugins

    @property
    def username(self):
        return self._username

    @property
    def description(self):
        return self._description

    @property
    def plugins(self):
        return self._plugins

    @username.setter
    def username(self, username):
        self._username = username

    @description.setter
    def description(self, description):
        self._description = description

    @plugins.setter
    def plugins(self, plugins):
        self._plugins = plugins






