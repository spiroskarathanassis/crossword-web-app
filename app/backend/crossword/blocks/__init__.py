"""
  example {
    "start_spot": (0, 1),
    "id": 0,
    "length": 4,
    "dimension": "across",

    "pattern": '????',
    "match_words": ['area', 'ping', ...],
    "w_match_size": 1200,

    "is_relaxed": False
  }
"""

class Block:
  def __init__(self, grid: list):
    self.grid = grid
    self.grid_length = len(grid)
    self.block_id = 0
    self.across = [] #list of dictionaries {(start_row, start_col), length, across}
    self.down = []
    self.find_across()
    self.find_down()
  
  def find_across(self):
    is_start = False
    is_found_empty_cell = False
    count = 0

    for row in range(0, self.grid_length):
      for col in range(0, self.grid_length):
        is_saved_spot = False
        
        if self.grid[row][col] != '#':
          count += 1

          if col == (self.grid_length - 1):
            is_found_empty_cell = True
            is_saved_spot = True
          elif not(is_found_empty_cell):
            is_start = True
            is_found_empty_cell = True
            start_row = row
            start_col = col
        elif is_start and is_found_empty_cell: # black
          is_saved_spot = True
      
        if is_saved_spot: 
          self.across.append({
            "id": self.block_id,
            "start_spot": (start_row, start_col), # start dimension
            "length": count,
            "dimension": "across"
          })
          
          self.block_id += 1
          is_found_empty_cell = False
          count = 0

  def find_down(self):
    is_start = False
    is_found_empty_cell = False
    count = 0

    for col in range(0, self.grid_length):
      for row in range(0, self.grid_length):
        is_saved_spot = False
        
        if self.grid[row][col] != '#':
          count += 1

          if row == (self.grid_length - 1):
            is_found_empty_cell = True
            is_saved_spot = True
          elif not(is_found_empty_cell):
            is_start = True
            is_found_empty_cell = True
            start_row = row
            start_col = col
        elif is_start and is_found_empty_cell: # black
          is_saved_spot = True
      
        if is_saved_spot: 
          self.down.append({
            "id": self.block_id,
            "start_spot": (start_row, start_col), # start dimension
            "length": count,
            "dimension": "down"
          })

          self.block_id += 1
          is_found_empty_cell = False
          count = 0
  
  def keep_uncompleted_blocks(self, theme_blocks: list):
    grid_blocks = self.across + self.down

    for block in grid_blocks:
      for themed in theme_blocks:
        if (
          block.get('start_spot') == themed.get('start_spot')
          and block.get('dimension') == themed.get('dimension')
          and block.get('length') == themed.get('length')
        ):
          grid_blocks.remove(block)

    return grid_blocks
  
  @staticmethod
  def adjust_current_block_new_words(block: dict, words_matched: list):
    block['match_words'] = words_matched
    block['w_match_size'] = len(words_matched)