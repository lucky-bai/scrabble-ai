
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

# Print out board in ascii
  def print_board(self, board):
    for r in range(self.SIZE):
      for c in range(self.SIZE):
        print board[r][c].upper(),
      print ''
    print '---------------------'
