class Arrayable:
    # Data
    # type: list
    __data = []

    # Return a sub-array that contains only the given keys.
    # param: keys
    # type: list
    # return: list
    def only(self, keys: list) -> list:
        arr = []
        for item in keys:
            arr[item] = self.__data[item]
        return arr

    # Make it compatible to work with php native array functions.
    # return: list
    def __call__(self) -> list:
        return self.__data

    # Get a data by key
    # param: key
    # type: str
    # return: mixed
    def get(self, key) -> any:
        return self.__data[key]

    # Assigns a value to the specified data
    # param: key
    # type: any
    # param: value
    # type: any
    # return: None
    def set(self, key, value) -> None:
        self.__data[key] = value

    # Whether or not data exists by key
    # param: key
    # type: any
    # return: bool
    def is_set(self, key) -> bool:
        return True if key in self.__data else False

    # Unsets a data by key
    # param: key
    # type: any
    def unset(self, key):
        self.__data.pop(key)

    # Assigns a value to the specified offset.
    # param: offset
    # type: str
    def offset_set(self, offset, value):
        if offset is None:
            self.__data.insert(value)
        else:
            self.__data[offset] = value

    # Unsets an offset.
    # param: offset
    # type: any
    def offset_unset(self, offset):
        if offset in self.__data:
            self.__data.pop(offset)

    # Returns the value at specified offset.
    # param: offset
    # type: any
    def offset_get(self, offset):
        return self.__data[offset] if offset in self.__data else None

    # Array representation of the object.
    # return: list
    def to_array(self) -> list:
        return self.__data

