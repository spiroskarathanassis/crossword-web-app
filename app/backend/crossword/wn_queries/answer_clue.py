import random
from re import sub
import spacy
from nltk.corpus import wordnet as wn

from ..crawler.search_google import GoogleSpider

class Answer_Clue:
  def __init__(self, theme: str):
    self.theme_input = theme
    # Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
    self.nlp = spacy.load('en_core_web_lg', disable=['parser', 'ner'])

  def prepare_answer_clue(self, answer_infos: list) -> list:
    for ans_info in answer_infos:
      if ans_info.get('is_reversed'):
        print('Reversed answer', ans_info.get('answer'))
        ans_info['answer'] = ans_info.get('answer')[::-1]
      
      clue = self.find_clue(ans_info.get('answer'), ans_info.get('is_theme_similar'))
      clue = self.capitilize_first_letter(clue)
      
      if ans_info.get('is_reversed'):
        clue = self.adjustTypeOfTease(clue, 'reversed')
      elif ans_info.get('is_relaxed'):
        clue = self.adjustTypeOfTease(clue, 'relaxed')

      ans_info['clue'] = clue

  def find_clue(self, answer: str, is_themed: bool = False) -> str:
    syns = wn.synsets(answer)
    clue = ""

    if len(syns) > 0:
      clue = self.get_clue_by_example_or_definition(syns)
    
    if is_themed and not(clue):
      lemma_name = wn.morphy(answer)

      if lemma_name:
        # find the slope if possible only for nouns and verbs
        syns = wn.synsets(lemma_name)
        clue = self.get_clue_by_example_or_definition(syns, True)
      
      # word google search definition
      if not(clue):
        clue = GoogleSpider().search_doc_definition(answer)

        if not(clue):
          # print(f'------- {answer} not found in wordnet')
          return ""

    clue = self.remove_answer_from_clue(answer, clue)
    return clue
  
  def get_clue_by_example_or_definition(self, syns: list, is_themed: bool = False) -> str:
    choices = ['definition', 'example']
    definitions = []
    examples = []
    choice = random.choice(choices)

    for synset in syns:
      # word example
      examples += synset.examples()
      # word definition
      definitions.append(synset.definition())
    
    if is_themed:
      theme_doc = self.nlp(self.theme_input)
      max_similar_score = 0

      if choice == 'example' and len(examples) > 0:
        example = ""

        # find the best example similar to theme
        for ex in examples:
          ex_doc = self.nlp(ex)
          score = theme_doc.similarity(ex_doc)
          
          if score > max_similar_score:
            example = ex
        
        return example
      
      # choice is definition
      clue_definition = ""
      for definition in definitions:
        definition_doc = self.nlp(definition)
        score = theme_doc.similarity(definition_doc)
        
        if score > max_similar_score:
          clue_definition = definition
      
      return clue_definition
    else:
      if choice == 'example' and len(examples) > 0:
        return random.choice(examples)
      
      if len(definitions) > 0:
        return random.choice(definitions)
    
    return ""

  def remove_answer_from_clue(self, answer: str, clue: str) -> str:
    # find the word lemma of the word via spacy where is more accurate
    ans_doc = self.nlp(answer)
    clue_doc = self.nlp(clue)

    for token in clue_doc:
      if token.lemma_ == ans_doc[0].lemma_:
        ans_token = token.text
        replace_text = '*' * len(ans_token)
        clue = sub(ans_token, replace_text, clue)
        break
    
    return clue

  def capitilize_first_letter(self, sentence: str):
    sentence = sentence[:1].upper() + sentence[1:]
    return sentence
  
  def adjustTypeOfTease(self, clue: str, type: str) -> str:
    return f'{clue} [{type}]'
  
  @staticmethod
  def add_id(ans_n_clues: list) -> None:
    for (index, ans) in enumerate(ans_n_clues):
      ans['id'] = index