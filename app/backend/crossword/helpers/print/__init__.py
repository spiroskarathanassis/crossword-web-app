class Print:
  @staticmethod
  def print_crossword(grid: list):
    """ Prints the grid
    
    Arguments:
      grid [list] -- matrix of generated crossword
    """
    length = len(grid)

    for col in grid:
      print(length * ' ---')
      row_chars = '| '
      
      for row in col:
        row = row or ' '
        row_chars += row + ' | '

      print(row_chars)
    print(length * ' ---')
  
  @staticmethod
  def print_dictionary(dic: dict, msg: str = "Dictionary"):
    """Prints dictionary elements verically"""
    print("\n------ " + msg)

    for key, value in dic.items():
      v = str(value)
      
      if key == 'match_words': continue
      
      if (type(value) == tuple):
        v =  str(value[0]) + ',' + str(value[1])
      
      sentence = " |" + key + ": " + v
      print(sentence)
    
    print("\n")
  
  @staticmethod
  def print_answers(answers: list):
    print("\n------ Answers")
    for ans in answers:
      print(
        ans.get('answer'), 
        ans.get('dimension'), 
        ans.get('spot'), 
        ans.get('is_reversed'),
        ans.get('is_relaxed'),
        'themed' if ans.get('is_theme_similar') else '',
      )

  @staticmethod
  def test_print(blocks):
    for curr_block in blocks:
      print(
        (
          curr_block.get('start_spot')[0], 
          curr_block.get('start_spot')[1]
        ), 
        curr_block.get('dimension'),
        curr_block.get('length'),
        curr_block.get('w_match_size'), 
        curr_block.get('pattern'),
      )