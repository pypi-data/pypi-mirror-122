""" Define Some Colors """


def hex_to_tuple(hex_str):
    return tuple(bytes.fromhex(hex_str))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# SPACE PALET
# https://coolors.co/1f2041-4b3f72-ffc857-119da4-19647e
SPACE_CADET = hex_to_tuple("1F2041")
CYBER_GRAPE = hex_to_tuple("4B3F72")
MAXIMUM_YELLOW_RED = hex_to_tuple("ffc857")
VIRIDIAN_GREEN = hex_to_tuple("119da4")
BLUE_SAPPHIRE = hex_to_tuple("19647E")
ELECTRIC_BLUE = hex_to_tuple("5AE6EE")
