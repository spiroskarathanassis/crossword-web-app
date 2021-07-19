from .grid import Grid
from .blackbox import Blackbox
from .pattern import Pattern
from .fill_strategy import Fill_Strategy
from .pick_strategy import Pick_Strategy
from .wn_queries.answer_clue import Answer_Clue

from .crawler import Crawler

from .blocks import Block
from .blocks.neighbor import Neighbor
from .blocks.theme_block import Theme_Block

from .utils import query_wn_words
from .helpers.print import Print
from .helpers import functions, constants

class Crossword_Generator:
  def __init__(self, theme: str, size: int = 15, is_level_easy: bool = True) -> None:
    self.INPUT_THEME = theme
    self.GRID_SIZE = size #e.g. 15x15
    self.IS_LEVEL_EASY = is_level_easy
    self.IS_RESPECT_SOLVER = False
  
  def begin_generate(self):
    # grid size
    self.cross_grid = Grid(self.GRID_SIZE)
    self.grid = self.cross_grid.get_grid()

    # initialize blackboxes
    self.blackbox = Blackbox(self.grid)
    self.total_blackboxes = self.blackbox.get_possible_blackboxes()
    print("✔ Black box filling task commpleted")

    # Find all seperated theme words over (wordnet or crawler)
    self.crawled_theme_words = Crawler().collect_all_crawled_theme_words(self.INPUT_THEME).copy()
    print('Themed ', len(self.crawled_theme_words))
    
    # initialize strategy
    self.fill_strategy = Fill_Strategy()
    start_fill_method = constants.THEME_BLOCKS.CENTER.value
    self.prefered_pick_method = 'SCRABBLE_WORD'

    # Initialize global variables
    self.block_neighbor = Neighbor()
    self.last_block_checked = {}
    self.saved_answers_and_clues = [] #save list of { answer, clue, ... } format
    self.words_exists_in_grid = []
    self.theme_blocks = []
    self.total_blocks = 0

    self.start_with_standard_theme_blocks(self.total_blackboxes, self.crawled_theme_words, start_fill_method)

  def collect_valid_answers(self, block: list, word: str, is_theme_similar: bool) -> None:
    self.saved_answers_and_clues.append({
      "answer": word, #lower case
      "clue": '',
      "dimension": block.get('dimension'),
      "spot": block.get('start_spot'),
      "length": block.get('length'),
      "is_reversed": True if block.get('is_reversed') else False,
      "is_relaxed": True if block.get('is_relaxed') else False,
      "is_theme_similar": is_theme_similar
    })

  def choose_next_grid_block(self, uncompleted_blocks_specs: list, prefered_fill_method = 'MOST_CONSTRAINED'):
    print("-------------------------------------------------\n")
    if len(uncompleted_blocks_specs) == 0:
      return True

    # Fill Strategy
    selected_fill_block = self.fill_strategy.choose_method_to_fill(prefered_fill_method, uncompleted_blocks_specs[:])
    Print.print_dictionary(selected_fill_block, 'Block selected to fill')
    print(f"✔ selected block by {prefered_fill_method} method commpleted")

    pick_strategy = Pick_Strategy()
    
    selected_block = selected_fill_block.copy()
    self.last_block_checked = selected_block.copy()
    is_match = False
    word_switcher = {
      'is_theme_words_turn': 'is_already_saved_turn',
      'is_already_saved_turn': 'is_rest_pos_tags_turn',
      'is_rest_pos_tags_turn': 'is_reversed_turn',
      'is_reversed_turn': 'is_relaxed_turn',
      'is_relaxed_turn': 'is_finished'
    }
    word_current_access = 'is_theme_words_turn'

    current_theme_words = functions.filter_crawled_words(
      self.crawled_theme_words.copy(),
      selected_block.get('pattern')
    )
    # adjective and adverb
    current_rest_pos_words = lambda: query_wn_words.search_rest_pos_tags(selected_block.get('pattern'))
    run_pos_tags_once = False

    is_found_reversed = False
    is_found_relaxed = False

    while not(is_match):
      selected_word = ''

      while True:
        # Initialize words to pick
        if word_current_access == "is_theme_words_turn":
          words_matched = current_theme_words
        elif word_current_access == "is_rest_pos_tags_turn":
          if not(run_pos_tags_once):
            words_matched = current_rest_pos_words()
            run_pos_tags_once = True
        else:
          words_matched = list(selected_block.get('match_words'))

        if len(words_matched) == 0 and word_current_access == 'is_relaxed_turn':
          return False

        if len(words_matched) != 0:
          # Pick Strategy
          selected_word = pick_strategy.chooose_method_to_pick(self.prefered_pick_method, words_matched)
          print(f"✔ selected word: {selected_word} by {self.prefered_pick_method} method commpleted")

        if selected_word:
          # -- Best accurance check
          if (selected_word in self.words_exists_in_grid):
            continue
          break

        # -- Dicision not word found
        curr_block_pattern = selected_block.get('pattern')
        print(f"✘ Word list of block was empty, pattern: {curr_block_pattern}")

        # Switching next word entity searching method
        word_current_access = word_switcher.get(word_current_access, None)
        
        # Reset  word list
        pick_strategy.reset_pick_strategy()

        # After theme searched find a general pattern word match
        if word_current_access in ['is_already_saved_turn', 'is_rest_pos_tags_turn']:
          continue
        elif word_current_access == 'is_reversed_turn' and not(is_found_reversed):
          is_found_reversed = query_wn_words.search_reversed_match(curr_block_pattern, selected_block)
          if is_found_reversed:
            continue
        elif word_current_access == 'is_relaxed_turn' and not(is_found_relaxed):
          is_found_relaxed = query_wn_words.search_for_relaxed_words(curr_block_pattern, selected_block)
          if is_found_relaxed:
            continue

        return False

      first_choice = selected_word #temp
      rest_uncompleted_blocks = functions.deepcopy_blocks(uncompleted_blocks_specs)

      if prefered_fill_method == 'MOST_CONSTRAINED':
        rest_uncompleted_blocks = Neighbor.adjust_neighbor_by_most_constrained(
          pick_strategy,
          self.cross_grid,
          rest_uncompleted_blocks,
          selected_block,
          selected_word
        )
      else:
        self.cross_grid.put_word_in_block(selected_block, selected_word)
      
      self.words_exists_in_grid.append(selected_word)
      if word_current_access == 'is_reversed_turn':
        print(f"Selected reversed word: {selected_word}")
      else:
        print(f"First choise is '{first_choice}' and finally choose: {selected_word}")

      Print.print_crossword(self.grid)
      new_uncompleted_blocks = list(filter(lambda block: block.get('id') != selected_block['id'], rest_uncompleted_blocks))
      is_match = self.choose_next_grid_block(new_uncompleted_blocks)

      if is_match:
        is_themed = word_current_access == 'is_theme_words_turn'
        self.collect_valid_answers(selected_block, selected_word, is_themed)
        return True

      self.words_exists_in_grid.remove(selected_word)
      self.cross_grid.remove_word_from_block(selected_block)
      
      if not(self.block_neighbor.is_parent_neighbor_of_child(selected_block, self.last_block_checked)):
        return False

    return False

  def start_with_standard_theme_blocks(self, blackboxes: int, theme_words: list, prefered_fill_method: str, symmetric_themed_block: dict = None):
    pick_strategy = Pick_Strategy()
    selected_block = None
    is_match = False
    is_searching_new_length = True
    is_theme_method_symmetric = prefered_fill_method != constants.THEME_BLOCKS.CENTER.value
    search_length = len(self.grid) if prefered_fill_method == constants.THEME_BLOCKS.CENTER.value else len(self.grid) - (3 + 1) # 1 extra is for 1 blackbox

    if is_theme_method_symmetric:
      if prefered_fill_method == constants.THEME_BLOCKS.FIRST_SYMMETRIC.value:
        theme_block = Theme_Block()
        selected_block = theme_block.choose_another_diff_length_across_block(self.grid, blackboxes, search_length)
      else:
        selected_block = functions.find_and_adjust_symmetric_block(symmetric_themed_block, self.GRID_SIZE)
    
    while not(is_match):
      selected_word = ''

      while True:
        if (search_length < 3):
          print('No themed crossword generated')
          return False
        
        if is_searching_new_length:
          block_poss_words = theme_words.copy()
          block_poss_words = list(filter(lambda word: len(word) == search_length, block_poss_words))
        
        if ( len(block_poss_words) == 0 or not(selected_block) ) and prefered_fill_method == constants.THEME_BLOCKS.FIRST_SYMMETRIC.value:
          is_searching_new_length = True
          search_length -= 1
          selected_block = theme_block.choose_another_diff_length_across_block(self.grid, blackboxes, search_length)
          continue

        if len(block_poss_words) > 0:
          selected_word = pick_strategy.chooose_method_to_pick(self.prefered_pick_method, block_poss_words)
        
        if selected_word:
          if (selected_word in self.words_exists_in_grid): continue

          is_searching_new_length = False
          break
        else:
          if prefered_fill_method == constants.THEME_BLOCKS.SECOND_SYMMETRIC.value:
            # if is second symmetric do not search for other block -> do only for the first symmetric
            return False

        pick_strategy.reset_pick_strategy()

        if prefered_fill_method == constants.THEME_BLOCKS.CENTER.value:
          is_searching_new_length = True
          search_length -= 2 # cannot be a symmetric length in center even number
          selected_block = Theme_Block.find_another_across_theme_block(self.grid, blackboxes, search_length)
        else:
          selected_block = theme_block.choose_another_same_length_across_block()
      
      # Set the block to fill
      if prefered_fill_method == constants.THEME_BLOCKS.CENTER.value:
        selected_block = Theme_Block.set_centered_theme_block(selected_word, self.GRID_SIZE)

      # Adjust blackboxes
      black_registered = self.blackbox.fill_blacks_for_theme_blocks(prefered_fill_method, selected_block.copy())
      total_blackboxes = blackboxes - black_registered

      self.cross_grid.put_word_in_block(selected_block, selected_word)
      self.words_exists_in_grid.append(selected_word)
      self.theme_blocks.append(selected_block.copy())

      if prefered_fill_method == constants.THEME_BLOCKS.SECOND_SYMMETRIC.value:
        self.blackbox.paste_boxes_symmetrically(total_blackboxes)

        # found how many across & down words have available
        blocks = Block(self.grid)
        print("✔ Adjusting blocks information commpleted")
        uncompleted_blocks = blocks.keep_uncompleted_blocks(self.theme_blocks)
        self.block_neighbor.uncompleted_blocks = uncompleted_blocks.copy()
        
        # Adjust pattern to uncompleted blocks
        pattern = Pattern(uncompleted_blocks, self.IS_RESPECT_SOLVER)
        uncompleted_blocks = pattern.adjust_block_pattern(self.grid)
        print("✔ Adjusting block pattern task commpleted")

        self.total_blocks = len(uncompleted_blocks)
        is_match = self.choose_next_grid_block(uncompleted_blocks)
      else:
        symmetric_block = selected_block.copy() if prefered_fill_method == constants.THEME_BLOCKS.FIRST_SYMMETRIC.value else None
        next_method = Fill_Strategy.choose_next_theme_method_to_fill(prefered_fill_method)
        is_match = self.start_with_standard_theme_blocks(total_blackboxes, theme_words.copy(), next_method, symmetric_block)

      if is_match:
        self.collect_valid_answers(selected_block, selected_word, True)
        return True
      
      self.blackbox.remove_blacks_from_grid(prefered_fill_method) # Remove last blacks
      self.theme_blocks.remove(selected_block)
      self.words_exists_in_grid.remove(selected_word)
      self.cross_grid.remove_word_from_block(selected_block)

    return False

  def adjust_answers_to_clues(self):
    Answer_Clue(self.INPUT_THEME).prepare_answer_clue(self.saved_answers_and_clues)
    Answer_Clue.add_id(self.saved_answers_and_clues)
    # Print.print_answers(self.saved_answers_and_clues)s
    Print.print_crossword(self.grid)

    return self.saved_answers_and_clues