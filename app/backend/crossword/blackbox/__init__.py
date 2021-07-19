# reference ./tips.txt
from math import pow
from random import randrange

class Blackbox:
  def __init__(self, grid: list):
    self.total_blackboxes = 0
    self.grid = grid
    self.grid_length = len(grid) # dimension length
    self.total_cells = pow(len(grid), 2)
    self.current_row = 0
    self.current_col = 0
    self.theme = {
      "center": [],
      "symmetric": [], # 2 symmetric theme blocks
      "rest_uncompleted": []
    }

  def get_possible_blackboxes(self):
    """
    Returns:
      [integer] -- a number of black boxes according to 12%-16% of grid length
    """
    random_number = randrange(14, 16)
    blackboxes = round(random_number * self.total_cells / 100)
    
    # number of black boxes must be even, because of symmetric
    if (blackboxes % 2) == 1:
      blackboxes += 1

    self.total_blackboxes = blackboxes
    return blackboxes
  
  def paste_boxes_symmetrically(self, blacks: int):
    """ Returns: [list]: grid with generated black boxes """
    prefered_fill_index = 0

    while (blacks > 0):
      possible_black_cells = self.collect_black_availaibility()
      pos_length = len(possible_black_cells)
      
      if (pos_length == 0): break

      if prefered_fill_index > 1:
        possible_black_cells = self.get_current_prefered_blacks(possible_black_cells)
      
      random_index = randrange(0, len(possible_black_cells))
      black_row = possible_black_cells[random_index][0]
      black_col = possible_black_cells[random_index][1]

      self.grid[black_row][black_col] = '#'
      self.grid[self.grid_length - black_row - 1][self.grid_length - black_col - 1] = '#' #diagonal symmetric
      self.theme["rest_uncompleted"].append((black_row, black_col))
      
      blacks -= 2
      prefered_fill_index += 1

  def get_current_prefered_blacks(self, cells: list):
    """
    # method_empty_both_dims
    # method_empty_at_least_one_dim
    # method_neighbors_3x3_under_four_blacks
    # method_long_distance - (over 8 cells)
    """

    prefered_both_dim_black = []
    points_of_3_method_neighbors_3x3 = []
    points_of_2_method_neighbors_3x3 = []
    one_dim_black_cells = []
    long_distance_cells = []
    self.prefered_pointed_cells = []

    # desicion prefer from unsuported directions(row & col) from list @see tips.txt
    for pos_black in cells:
      pos_row = pos_black[0]
      pos_col = pos_black[1]
      row_accepts_black = True
      col_accepts_black = True
      
      # 1. method_empty_both_dims
      for index in range(0, self.grid_length):
        if self.grid[pos_row][index] == '#':
          row_accepts_black = False
        if self.grid[index][pos_col] == '#':
          col_accepts_black = False
      
      # if row and col has not any black yet
      if row_accepts_black and col_accepts_black:
        prefered_both_dim_black.append(pos_black)

      # 2. method_neighbors_3x3_under_four_blacks
      points = 0
      is_not_edge_of_grid = (pos_row != 0 or pos_col != 0)

      # if row or col has not any black yet
      if row_accepts_black or col_accepts_black:
        one_dim_black_cells.append(pos_black)
        points += 1
      
      points += self.get_box_points_prefered_standards(pos_black)

      if points == 3 and is_not_edge_of_grid:
        points_of_3_method_neighbors_3x3.append(pos_black)
      elif points == 2:
        points_of_2_method_neighbors_3x3.append(pos_black)

      if points == 2 and is_not_edge_of_grid:
        self.prefered_pointed_cells.append(pos_black)
      
      # 3. method_long_distance - (over 8 cells)
      if self.is_long_distance_cell(pos_row, pos_col) and (row_accepts_black or col_accepts_black):
        long_distance_cells.append(pos_black)
  
    # decision choice
    if len(prefered_both_dim_black) > 0:
      cells = prefered_both_dim_black
    elif len(self.prefered_pointed_cells) > 0:
      cells = points_of_3_method_neighbors_3x3 if len(points_of_3_method_neighbors_3x3) > 0 else points_of_2_method_neighbors_3x3
    elif len(long_distance_cells) > 0:
      cells = long_distance_cells
    elif len(one_dim_black_cells) > 0:
      cells = one_dim_black_cells

    return cells


  def collect_black_availaibility(self):
    """Returns [list]"""
    availables = []
    center_index = int(self.grid_length / 2)
    center_cell = (center_index, center_index)
    # excluded middle cells symmetrically around center
    excluded = {
      (center_index    , center_index - 1),
      (center_index    , center_index + 1),
      (center_index - 1, center_index    ),
      (center_index + 1, center_index    )
    }
    
    try:
      for row in range(0, self.grid_length):
        for col in range(0, self.grid_length):
          if (row, col) == center_cell:
            raise StopIteration # break from the loops
          if (row, col) in excluded or (self.grid[row][col]):
            continue

          self.current_row = row
          self.current_col = col

          if self.are_neighbors_accept_black():
            availables.append((row, col))
    except StopIteration: pass

    return availables

  def remove_blacks_from_grid(self, block_entity: str):
    EMPTY_STRING = ''

    if block_entity == 'THEME_CENTER':
      if len(self.theme.get('center')) > 0:
        for spot in self.theme.get('center'):
          last_row = spot[0]
          last_col = spot[1]
          self.grid[last_row][last_col] = EMPTY_STRING
          self.grid[last_row][self.grid_length - 1 - last_col] = EMPTY_STRING
    
    else:
      # symmetric
      theme_key = "symmetric" if block_entity == "THEME_FIRST_SYMMETRIC" else "rest_uncompleted"

      if len(self.theme.get(theme_key)) > 0:
        for spot in self.theme.get(theme_key):
          last_row = spot[0]
          last_col = spot[1]
          self.grid[last_row][last_col] = EMPTY_STRING
          self.grid[self.grid_length - 1 - last_row][self.grid_length - 1 - last_col] = EMPTY_STRING

  def fill_blacks_for_theme_blocks(self, position: str, block: dict) -> int:
    """ position {[string]} -- 'center' or 'elsewhere' """
    black_registered = 0
    
    if position == 'THEME_CENTER':
      if block.get('length') == self.grid_length:
        return 0

      # find two spots right & left of centered word
      centered_row = block.get('start_spot')[0]
      centered_col = block.get('start_spot')[1]
      accepted = False
      index = 1
      # if neighbors accepts then push and return
      while accepted == False:
        self.current_row = centered_row
        self.current_col = centered_col - index
        
        if self.are_neighbors_accept_black():
          accepted = True
       
        self.grid[self.current_row][self.current_col] = '#'
        self.grid[self.current_row][self.grid_length - 1 - self.current_col] = '#' #column symmetric
        self.theme["center"].append((self.current_row, self.current_col))

        black_registered += 2
        index += 1
    elif position == "THEME_FIRST_SYMMETRIC":
      # case is known across
      start_row = block.get('start_spot')[0]
      start_col = block.get('start_spot')[1]
      insert_down_blacks = 1
      # put one time at first symmetric random block selected
      if start_col == 0:
        if start_row <= 2:
          insert_down_blacks = start_row + 1
      
        black_registered = insert_down_blacks
        index = 0
        while insert_down_blacks > 0:
          self.current_row = start_row - index
          self.current_col = start_col + block.get('length')

          self.grid[self.current_row][self.current_col] = '#'
          self.grid[self.grid_length - 1 - self.current_row][self.grid_length - 1 - self.current_col] = '#'
          self.theme["symmetric"].append((self.current_row, self.current_col))

          insert_down_blacks -= 1
          index += 1

    return black_registered

  def are_neighbors_accept_black(self):
    """Returns: [boolean]"""
    top     = self.get_direction_status(False, -1)
    bottom  = self.get_direction_status(False, 1)
    left    = self.get_direction_status(True, -1)
    right   = self.get_direction_status(True, 1)

    is_on_the_edge = True if self.is_on_the_grid_side() else False

    if (
      not('reject' in {top, bottom, left, right})
      and (
        ('accept' in {left, right} # across
          and 'accept' in {top, bottom} # down
        ) or (
          'accept' in {top, bottom, left, right}
          and is_on_the_edge
        )
      )
    ):
      return True

    return False
  
  def get_direction_status(self, is_horizontial: bool, sign: str):
    """ 
    Arguments:
      is_horizontial {[boolean]} -- Horizontial: True, Vertical: False
      sign {[integer]} -- (1) or (-1)

    Returns:
      [string] -- {
        "black" -- if neighbor cell is 'black' or 'out of grid'
        "accept" -- if belongs to 3+ empty cells (in the same dirction check)
        "reject" -- elsewhere
      }
    """
    count = 0

    # look into next 3 cells of all directions
    for index in range(1, 4):
      i = sign * index

      if is_horizontial:
        if (0 <= self.current_col + i < self.grid_length):
          if self.grid[self.current_row][self.current_col + i] == '#':
            return 'black' if count == 0 else 'reject'
          
          count += 1
        else: # out of grid
          return self.is_on_the_grid_side(count)
          
      else:
        if (0 <= self.current_row + i < self.grid_length):
          if self.grid[self.current_row + i][self.current_col] == '#':
            return 'black' if count == 0 else 'reject'

          count += 1
        else: # out of grid
          return self.is_on_the_grid_side(count)

    if (count == 3):
      return 'accept'

    return 'reject'

  def get_box_points_prefered_standards(self, pos_black: list) -> int:
    """Returns points"""
    pos_row = pos_black[0]
    pos_col = pos_black[1]
    # if grid neighbor of 3x3 has not more than 3 blacks
    # and distance from another black is over than 8
    points = 0
    is_neighbors_allowed = True
    
    for i in range(3):
      for cc in range(3):
        count = 0
        
        for x in range(pos_row - 2 + i, 1 + i):
          for y in range(pos_col - 2 + cc, 1 + cc):
            
            if self.grid[x][y] and self.grid[x][y] == '#':
              count += 1
            
        if count < 3 and not(pos_black in self.prefered_pointed_cells):
          is_neighbors_allowed = False
  
    if is_neighbors_allowed:
      points += 1
    
    # if row or col has a gap of blacks bigger than 8
    if self.is_long_distance_cell(pos_row, pos_col):
      points += 1
    
    return points

  def is_long_distance_cell(self, row: str, col: str) -> bool:
    # if row or col has a gap of blacks bigger than 8
    GAP = 8

    for index in range(0, self.grid_length):
      if (
        (
          (0 <= row - index < self.grid_length) and self.grid[row - index][col] == '#'
          or (0 <= row + index < self.grid_length) and self.grid[row + index][col] == '#'
        ) or (
          (0 <= col - index < self.grid_length) and self.grid[row][col - index] == '#'
          or (0 <= col + index < self.grid_length) and self.grid[row][col + index] == '#'
        ) 
      ) and (
        abs(row - index) > GAP or abs(col - index) > GAP
        or abs(row + index) > GAP or abs(col + index) > GAP
      ):
        return True
    
    return False

  def is_on_the_grid_side(self, counter: int = 0):
    if (self.current_row == 0 or self.current_col == 0) and counter == 0:
      return 'black'
    
    return 'reject'