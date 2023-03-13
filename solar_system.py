# coding: utf-8



class Corps:

    corpsTypes = ["Star", "Planet", "Moon"]

    def __init__(self, **kwargs):

        try:
            if kwargs["type"] not in self.corpsTypes:
                raise ValueError("{} is not a valid type of {}... ".format(kwargs["type"], type(self)))
            self._type = kwargs["type"]
        except KeyError:
            raise KeyError("A type must be provided to instantiate a {} object... ".format(type(self)))

        if "name" in kwargs:
            if not isinstance(kwargs["name"], str):
                raise TypeError("The name must be a string... ")
            self._name = kwargs["name"]
        else:
            self._name = None

        try:
            if not isinstance(kwargs["mass"], (int, float)):
                raise TypeError("The mass must either be an integer or a float... ")
            if kwargs["mass"] <= 0:
                raise ValueError("The mass must be positive... ")
            self._mass = kwargs["mass"]
        except KeyError:
            raise KeyError("A mass must be provided to instantiate a {} object... ".format(type(self)))

        try:
            if not isinstance(kwargs["radius"], (int, float)):
                raise TypeError("The radius must either be an integer or a float... ")
            if kwargs["radius"] <= 0:
                raise ValueError("The radius must be positive... ")
            self._radius = kwargs["radius"]
        except KeyError:
            raise KeyError("A radius must be provided to instantiate a {} object... ".format(type(self)))

        if "color" in kwargs:
            if not isinstance(kwargs["color"], tuple):
                raise TypeError("The color must be a tuple... ")
            if not len(kwargs["color"]) == 3:
                raise TypeError("The color must have three components... ")
            for c in kwargs["color"]:
                if not isinstance(c, int):
                    raise TypeError("The color components must be integers... ")
                if not c in range(256):
                    raise ValueError("The color components must be between 0 and 255... ")
            self._color = kwargs["color"]
        else:
            self._color = None
