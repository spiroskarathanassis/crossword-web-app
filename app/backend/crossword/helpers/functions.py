def deepcopy_blocks(block_list: list):
  new_blocks = []
  
  for block in block_list:
    new_block = {}
    for key, value in block.items():
      if key == 'match_words':
        new_block[key] = value.copy()
      else:
        new_block[key] = value
    
    new_blocks.append(new_block)
  
  return new_blocks

def sort_words_by_score(w_list: list):
  from .constants import SCRABBLE_RATE

  adjusted_word_list = []

  # adjust score by scrabble rate
  for word in w_list:
    score = 0
    for char in word:
      for rate_group in SCRABBLE_RATE:
        if char.upper() in rate_group.get('letters'):
          score += rate_group.get('score')
          break
    
    adjusted_word_list.append({
      "word": word,
      "score": score
    })
  
  return sorted(adjusted_word_list, key=lambda x: x.get('score'))

def find_and_adjust_symmetric_block(current_block: dict, grid_size: int):
  symmetric_block = {}

  prev_row = current_block.get('start_spot')[0]
  prev_col = current_block.get('start_spot')[1]
  block_length = current_block.get('length')

  symmetric_block = current_block.copy()
  new_spot = (grid_size - 1 - prev_row, grid_size - 1 - prev_col - (block_length - 1))
  symmetric_block["start_spot"] = new_spot

  return symmetric_block

def filter_crawled_words(words: list, pattern: str) -> list:
  from .regex import recalculate_matched_words

  pattern_words = [word for word in words if len(word) == len(pattern)]
  return recalculate_matched_words(pattern, pattern_words)