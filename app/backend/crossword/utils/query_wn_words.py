from ..wn_queries import Wn_Queries
from ..blocks import Block

def search_for_relaxed_words(pattern: str, block: dict) -> bool:
  words_matched = Wn_Queries.get_bigger_length_matched_words(pattern)

  if len(words_matched) > 0:
    Block.adjust_current_block_new_words(block, words_matched)
    block['is_relaxed'] = True
    return True

  return False

def search_rest_pos_tags(pattern: str):
  return Wn_Queries.get_total_match_words_by_pos_tag(pattern, False)

def search_reversed_match(pattern: str, block: dict) -> bool:
  words_matched = Wn_Queries.get_reversed_match_words(pattern)

  if len(words_matched) > 0:
    Block.adjust_current_block_new_words(block, words_matched)
    block['is_reversed'] = True

    return True

  return False