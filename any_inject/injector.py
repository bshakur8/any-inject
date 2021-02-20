from functools import wraps
from multiprocessing import RLock as processRlock
from threading import RLock as threadingRlock


def safe_guard(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.multiprocess_lock, self.threading_lock:
            return func(self, *args, **kwargs)

    return wrapper


def guard_funcs(decorator):
    def wrapper(cls):
        for attr, val in cls.__dict__.items():
            if callable(val) and not attr.startswith("__"):
                setattr(cls, attr, decorator(val))
        return cls

    return wrapper


@guard_funcs(safe_guard)
class InjectorCache:
    """
    Injector that register any Class or Object and can be extracted anywhere by calling injector 'get'
    """
    __slots__ = ('multiprocess_lock', 'threading_lock', '_classes', '_instances')

    def __init__(self):
        self.multiprocess_lock = processRlock()
        self.threading_lock = threadingRlock()
        self._classes = {}
        self._instances = {}

    def register_class(self, name, register_type):
        assert type(register_type) == type
        self._classes[name] = register_type

    def register_instance(self, name, instance):
        self._instances[name] = instance

    def is_registered(self, name):
        return any([name in self._classes, name in self._instances])

    def get_class(self, name):
        return self._classes.get(name)

    def unregister_instance(self, name):
        self._instances.pop(name, None)

    def unregister(self, name):
        self._classes.pop(name, None)

    def create(self, *, name, **kwargs):
        klass = self._classes.get(name)
        if not klass:
            raise TypeError(f'Class {name} is not part of {len(self._classes)} registered types {list(self._classes)}')
        return klass(**kwargs)

    def get_instance(self, name):
        return self._instances.get(name, None)

    def get_all_instances(self):
        return self._instances

    def get_all_classes(self):
        return self._classes


# # Singleton
# Injector = InjectorCache()
