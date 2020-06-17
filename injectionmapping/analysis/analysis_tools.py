from injectionmapping.misc.RSP_region_info import midline, RSP_info

a_p_midpoint = (RSP_info["z_min_um_left"] + RSP_info["z_max_um_left"]) / 2


def distance_from_midline(x_value, midline=midline):
    return abs(x_value - midline)


def distance_from_a_p_midpoint(value):
    return value - a_p_midpoint
