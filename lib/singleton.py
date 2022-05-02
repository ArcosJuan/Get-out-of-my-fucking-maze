
class Singleton(type):
    """ A metaclass that creates a Singleton base class when called.
        
        Code Author: https://stackoverflow.com/users/500584/agf 
        From: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]