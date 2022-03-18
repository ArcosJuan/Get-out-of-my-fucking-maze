from lib.weak_bound_method import WeakBoundMethod as Wbm


class EventDispatcher:
    """ Handles the sending of events 
        and their subscription
    """

    # Contains event classes and the object method 
    # subscribed to said event.
    listeners = dict()

    @classmethod
    def add(cls, eventcls, listener):
        """ Suscribes a listener to an specific Event class.
            Receives:
                eventcls:<Event.__class__>
                listener:<BoundMethod>
        """

        listener = Wbm(listener)

        # If the event is not in the dictionary, 
        # it is added and subscribed to by the listener.
        cls.listeners.setdefault(eventcls, list()).append(listener)


    @classmethod
    def remove(cls, eventcls, listener):
        for l in cls.listeners[eventcls]:
            if l == listener:
                cls.listeners[eventcls].remove(l)


    @classmethod
    def post(cls, event):
        """ Sends an event instance to their suscribers.
                Receives:
                    event:<Event>
        """

        if cls.listeners.get(event.__class__, False):
            for listener in cls.listeners[event.__class__]:
                listener(event)