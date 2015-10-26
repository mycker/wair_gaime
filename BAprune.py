from copy import deepcopy
import war_game_main

def ba_prune(orig_col, orig_en, cur_color, other_color, board, max_depth=3, cur_depth = 0, next_loc = None, alpha = [-100000, None], beta = [100000, None]):
    # types: string, string, string, string, class, int, int, array[2], array[2], array [2]
    # goal is to keep going until cur_depth is greater than max depth and then return location after pruning
    global nodes_searched = 0
    copied_board = deepcopy(board)
    nodes_searched += 1
    if cur_depth == 0:
        nodes_searched = 1
        # team to go first is blue so it will be the "max"
        if cur_color == orig_col:
            ret_val = max(ba_prune(orig_col, orig_en, cur_color, other_color, copied_board, max_depth, cur_depth+1, n_loc) for n_loc in copied_board.open)
            return ret_val
        else:
            ret_val = min(ba_prune(orig_col, orig_en, cur_color, other_color, copied_board, max_depth, cur_depth+1, n_loc) for n_loc in copied_board.open)
            return ret_val
    # give theoretical points for further calculating assuming paradrop then check for neighbors for blitz (we're checking every spots paradrop)
    war_game_main.__paradrop(copied_board, next_loc, cur_color)
    # now blitz
    height = len(copied_board.board)
    width = len(copied_board.board[0])
    neighbors = [(next_loc[0]+1, next_loc[1]), (next_loc[0]-1, next_loc[1]), (next_loc[0], next_loc[1]+1), (next_loc[0], next_loc[1]-1)]
    for neighbor in neighbors:
        row = neighbor[0]
        col = neighbor[1]
        if ~((0 <= row < height) and (0 <= col < width)):
            neighbors.remove(neighbor)
        if copied_board.board[row][col]['team'] == other_color:
            # change values and team color for blitzed spots
            value = copied_board.board[row][col]['value']
            copied_board.score[cur_color] += value
            copied_board.score[other_color] -= value
            copied_board.board[row][col]['team'] = cur_color

    # returns the alpha/beta, and location when hitting the bottom
    if cur_depth >= max_depth or len(copied_board.open) == 0:
        return [copied_board.score[orig_col] - copied_board.score[orig_en], ]
    else:
        if cur_color != orig_col:
            for next in copied_board.open:
                alpha = max(ba_prune(orig_col, orig_en, cur_color, other_color, copied_board, max_depth, cur_depth+1, next, alpha, beta))
                if beta[0] <= alpha[0]:
                    #prune
                    break
            alpha[1] = next_loc
            return alpha
        else:
            for next in copied_board.open:
                beta = min(ba_prune(orig_col, orig_en, cur_color, other_color, copied_board, max_depth, cur_depth+1, next, alpha, beta))
                if beta[0] <= alpha[0]:
                    #prune
                    break
            beta[1] = next_loc
            return beta

