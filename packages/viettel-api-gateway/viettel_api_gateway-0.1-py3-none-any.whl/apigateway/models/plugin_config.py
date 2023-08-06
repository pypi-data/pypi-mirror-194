class PluginConfig(object):
    def __init__(self, id=None, plugins=None, description=None, labels=None):
        self._id = None
        self._plugins = None
        self._description = None
        self._labels = None

        if id:
            self._id = id

        if plugins != None:
            self._plugins = plugins

        if description:
            self._description = description

        if labels:
            self._labels = labels

    @property
    def id(self):
        return self._id

    @property
    def plugins(self):
        return self._plugins

    @property
    def description(self):
        return self._description

    @property
    def labels(self):
        return self._labels

    @id.setter
    def id(self, id):
        self._id = id

    @plugins.setter
    def plugins(self, plugins):
        self._plugins = plugins

    @description.setter
    def description(self, description):
        self._description = description

    @labels.setter
    def labels(self, labels):
        self._labels = labels



