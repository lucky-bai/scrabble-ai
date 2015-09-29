GAME1 = """
  ...........
  ...........
  ........VON
  ........O..
  ........L..
  .....HIKERS
  .....E....Q
  ...FAX....U
  ANTA.E....A
  ..O..D....D
  ..W....BIOS
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
  ..........C..W.
  .........WHIPS.
  ...............
  ...............
  ...............
  ...............
  ...............
"""

GAME3 = """
  ...........
  ...........
  O..........
  V..Z.......
  E..O.UH....
  RIPOSTES.D.
  B......L.E.
  I......A.W.
  G......MEAL
  .........X.
  ...........
"""

class BoardSolve:

  BOARDSIZE = 11

  # . blank
  # 2,3: double, triple word
  # d,t: double, triple letter
  BOARDSTR = """
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
  """

  BOARDSTATE = """
  ...........
  ...........
  ...........
  ...........
  ...........
  ...RADIO...
  ...........
  ...........
  ...........
  ...........
  ...........
  """

  def __init__(self, wdict):
    self.wdict = wdict
    self.BOARDSTATE = GAME3
    
    # Parse board state
    self.BOARDSTATE = self.BOARDSTATE.split()

  def score(self, word, pr, pc, vertical):
    """
    Try to place a word in a space and return the score it will get.
    Return None if it's invalid.

    For now, return # of letters placed, don't care about scoring
    """
    assert pr >= 0 and pc >= 0 and pr < self.BOARDSIZE and pc < self.BOARDSIZE

    # Step 1: put the word on, error out if conflict
    temp_board = []
    num_put = 0
    is_connected = False
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
          num_put += 1
        if pc > 0 and self.BOARDSTATE[pr+i][pc-1] != '.':
          is_connected = True
        if pc < self.BOARDSIZE-1 and self.BOARDSTATE[pr+i][pc+1] != '.':
          is_connected = True

    else:
      assert pc + len(word) <= self.BOARDSIZE
      for i in range(len(word)):
        cch = temp_board[pr][pc+i]
        if cch == '.' or cch == word[i]:
          temp_board[pr][pc+i] = word[i]
        else:
          return None

        if cch == '.':
          num_put += 1
        if pr > 0 and self.BOARDSTATE[pr-1][pc+i] != '.':
          is_connected = True
        if pr < self.BOARDSIZE-1 and self.BOARDSTATE[pr+1][pc+i] != '.':
          is_connected = True

    if not is_connected:
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

    # Visualize
    if num_put >= 4:
      for r in range(self.BOARDSIZE):
        for c in range(self.BOARDSIZE):
          print temp_board[r][c].upper(),
        print ''
      print '---------------------'

    return num_put
        
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
          cscore = self.score(w, r, c, False)
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
          cscore = self.score(w, r, c, True)
          if cscore is not None:
            candidates.append((cscore, w))
    
    candidates = sorted(list(set(candidates)))
    print candidates

# Use these in our strategy later
letter_values = [1,4,4,2,1,4,2,3,1,10,5,1,3,1,1,3,10,1,1,1,2,5,5,8,5,10]

def word_val(w):
  s = 0
  for c in w:
    s += letter_values[ord(c)-ord('a')]
  return s

