from ..fill_strategy.constrained_factor import Constrained_Factor

class Neighbor:
  def __init__(self):
    self.uncompleted_blocks = []

  def set_blocks(self, uncompleted_blocks: list):
    self.uncompleted_blocks = uncompleted_blocks

  def is_parent_neighbor_of_child(self, parent_block: dict, child_block: dict):
    child_row = child_block.get('start_spot')[0]
    child_col = child_block.get('start_spot')[1]
    child_length = child_block.get('length')

    for curr_block in self.uncompleted_blocks:
      if curr_block.get('id') != parent_block.get('id'): 
        continue

      curr_start_row = curr_block.get('start_spot')[0]
      curr_start_col = curr_block.get('start_spot')[1]
      curr_length = curr_block.get('length')

      if child_block.get('dimension') == 'across':
        if curr_block.get('dimension') == 'across': continue

        # Checking if block affected (current = across) / if one cell exists in a row:
        is_curr_row_affected = curr_start_row <= child_row <= curr_start_row + curr_length - 1
        is_curr_col_affected = child_col <= curr_start_col <= child_col + child_length - 1
      else:
        if curr_block.get('dimension') == 'down': continue

        # Checking if block affected (current = down) / if one cell exists in a col:
        is_curr_row_affected = child_row <= curr_start_row <= child_row + child_length - 1
        is_curr_col_affected = curr_start_col <= child_col <= curr_start_col + curr_length - 1

      if (is_curr_row_affected and is_curr_col_affected):
        return True
    
    return False

  @staticmethod
  def adjust_neighbor_by_most_constrained(
    pick_strategy: object, 
    cross_grid: object,
    uncompleted_blocks: list, 
    choosen_block: dict, 
    choosen_word: str,
  ):
    constrained_factor = Constrained_Factor(cross_grid.grid, choosen_block.copy())
    constrained_factor.find_affected_neighbors(uncompleted_blocks)
    # print('Affected blocks -', len(affected_neighbor_blocks))

    # --------- Choose the best current word choice by biggest sum of neighbors match ---------  #
    next_choosed_word = choosen_word
    max_neighbor_words_size = 0
    curr_min_neighbor_match = 0
    max_compare_words = 10

    while max_compare_words > 0:
      cross_grid.put_word_in_block(choosen_block, next_choosed_word)
      factor_result = constrained_factor.calc_constrained_factor()
      sum_neighbor_words_size = factor_result.get('total_words')
      min_neighbor_words = factor_result.get('min_cell_words')

      # condition pass: if has bigger sum of words matching and smaller of minimum neighbor words size
      if (max_neighbor_words_size < sum_neighbor_words_size) and (curr_min_neighbor_match < min_neighbor_words):
        max_neighbor_words_size = sum_neighbor_words_size
        curr_min_neighbor_match = min_neighbor_words
        choosen_word = next_choosed_word
      
      next_choosed_word = pick_strategy.choose_next_scrabble_word_selected(next_choosed_word)
      if not(next_choosed_word): break
      
      max_compare_words -= 1
    # --------- End ---------  #
    
    cross_grid.put_word_in_block(choosen_block, choosen_word)
    neighbor_blocks = constrained_factor.adjust_filtered_words_in_neighbors()
    
    # map neigbor blocks into uncompleted
    for main_block in uncompleted_blocks:
      for neighbor in neighbor_blocks:
        if neighbor.get('id') == main_block.get('id'):
          for key, value in main_block.items():
            if key in ['pattern', 'match_words', 'w_match_size']:
              main_block[key] = neighbor.get(key)
  
    return uncompleted_blocks