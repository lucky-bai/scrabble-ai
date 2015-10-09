
class BoardHelper:
  """
  Handles boring board functions that aren't directly related to AI
  """
  def __init__(self, size, language):
    self.SIZE = size
    self.LANGUAGE = language
  
  # . blank
  # 2,3: double, triple word
  # d,t: double, triple letter
  BOARDSTRS = {
    11: """
    t.3.....3.t
    .2...2...2.
    3.d.d.d.d.3
    ...t...t...
    ..d.....d..
    .2.......2.
    ..d.....d..
    ...t...t...
    3.d.d.d.d.3
    .2...2...2.
    t.3.....3.t
    """.split(),

    15: """
    ...3..t.t..3...
    ..d..2...2..d..
    .d..d.....d..d.
    3..t...2...t..3
    ..d...d.d...d..
    .2...t...t...2.
    t...d.....d...t
    ...2.......2...
    t...d.....d...t
    .2...t...t...2.
    ..d...d.d...d..
    3..t...2...t..3
    .d..d.....d..d.
    ..d..2...2..d..
    ...3..t.t..3...
    """.split()
  }

  letter_values = {
    'en': [1,4,4,2,1,4,3,3,1,10,5,2,4,2,1,4,10,1,1,1,2,5,4,8,3,10],
    'fr': [1,5,4,3,1,4,5,3,1,10,10,2,4,1,1,4,10,1,1,1,2,8,10,10,10,8]
  }

  def letter_value(self, c):
    assert c >= 'A' and c <= 'Z'
    return self.letter_values[self.LANGUAGE][ord(c) - ord('A')]

  def board_property(self, r, c):
    return self.BOARDSTRS[self.SIZE][r][c]

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
