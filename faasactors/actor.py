from .channel import Channel
import inspect


class Actor(object):

    def __init__(self, name, klass):
        self._name = name
        self._class = klass
        self._channel = Channel(name)
        self.obj = None

    def create(self, *args, **kwargs):
        self.obj = self._class(*args, **kwargs)

    def load(self):
        pass

    def dump(self):
        pass


class Proxy(object):

    def __init__(self, actor: Actor):
        self.__actor_name = actor._name
        self.__channel = actor._channel

        methods = inspect.getmembers(actor.obj, inspect.ismethod)
        for method in [meth[0] for meth in methods]:
            setattr(self, method, TellWrapper(self.__channel, method, self.__actor_name))


class TellWrapper(object):

    def __init__(self, channel, method, actor_name):
        self.__channel = channel
        self.__method = method
        self.__target = actor_name

    def __call__(self, *args, **kwargs):
        #  SENDING MESSAGE TELL
        msg = {"METHOD": self.__method, "PARAMS": (args, kwargs),
               "TO": self.__target}
        self.__channel.send(msg)
