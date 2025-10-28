from .facade import HBnBFacade

# Global facade instance
_facade_instance = None

def get_facade():
    global _facade_instance
    if _facade_instance is None:
        _facade_instance = HBnBFacade()
    return _facade_instance

facade = get_facade()
