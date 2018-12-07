# -*- coding: utf-8 -*-

class InstanceSingleton(type):
    _objects = {}

    def __call__(
        cls,
        ip,
        classes
    ):

        if ip not in InstanceSingleton._objects:
            InstanceSingleton._objects[ip] = (
                super(InstanceSingleton, cls).__call__(ip, classes)
            )

        return InstanceSingleton._objects[ip]

