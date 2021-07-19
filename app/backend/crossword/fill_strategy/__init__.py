class Fill_Strategy:
  def choose_method_to_fill(self, method: str, block_list: list) -> dict:
    if len(block_list) == 0:
      return None

    switcher = {
      "FISRT_PATTERN_OCCURANCE": lambda: self.choose_first_word_pattern_occur(block_list),
      "RANDOM_PATTERN": lambda: self.choose_random_pattern(block_list),
      "SHORTEST_PATTERN": lambda: self.choose_shortest_or_longest_pattern(block_list, False),
      "LONGEST_PATTERN": lambda: self.choose_shortest_or_longest_pattern(block_list, True),
      "MOST_CONSTRAINED": lambda: self.most_constrained_pattern(block_list)
    }
    switch_res = switcher.get(method, None)
    
    # EnvironmentError(method, 'Error fill method, is not accepted')
    return None if switch_res == None else switch_res()
  
  def choose_first_word_pattern_occur(self, b_list: list) -> dict:
    print("First pattern selected")
    return b_list[0]

  def choose_random_pattern(self, b_list: list) -> dict:
    from random import randrange

    random_number = randrange(0, len(b_list))
    return b_list[random_number]
  
  def choose_shortest_or_longest_pattern(self, b_list: list, is_longest: bool) -> dict:
    min_length_blocks = []

    # sort list ascending by length
    # if is longest method, make descending sort
    sorted_b_list = sorted(b_list, key=lambda x: x['length'], reverse=is_longest)
    min_length_block = sorted_b_list[0]['length']

    for w in sorted_b_list:
      if w['length'] != min_length_block:
        break

      min_length_blocks.append(w)

    if len(min_length_blocks) > 1:
      return self.choose_random_pattern(min_length_blocks)

    return min_length_blocks[0]
  
  def most_constrained_pattern(self, b_list: list) -> dict:
    '''Is the way that affects less the rest uncompleted words cells'''
    min_length_match_patterns = []

    # sort ascending b_list by w_match_size of every block
    sorted_b_list = sorted(b_list, key=lambda x: x['w_match_size'])
    min_length_pattern = sorted_b_list[0]['w_match_size']

    for w in sorted_b_list:
      if w['w_match_size'] != min_length_pattern:
        break
          
      # get those with the minimum length
      min_length_match_patterns.append(w)

    if len(min_length_match_patterns) > 1:
      return self.choose_random_pattern(min_length_match_patterns)
      
    return min_length_match_patterns[0]

  @staticmethod
  def choose_next_theme_method_to_fill(curr_method: str) -> str:
    from ..helpers.constants import THEME_BLOCKS

    switcher = {
      "THEME_CENTER": THEME_BLOCKS.FIRST_SYMMETRIC.value,
      "THEME_FIRST_SYMMETRIC": THEME_BLOCKS.SECOND_SYMMETRIC.value,
      "THEME_SECOND_SYMMETRIC": "MOST_CONSTRAINED",
    }
    
    return switcher.get(curr_method, None)