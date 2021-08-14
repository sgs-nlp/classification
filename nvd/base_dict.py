class BaseDict:
    def __init__(self):
        self.base_dict = {}

    def set_item(self, key, value):
        key = str(key)
        self.base_dict[key] = value

    def get_item(self, key):
        key = str(key)
        if key in self.base_dict:
            return self.base_dict[key]
        return None
