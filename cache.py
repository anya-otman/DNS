import pickle
import time


class Cache:
    def __init__(self):
        self.data = dict()
        self.load_cache()

    def load_cache(self):
        try:
            with open("cache.txt", 'rb') as f:
                data = pickle.load(f)
                overdue_records = []
                for k, v in data.items():
                    if v[1] + v[2] <= time.time():
                        overdue_records.append(k)
                for k in overdue_records:
                    data.pop(k)
            print("Cache is loaded")
            self.data = data
        except EOFError:
            print("Cache is empty")

    def add(self, name, type, ttl, item):
        self.data[(name, type)] = (item, time.time(), ttl)
        self.caching()

    def caching(self):
        with open("cache.txt", 'wb') as f:
            pickle.dump(self.data, f)

    def get_record(self, key):
        if key in self.data:
            value = self.data[key]
            if value[1] + value[2] >= time.time():
                return value
        return None
