from ..helpers.regex import recalculate_matched_words

class Constrained_Factor:
  def __init__(self, grid: list, selected_block: dict):
    self.neighbor_blocks = []
    self.grid = grid
    self.selected_block = selected_block
    self.selec_start_row = selected_block.get('start_spot')[0]
    self.selec_start_col = selected_block.get('start_spot')[1]
    self.selec_length = selected_block.get('length')

  def find_affected_neighbors(self, uncompleted_blocks: list):
    """ Find all the blocks affected by this current word selected """

    for curr_block in uncompleted_blocks:
      curr_start_row = curr_block.get('start_spot')[0]
      curr_start_col = curr_block.get('start_spot')[1]
      curr_length = curr_block.get('length')

      if self.selected_block.get('dimension') == 'across':
        if curr_block.get('dimension') == 'across': continue

        # Checking if block affected (current = across) / if one cell exists in a row:
        is_curr_row_affected = curr_start_row <= self.selec_start_row <= curr_start_row + curr_length - 1
        is_curr_col_affected = self.selec_start_col <= curr_start_col <= self.selec_start_col + self.selec_length - 1
      else:
        if curr_block.get('dimension') == 'down': continue

        # Checking if block affected (current = down) / if one cell exists in a col:
        is_curr_row_affected = self.selec_start_row <= curr_start_row <= self.selec_start_row + self.selec_length - 1
        is_curr_col_affected = curr_start_col <= self.selec_start_col <= curr_start_col + curr_length - 1

      if is_curr_row_affected and is_curr_col_affected:
        self.neighbor_blocks.append(curr_block.copy())

    # return self.neighbor_blocks
  
  def calc_constrained_factor(self):
    """
      - Find the sum of all neighbor cell matching words
      - Find also the minimum neighbor cell mathing words
    """
    total_words = 0
    min_cell_words = float("inf") # positive infinity number

    for curr_block in self.neighbor_blocks:
      curr_words = curr_block.get('match_words').copy()
      new_pattern = self.create_new_block_pattern(curr_block)

      # recalculate_matched_words (filter the previous)
      matched_words = recalculate_matched_words(new_pattern, curr_words)
      total_words += len(matched_words)

      if total_words > min_cell_words:
        min_cell_words = total_words
    
    return { "total_words": total_words, "min_cell_words": min_cell_words }
  
  def adjust_filtered_words_in_neighbors(self):
    filtered_neighbors = []

    for block in self.neighbor_blocks:
      curr_words = block.get('match_words').copy()
      new_pattern = self.create_new_block_pattern(block)

      curr_block = {
        "start_spot": block.get('start_spot'),
        "id": block.get('id'),
        "length": block.get('length'),
        "dimension": block.get('dimension'),
        "pattern": new_pattern,
        "match_words": recalculate_matched_words(new_pattern, curr_words)
      }
      curr_block['w_match_size'] = len(curr_block.get('match_words'))
      
      filtered_neighbors.append(curr_block)

    return filtered_neighbors

  def create_new_block_pattern(self, curr_block: dict):
    curr_start_row = curr_block.get('start_spot')[0]
    curr_start_col = curr_block.get('start_spot')[1]

    if self.selected_block.get('dimension') == 'across':
      letter_index = self.selec_start_row - curr_start_row
      cell_letter = self.grid[self.selec_start_row][curr_start_col]
    else:
      letter_index = self.selec_start_col - curr_start_col
      cell_letter = self.grid[curr_start_row][self.selec_start_col]

    cell_letter = cell_letter if cell_letter else '?'

    # change this index of current block's pattern
    pattern = curr_block.get('pattern')
    new_pattern = pattern[:letter_index] + cell_letter.lower() + pattern[letter_index + 1:]

    return new_pattern
  