from ..wn_queries import Wn_Queries

class Pattern:
  def __init__(self, block_list, is_respect_solver: bool = False):
    self.uncompleted_blocks = block_list
    self.saved_block_diff_patterns = {} # { '???': {size: 356, words: []} }
    self.is_respect_solver = is_respect_solver

  def adjust_block_pattern(self, grid: list):
    """Add to block dictionary:
    {
      'pattern': '??a?',
      'match_words': [],
      'w_match_size': 2345
    }
    """

    for count, block in enumerate(self.uncompleted_blocks):
      # Search block pattern
      block_pattern = ''
      available_words = []

      for i in range(0, block['length']):
        row = block.get('start_spot')[0]
        col = block.get('start_spot')[1]
        
        if (block['dimension'] == 'across'):
          block_pattern += grid[row][col + i] if grid[row][col + i] else '?'
        else:
          block_pattern += grid[row + i][col] if grid[row + i][col] else '?'
        block_pattern = block_pattern.lower()
        
      # Find all words matching the pattern
      if block_pattern in self.saved_block_diff_patterns:
        available_words = self.saved_block_diff_patterns[block_pattern].get('words')
        block_pattern_size = self.saved_block_diff_patterns[block_pattern].get('size')
      else:
        # query to database and extend uncompleted_blocks
        if self.is_respect_solver:
          available_words = Wn_Queries.get_total_match_words_by_pos_tag(block_pattern)
        else:
          available_words = Wn_Queries.get_total_match_words(block_pattern)
        block_pattern_size = len(available_words)
        self.saved_block_diff_patterns['block_pattern'] = {
          'size': len(available_words),
          'words': available_words
        }
      
      block['pattern'] = block_pattern # 'b??a?'
      block['w_match_size'] = block_pattern_size
      block['match_words'] = available_words

    return self.uncompleted_blocks
  
  def adjust_pattern_for_unmatching_blocks(grid: list, blocks: list):
    from ..helpers.regex import recalculate_matched_words
    
    for count, block in enumerate(blocks):
      block_pattern = ''

      for i in range(0, block.get('length')):
        row = block.get('start_spot')[0]
        col = block.get('start_spot')[1]
        
        if block.get('dimension') == 'across':
          grid_letter = grid[row][col + i]
        else:
          grid_letter = grid[row + i][col]

        block_pattern += grid_letter.lower() if grid_letter else '?'

      if block_pattern == block.get('pattern'):
        continue
      
      # Filter from past word list
      block['pattern'] = block_pattern # 'b??a?'
      block['match_words'] = recalculate_matched_words(block_pattern, block.get('match_words'))
      block['w_match_size'] = len(block.get('match_words'))

    return blocks
