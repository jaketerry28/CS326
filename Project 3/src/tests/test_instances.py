# test_instances.py

from csp.map_coloring_instance import*
from csp.sudoku_instance import*

def test_map_instance_different_colors_constraint():
    red = map_colors[0]
    for region1 in map_variables:
        for region2 in map_neighbors:
            
            if region2 == region1:
                continue
            
            # neighbors conflict with same colors
            elif region2 in map_neighbors[region1]:
                assert not different_colors_constraint(region1, red, region2, red )
            
            # not neighbhors so no conflict with same color
            else:
                assert different_colors_constraint(region1, red, region2, red )




def test_sudoku_instance_constraints():
    for cell1 in sudoku_variables:
        for cell2 in sudoku_variables:
            
            if cell2 == cell1:
                continue
            
            # neighbors conflict with same values
            elif cell2 in sudoku_neighbors[cell1]:
                assert not different_values_constraint(cell1, 5, cell2, 5)
            
            # not neighbhors so no conflict with same value
            else:
                assert different_values_constraint(cell1, 5, cell2, 5)