from random import randrange

from ..blackbox import Blackbox
from ..grid import Grid

class Theme_Block:
  def __init__(self) -> None:
    self.current_tried_block = {}
  
  def choose_another_diff_length_across_block(self, grid: list, blackboxes: int, max_word_length: int):
    self.tried_theme_blocks = []
    self.availables_first_blocks = Theme_Block.find_across_theme_blocks(grid, blackboxes, max_word_length)
    return self.choose_another_same_length_across_block()

  def choose_another_same_length_across_block(self):
    new_block = {}

    if len(self.tried_theme_blocks) == 0:
      new_block = Theme_Block.choose_random_from_availables(self.availables_first_blocks)
    else:
      for block in self.availables_first_blocks:
        if not(block in self.tried_theme_blocks):
          new_block = block.copy()

    if new_block:
      self.tried_theme_blocks.append(new_block)
      self.current_tried_block = new_block.copy()

    return new_block

  @staticmethod
  def find_across_theme_blocks(grid: list, max_blacks: int, word_length: int) -> list:
    """ Returns available blocks """
    blackbox = Blackbox(grid)
    temp_grid = Grid(len(grid))
    temp_grid.set_grid(grid)

    availables_blocks = []
    block = {}
    temp_word = word_length * '-'
    
    col = 0
    row = 1 # between 2 and center - 1
    max_row = int(len(grid) / 2) - 1
    
    while row < max_row:
      block = {
        "start_spot": (row, col),
        "length": word_length,
        "dimension": "across",
        "pattern": word_length * '?'
      }

      temp_grid.put_word_in_block(block, temp_word)
      possible_blacks = blackbox.collect_black_availaibility()
      if 2 * len(possible_blacks) >= max_blacks:
        availables_blocks.append(block)
      
      temp_grid.remove_word_from_block(block)
      row += 1

    return availables_blocks
  
  @staticmethod
  def choose_random_from_availables(availables_blocks: list):
    if len(availables_blocks) > 0:
      random_index = randrange(len(availables_blocks))
      return availables_blocks[random_index].copy()
    
    return None

  @staticmethod
  def find_another_across_theme_block(grid: list, blackboxes: int, w_length: str) -> dict:
    availables = Theme_Block.find_across_theme_blocks(grid.copy(), blackboxes, w_length)
    new_block = Theme_Block.choose_random_from_availables(availables)

    while not(new_block):
      w_length -= 1
      if w_length < 3:
        print('Second theme block not found')
        return None
      
      # choose_theme_word_for_symmetric_blocks
      availables = Theme_Block.find_across_theme_blocks(grid.copy(), blackboxes, w_length)
      new_block = Theme_Block.choose_random_from_availables(availables)
    
    return new_block

  @staticmethod
  def set_centered_theme_block(choosen_word: str, grid_size: int) -> dict:
    center_spot = int((grid_size - 1) / 2)
    w_length = len(choosen_word)
    spot = (center_spot, center_spot - int((w_length - 1) / 2))
    
    return {
      "start_spot": spot,
      "length": w_length,
      "dimension": "across",
      "pattern": w_length * '?'
    }