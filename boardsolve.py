GAME1 = """
  ........H..
  .......PA..
  ......ZOEAL
  .......W.G.
  .......D.E.
  ....SIRE.S.
  .......R...
  ...........
  ...........
  ...........
  ...........
  """

GAME2 = """
  ...............
  ...............
  ..............F
  ..............A
  ..............M
  .............BE
  ..........T..L.
  .......VEXED.O.
  .......O..C..W.
  .......T.WHIPS.
  ......GI.O.....
  ......EN.MODERN
  ......AG.E.R...
  ......R..N.A...
  ...POTS....T...
"""

GAME3 = """
  ...........
  ...........
  O...F.....C
  V..ZA.....O
  E..O.UH...R
  RIPOSTES.DE
  B.A....L.E.
  I.N....A.W.
  G.T....MEAL
  .KEY.....X.
  ..D........
"""

GAME4 = """
  ........GO.
  ........OW.
  ........FE.
  .......DE..
  ......HURL.
  .....ZAPS..
  .......E...
  .......DIVA
  ..........X
  ..........I
  ......JAMBS
  """

GAME5 = """
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............
  .......E.......
  .......V.......
  .......I.......
  .......L.......
  ...............
  ...............
  ...............
  ...............
  ...............
"""

class BoardSolve:

  BOARDSIZE = 11
  VISUAL_THRESHOLD = 5

  BOARDSTATE = None

  def __init__(self, wdict):
    self.wdict = wdict
    self.BOARDSTATE = GAME1
    self.VISUAL_THRESHOLD = 5
    
    # Parse board state
    self.BOARDSTATE = self.BOARDSTATE.split()
    self.BOARDSIZE = len(self.BOARDSTATE)

  def square_neighbors(self, sq):
    r = sq[0]
    c = sq[1]
    if r > 0:
      yield (r-1,c)
    if c > 0:
      yield (r,c-1)
    if r < self.BOARDSIZE - 1:
      yield (r+1,c)
    if c < self.BOARDSIZE - 1:
      yield (r,c+1)

  def check_connected(self, board):
    """
    BFS to check that board is connected
    """
    if board[self.BOARDSIZE/2][self.BOARDSIZE/2] == '.':
      return False

    q = []
    q.append((self.BOARDSIZE/2, self.BOARDSIZE/2))
    seen = set()

    while len(q) > 0:
      cur = q[0]
      q = q[1:]
      seen.add(cur)

      for nei in self.square_neighbors(cur):
        if not nei in seen:
          if board[nei[0]][nei[1]] != '.':
            q.append(nei)

    # Now tally up all non empty
    non_empty_count = 0
    for r in board:
      for c in r:
        if c != '.':
          non_empty_count += 1

    connect_count = len(seen)
    return connect_count == non_empty_count

  def score(self, word, pr, pc, vertical, rack=None):
    """
    Try to place a word in a space and return the score it will get.
    Return None if it's invalid.

    For now, return # of letters placed, don't care about scoring
    """
    assert pr >= 0 and pc >= 0 and pr < self.BOARDSIZE and pc < self.BOARDSIZE

    # Step 1: put the word on, error out if conflict
    temp_board = []
    letters_put = []
    for r in self.BOARDSTATE:
      temp_board.append(list(r.lower()))

    if vertical:
      assert pr + len(word) <= self.BOARDSIZE
      for i in range(len(word)):
        cch = temp_board[pr+i][pc]
        if cch == '.' or cch == word[i]:
          temp_board[pr+i][pc] = word[i]
        else:
          return None

        if cch == '.':
          letters_put.append(word[i])

    else:
      assert pc + len(word) <= self.BOARDSIZE
      for i in range(len(word)):
        cch = temp_board[pr][pc+i]
        if cch == '.' or cch == word[i]:
          temp_board[pr][pc+i] = word[i]
        else:
          return None

        if cch == '.':
          letters_put.append(word[i])

    if not self.check_connected(temp_board):
      return None

    # Step 2: verify that everything is a word
    for r in range(self.BOARDSIZE):
      r_str = []
      for c in range(self.BOARDSIZE):
        r_str.append(temp_board[r][c])
      r_str = ''.join(r_str)
      wds = r_str.split('.')
      for w in wds:
        if len(w) >= 2:
          if not self.wdict.check_word(w):
            return None
    for c in range(self.BOARDSIZE):
      c_str = []
      for r in range(self.BOARDSIZE):
        c_str.append(temp_board[r][c])
      c_str = ''.join(c_str)
      wds = c_str.split('.')
      for w in wds:
        if len(w) >= 2:
          if not self.wdict.check_word(w):
            return None

    # check to ensure we're only using rack letters
    if rack is not None:
      for l in letters_put:
        if l not in rack:
          return None

    # Visualize
    if len(letters_put) >= self.VISUAL_THRESHOLD:
      for r in range(self.BOARDSIZE):
        for c in range(self.BOARDSIZE):
          print temp_board[r][c].upper(),
        print ''
      print '---------------------'

    return len(letters_put)
        
  # Try to find the best play given the board state and rack
  def solve(self, rack):
    # (score, word)
    candidates = []

    # try each column and each row
    for r in range(self.BOARDSIZE):
      extra_chars = list(rack)
      for ch in self.BOARDSTATE[r]:
        if ch != '.':
          extra_chars.append(ch.lower())
      extra_chars = list(set(extra_chars))
      words = self.wdict.sub_anagrams(extra_chars)
      # try each one
      for w in words:
        for c in range(self.BOARDSIZE - len(w) + 1):
          cscore = self.score(w, r, c, False, rack)
          if cscore is not None:
            candidates.append((cscore, w))

    for c in range(self.BOARDSIZE):
      extra_chars = list(rack)
      for r in range(self.BOARDSIZE):
        ch = self.BOARDSTATE[r][c]
        if ch != '.':
          extra_chars.append(ch.lower())
      extra_chars = list(set(extra_chars))
      words = self.wdict.sub_anagrams(extra_chars)
      # try each one
      for w in words:
        for r in range(self.BOARDSIZE - len(w) + 1):
          cscore = self.score(w, r, c, True, rack)
          if cscore is not None:
            candidates.append((cscore, w))
    
    candidates = sorted(list(set(candidates)))
    print candidates

