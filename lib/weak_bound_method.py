import weakref


class WeakBoundMethod:
    """ Converts a bound method instance 
        of a class into a weak reference.
    """

    def __init__(self, meth, eventcls, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._self = weakref.ref(meth.__self__)
        self._func = meth.__func__
        self.eventcls = eventcls


    def __call__(self, *args, **kwargs):
        
        if self._args or self._kwargs:
            args = self._args
            kwargs = self._kwargs

        if not self._self() is None:
            self._func(self._self(), *args, **kwargs)

        else:  
            from src.controller.event_dispatcher import EventDispatcher as Ed
            Ed.remove(self.eventcls, self)


    def __eq__(self, other):
        try:
            return self._func == other.__func__ and self._self == weakref.ref(other.__self__)
        except:
            return self._func == other._func and self._self == other._self