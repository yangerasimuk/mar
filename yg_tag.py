import re
from legacy_constant import *


class YgTag:
    def __init__(self, string: str):
        self.source = string
        self.target = re.sub(r"[\r\n\t]+", " ", string).strip()

    def __str__(self):
        return self.target

    def is_key_value(self) -> bool:
        # [uuid]:a8a34650-2653-4e62-8886-a94f09bce70f
        if re.match(r"\[.+]:.+", self.target) is None:
            return False
        else:
            return True

    def key_if_kvo(self):
        if not self.is_key_value():
            return None

        try:
            index = self.target.index("]:")
            if index < 0:
                return None
            key = self.target[1:index]
            return key
        except ValueError:
            return None

    def value_if_kvo(self):
        if not self.is_key_value():
            return None

        try:
            index = self.target.index("]:")
            if index < 0:
                return None
            value = self.target[index + 2:]
            return value
        except ValueError:
            return None

    def identifiable_by_uuid(self) -> bool:
        if not self.is_key_value():
            return False

        key = self.key_if_kvo()
        if not key or key != Constant.TAG_KEY_SYSTEM_UUID:
            return False

        return True
