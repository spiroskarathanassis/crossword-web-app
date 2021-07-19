import unittest

import sys
sys.path.append('./app/backend/')

from crossword.blocks.neighbor import Neighbor
from constants import uncompleted_blocks

neighbor = Neighbor()
neighbor.set_blocks(uncompleted_blocks)

class TestNeighorhood(unittest.TestCase):
  def test_neighborhood_true(self):
    parent = {'id': 4,  'start_spot': (2, 0), 'length': 6, 'dimension': 'across'}
    child = {'id': 28, 'start_spot': (0, 4), 'length': 7, 'dimension': 'down'  }
    
    self.assertTrue(neighbor.is_parent_neighbor_of_child(parent, child))

  def test_neighborhood_false(self):
    parent = {'id': 4,  'start_spot': (2, 0), 'length': 6, 'dimension': 'across'}
    child = {'id': 39, 'start_spot': (8, 10),'length': 3, 'dimension': 'down'  }
    
    self.assertFalse(neighbor.is_parent_neighbor_of_child(parent, child))

if __name__ == '__main__':
  unittest.main()