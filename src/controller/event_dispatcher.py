from lib.weak_bound_method import WeakBoundMethod as Wbm


class EventDispatcher:
    """ Handles the sending of events 
        and their subscription
    """

    # Contains event classes and the object method 
    # subscribed to said event.
    listeners = dict()
    exclusive_listeners = dict() # {event: [listener]}

    @classmethod
    def add(cls, eventcls, listener):
        """ Suscribes a listener to an specific Event class.
            Receives:
                eventcls:<Event.__class__>
                listener:<BoundMethod>
        """

        listener = Wbm(listener, eventcls)

        # If the event is not in the dictionary, 
        # it is added and subscribed to by the listener.
        cls.listeners.setdefault(eventcls, list()).append(listener)


    @classmethod
    def remove(cls, eventcls, listener):
        cls.listeners[eventcls].remove(listener)


    @classmethod
    def post(cls, event):
        """ Sends an event instance to their suscribers.
                Receives:
                    event:<Event>
        """

        if cls.listeners.get(event.__class__, False):
            if event.__class__ in cls.exclusive_listeners:
                el = cls.exclusive_listeners[event.__class__].copy()
                for listener in el:
                    listener(event)

            else:
                l = cls.listeners[event.__class__].copy()
                for listener in l:
                    listener(event)             


    @classmethod
    def add_exclusive_listener(cls, eventcls, listener):
        listener = Wbm(listener, eventcls)
        cls.exclusive_listeners.setdefault(eventcls, list()).append(listener)


    @classmethod
    def remove_exclusive_listener(cls, eventcls, listener):
        if eventcls in cls.exclusive_listeners:
            cls.exclusive_listeners[eventcls].remove(listener)
            if not cls.exclusive_listeners[eventcls]:
                cls.exclusive_listeners.pop(eventcls)
