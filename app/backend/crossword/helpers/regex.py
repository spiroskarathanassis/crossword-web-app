import re

def build_regex_word_pattern(pattern: str):
  # '??a?' -> '[a-z][a-z]a[a-z]'
  return pattern.lower().replace('?', '[a-z]')

def recalculate_matched_words(pattern: str, previous_matched_words: list):
  mathed_words = previous_matched_words.copy()
  regex = build_regex_word_pattern(pattern)
  
  return list(
    filter(
      lambda word: re.search(regex, word.lower()),
      mathed_words
    )
  )

def find_relative_word(word: str, pattern: str):
  regex = build_regex_word_pattern(pattern)
  res = re.search(regex, word.lower())
  
  return res.group(0)

def choose_part_of_definition(definition_of_google: str) -> str:
  # split every sentence
  sentences = re.split('\. ', definition_of_google)
  if len(sentences) == 0:
    return definition_of_google
  
  # from 1st sentence find a definition between 2 commas
  spesific_definition = re.split(',', sentences[0])
  if spesific_definition[1]:
    return spesific_definition[1]

  # else return all the 1st sentence
  return sentences[0]