"""
Rules:
  - search for words match the pattern
  - prefered to be noun or adverb
"""
from nltk.corpus import wordnet as wn
import re

from ..helpers.regex import build_regex_word_pattern

NUMBERS_WORD_REGEX = "\d+" # numbers
DASH_WORD_REGEX = "(_|-)" # ex: ad_hoc
NUMBERS_OR_DASH_REGEX = "\d+|(_|-)"

class Wn_Queries:

  @staticmethod
  def get_total_match_words(pattern: str):
    word_list = []
    length = len(pattern)
    curr_block_regex = build_regex_word_pattern(pattern)

    for lemma_name in wn.words():
      if len(lemma_name) == length:
        if not(re.search(NUMBERS_OR_DASH_REGEX, lemma_name)):
          curr_name = lemma_name.lower()

          if re.match(curr_block_regex, curr_name):
            word_list.append(curr_name)

    return word_list

  @staticmethod
  def get_total_match_words_by_pos_tag(pattern: str, is_prefered_pos_tag: bool = True):
    word_list = set()
    length = len(pattern)
    curr_block_regex = build_regex_word_pattern(pattern)
    pos_tags = ['n', 'v'] if (is_prefered_pos_tag) else ['a', 'r']

    def save_same_lemma_names(synset):
      for lemma_name in synset.lemma_names():
        if len(lemma_name) == length:

          if not(re.search(NUMBERS_OR_DASH_REGEX, lemma_name)):
            curr_name = lemma_name.lower()

            if re.match(curr_block_regex, curr_name):
              word_list.add(curr_name)
    
    for tag in pos_tags:
      for synset in wn.all_synsets(tag):
        save_same_lemma_names(synset)
    
    return list(word_list)

  @staticmethod
  def get_bigger_length_matched_words(pattern: str):
    word_list = []
    length = len(pattern)
    curr_block_regex = build_regex_word_pattern(pattern)

    for lemma_name in wn.words():
      if length <= len(lemma_name) <= length + 3:
        if not(re.search(NUMBERS_OR_DASH_REGEX, lemma_name)):
          curr_name = lemma_name.lower()

          if re.search(curr_block_regex, curr_name):
            word_list.append(lemma_name)
  
    return word_list
  
  @staticmethod
  def get_reversed_match_words(pattern: str):
    word_list = []
    length = len(pattern)
    pattern = pattern[::-1]
    curr_block_regex = build_regex_word_pattern(pattern)

    for lemma_name in wn.words():
      if len(lemma_name) == length:
        if not(re.search(NUMBERS_OR_DASH_REGEX, lemma_name)):
          curr_name = lemma_name.lower()

          if re.match(curr_block_regex, curr_name):
            word_list.append(curr_name)

    return word_list
