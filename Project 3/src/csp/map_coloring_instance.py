# map_coloring_instance.py

"""
Defines variables, domains, neighbors, constraints for a map coloring CSP instance.

Variables: Each region on the map is a variable.
Domains: red, green, blue
Constraints: No two neighboring regions can have the same color.

"""

map_colors = ["Red", "Green", "Blue"]

map_variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]

map_domains = {var: map_colors[:] for var in map_variables}

map_neighbors = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Q"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V": ["SA", "NSW"],
    "T": []
}


def different_colors_constraint(region1: str, color1: str, region2: str, color2: str) -> bool:
    if region2 in map_neighbors[region1] and region2 != region1:
        return color1 != color2
    return True  # No constraint if not neighbors


