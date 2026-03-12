# test_constraints.py

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
    board = [["5","3",".",".","7",".",".",".","."],
             ["6",".",".","1","9","5",".",".","."],
             [".","9","8",".",".",".",".","6","."],
             ["8",".",".",".","6",".",".",".","3"],
             ["4",".",".","8",".","3",".",".","1"],
             ["7",".",".",".","2",".",".",".","6"],
             [".","6",".",".",".",".","2","8","."],
             [".",".",".","4","1","9",".",".","5"],
             [".",".",".",".","8",".",".","7","9"]]
    
    board2 = [["8","3",".",".","7",".",".",".","."],
              ["6",".",".","1","9","5",".",".","."],
              [".","9","8",".",".",".",".","6","."],
              ["8",".",".",".","6",".",".",".","3"],
              ["4",".",".","8",".","3",".",".","1"],
              ["7",".",".",".","2",".",".",".","6"],
              [".","6",".",".",".",".","2","8","."],
              [".",".",".","4","1","9",".",".","5"],
              [".",".",".",".","8",".",".","7","9"]]
    
    assert is_different_constraint(board)
    assert not is_different_constraint(board2)
