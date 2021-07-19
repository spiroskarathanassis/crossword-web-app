from ..helpers.regex import find_relative_word

class Grid:
  def __init__(self, length):
    self.grid_length = length
    self.grid = self.init_grid()
    
  def init_grid(self):
    grid = []
    for i in range(self.grid_length):
      grid.append([''] * self.grid_length)

    return grid
  
  def set_grid(self, grid):
    self.grid = grid
  
  def get_grid(self):
    return self.grid
  
  def put_word_in_block(self, block: dict, word: str):
    if not(word): return
    if block.get('is_relaxed'):
      word = find_relative_word(word, block.get('pattern'))
    elif block.get('is_reversed'):
      word = word[::-1]

    block_length = block.get('length')
    spot_row = block.get('start_spot')[0]
    spot_col = block.get('start_spot')[1]

    word = word.upper()
    index = 0

    if block.get('dimension') == 'across':
      for curr_col in range(spot_col, spot_col + block_length):
        self.grid[spot_row][curr_col] = word[index]
        index += 1
    else:
      for curr_row in range(spot_row, spot_row + block_length):
        self.grid[curr_row][spot_col] = word[index]
        index += 1
  
  def remove_word_from_block(self, block: dict):
    spot_row = block.get('start_spot')[0]
    spot_col = block.get('start_spot')[1]
    block_length = block.get('length')
    pattern = block.get('pattern')

    if block.get('dimension') == 'across':
      for i, curr_col in enumerate(range(spot_col, spot_col + block_length)):
        self.grid[spot_row][curr_col] = pattern[i].upper() if pattern[i] != '?' else ''
        i += 1
    else:
      for i, curr_row in enumerate(range(spot_row, spot_row + block_length)):
        self.grid[curr_row][spot_col] = pattern[i].upper() if pattern[i] != '?' else ''
        i += 1