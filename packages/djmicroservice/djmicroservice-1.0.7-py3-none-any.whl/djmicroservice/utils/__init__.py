from .objectid import ObjectID,create_objectid


def import_object(name):
        mm = name.split('.')
        m = mm.pop() 
        return getattr(__import__('.'.join(mm),fromlist=[m]),m)  