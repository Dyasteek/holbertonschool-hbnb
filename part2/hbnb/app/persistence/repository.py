class Repository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Get an object by its ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Get all objects in the repository"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object with new data"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object from the repository"""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute value"""
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
