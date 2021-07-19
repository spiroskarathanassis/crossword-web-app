from ..helpers.functions import sort_words_by_score

class Pick_Strategy:
  def __init__(self):
    self.reset_pick_strategy()

  def reset_pick_strategy(self):
    self.already_tried_words_in_current_block = []
    self.sorted_word_list = []
    self.words_already_used = []
  
  def chooose_method_to_pick(self, method: str, w_list: list) -> str:
    if len(w_list) == 0:
      return None

    switcher = {
      "FISRT_WORD_OCCURANCE": lambda: self.choose_first_word_occur(w_list),
      "RANDOM_WORD": lambda: self.choose_random_word(w_list),
      "SCRABBLE_WORD": lambda: self.choose_scrabble_word(w_list)
    }
    switch_res = switcher.get(method, None)
    
    # EnvironmentError(method, 'Error fill method, is not accepted')
    return None if switch_res == None else switch_res()
  
  def choose_first_word_occur(self, w_list: list) -> str:
    return w_list[0]
  
  def choose_random_word(self, w_list: list) -> str:
    from random import randrange
    random_number = randrange(0, len(w_list))

    return w_list[random_number]

  def choose_scrabble_word(self, w_list: list) -> str:
    if len(self.words_already_used) == 0:      
      self.sorted_word_list = sort_words_by_score(w_list.copy())
    
    # keep the word(s) with the lowest score
    # min_score = self.sorted_word_list[0].get('score')

    for selected_word in self.sorted_word_list:
      if selected_word.get('word') in self.words_already_used:
        continue
      
      next_word = selected_word.get('word')
      self.words_already_used.append(next_word)
      return next_word
    
    return ''
  
  def choose_next_scrabble_word_selected(self, prev_selected: str):
    prev_selected = prev_selected.lower()
    next_choosed_word = ''

    for curr_word_spec in self.sorted_word_list:
      current_word = curr_word_spec.get('word').lower()

      if (current_word in self.already_tried_words_in_current_block
        or current_word in self.words_already_used
        or current_word == prev_selected):
        continue
      
      next_choosed_word = current_word
      break

    self.already_tried_words_in_current_block.append(prev_selected)

    return next_choosed_word