from looqbox.class_loader.class_loader import ClassLoader
import json
import os

looqObjects_configuration_file = open(os.path.join(os.path.dirname(__file__), "..",
                                                   "configuration", "LooqObjects_path.json"))

class_paths = json.load(looqObjects_configuration_file)


class LazyLoad:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return ClassLoader(self.function.__name__, class_paths[self.function.__name__]).call_class(*args, **kwargs)

    def __instancecheck__(self, instance):
        self_class = ClassLoader(self.function.__name__, class_paths[self.function.__name__]).load_class()
        return isinstance(instance, self_class)
