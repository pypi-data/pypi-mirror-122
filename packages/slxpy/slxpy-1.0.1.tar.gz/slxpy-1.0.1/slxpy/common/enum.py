from enum import Enum

class FieldMode(Enum):
    MODEL = 0
    PLAIN = 1
    PLAIN_ARRAY = 2
    STRUCT = 3
    STRUCT_ARRAY = 4
    # Other modes like pointer is currently unsupported
