import enum

class THEME_BLOCKS(enum.Enum):
  CENTER = "THEME_CENTER"
  FIRST_SYMMETRIC = "THEME_FIRST_SYMMETRIC"
  SECOND_SYMMETRIC = "THEME_SECOND_SYMMETRIC"

SCRABBLE_RATE = [
  {
    "letters": ("A", "E", "I", "O", "U", "L", "N", "S", "T", "R"),
    "score": 1
  }, 
  {
    "letters": ("D", "G"),
    "score": 2
  }, 
  {
    "letters": ("B", "C", "M", "P"),
    "score": 3
  }, 
  {
    "letters": ("F", "H", "V", "W", "Y"),
    "score": 4
  }, 
  {
    "letters": ("K"),
    "score": 5
  }, 
  {
    "letters": ("J", "X"),
    "score": 8
  }, 
  {
    "letters": ("Q", "Z"),
    "score": 10
  }, 
]