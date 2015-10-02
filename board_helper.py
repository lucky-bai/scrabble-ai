
class BoardHelper:
  """
  Handles boring board functions that aren't directly related to AI
  """
  def __init__(self, size):
    self.SIZE = size

  def square_neighbors(self, sq):
    r = sq[0]
    c = sq[1]
    if r > 0:
      yield (r-1,c)
    if c > 0:
      yield (r,c-1)
    if r < self.SIZE - 1:
      yield (r+1,c)
    if c < self.SIZE - 1:
      yield (r,c+1)

  def print_board(self, board):
    # Print out board in ascii
    for r in range(self.SIZE):
      for c in range(self.SIZE):
        print board[r][c].upper(),
      print ''
    print '---------------------'

  def words_on_board(self, bd):
    """
    Determines which words are on the board. Doesn't check for validity.
    Returns set of (word, starting square, vertical)
    """
    words = set()
    for r in range(self.SIZE):
      cur_run = ''
      for c in range(self.SIZE):
        if bd[r][c] != '.':
          cur_run += bd[r][c]
        else:
          if len(cur_run) >= 2:
            words.add((cur_run, (r,c-len(cur_run)), False))
          cur_run = ''
      if len(cur_run) >= 2:
        words.add((cur_run, (r,self.SIZE-len(cur_run)), False))
    for c in range(self.SIZE):
      cur_run = ''
      for r in range(self.SIZE):
        if bd[r][c] != '.':
          cur_run += bd[r][c]
        else:
          if len(cur_run) >= 2:
            words.add((cur_run, (r-len(cur_run),c), True))
          cur_run = ''
      if len(cur_run) >= 2:
        words.add((cur_run, (self.SIZE-len(cur_run),c), True))
    return words
