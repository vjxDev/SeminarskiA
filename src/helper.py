def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def rgb_to_hex(colortuple: tuple[int, int, int]):
    return '#' + ''.join(f'{i:02X}' for i in colortuple)
