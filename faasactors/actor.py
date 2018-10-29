import inspect
from types import FunctionType

from faasactors.channel import Channel
from faasactors.utils.database import create_actor_entry, load_actor, dump_actor


class Actor(object):

    def __init__(self, name, klass):
        self._name = name
        self._class = klass
        self._channel = Channel(name)
        self.obj = None

    def create(self, *args, **kwargs):
        self.obj = self._class(*args, **kwargs)
        create_actor_entry(self._name, self.obj)

    def load(self):
        self.obj = self._class()
        self.obj = load_actor(self._name, self.obj)

    def dump(self):
        dump_actor(self._name, self.obj)

    def invoke(self, method_name, args=(), kwargs={}):
        invoke = getattr(self.obj, method_name)
        invoke(*args, **kwargs)


class Proxy(object):

    def __init__(self, actor: Actor, repeat_message=0):
        self.actor_name = actor._name
        self.channel = actor._channel

        methods = inspect.getmembers(actor.obj, inspect.ismethod)
        for method in [meth[0] for meth in methods]:
            setattr(self, method,
                    TellWrapper(self.channel, method, self.actor_name, repeat_message))

class ProxyRef(object):
    def __init__(self, actor_name, klass):
        self.channel = Channel(actor_name)


        for method in dir(klass):
            if type(getattr(klass, method)) == FunctionType:
                setattr(self, method,
                        TellWrapper(self.channel, method, actor_name))

class TellWrapper(object):

    def __init__(self, channel, method, actor_name, times_repeated=0):
        self.__channel = channel
        self.__method = method
        self.__target = actor_name
        self.__times_repeated = times_repeated

    def __call__(self, *args, **kwargs):
        msg = {"METHOD": self.__method, "PARAMS": (args, kwargs),
               "TO": self.__target}
        #  SENDING MESSAGE TELL
        if self.__times_repeated > 0:
            self.__channel.sendRepeated(msg, self.__times_repeated)
        else:
            self.__channel.send(msg)
