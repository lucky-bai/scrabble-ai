from board_helper import BoardHelper

class BoardSolve:
  VISUAL_THRESHOLD = 4

  def __init__(self, wdict):
    self.wdict = wdict

  def score(self, word, pr, pc, vertical, rack=None):
    """
    Try to place a word in a space and return the score it will get.
    Return None if it's invalid.

    For now, return # of letters placed, don't care about scoring
    """
    assert pr >= 0 and pc >= 0 and pr < self.SIZE and pc < self.SIZE

    # Step 1: put the word on, error out if conflict
    temp_board = []
    letters_put = []
    squares_put = []
    for r in self.BOARD:
      temp_board.append(list(r.lower()))

    if vertical:
      assert pr + len(word) <= self.SIZE
      for i in range(len(word)):
        cch = temp_board[pr+i][pc]
        if cch == '.' or cch == word[i]:
          temp_board[pr+i][pc] = word[i]
        else:
          return None

        if cch == '.':
          letters_put.append(word[i])
          squares_put.append((pr+i,pc))

    else:
      assert pc + len(word) <= self.SIZE
      for i in range(len(word)):
        cch = temp_board[pr][pc+i]
        if cch == '.' or cch == word[i]:
          temp_board[pr][pc+i] = word[i]
        else:
          return None

        if cch == '.':
          letters_put.append(word[i])
          squares_put.append((pr,pc+i))

    # Check connected
    is_connected = False
    for rc in squares_put:
      for nei in self.boardhelper.square_neighbors(rc):
        if self.BOARD[nei[0]][nei[1]] != '.':
          is_connected = True
    if not is_connected:
      return None

    # Step 2: verify that everything is a word
    for r in range(self.SIZE):
      r_str = []
      for c in range(self.SIZE):
        r_str.append(temp_board[r][c])
      r_str = ''.join(r_str)
      wds = r_str.split('.')
      for w in wds:
        if len(w) >= 2:
          if not self.wdict.check_word(w):
            return None
    for c in range(self.SIZE):
      c_str = []
      for r in range(self.SIZE):
        c_str.append(temp_board[r][c])
      c_str = ''.join(c_str)
      wds = c_str.split('.')
      for w in wds:
        if len(w) >= 2:
          if not self.wdict.check_word(w):
            return None

    # check to ensure we're only using rack letters
    rack2 = rack[:]
    if rack2 is not None:
      for l in letters_put:
        if l not in rack2:
          return None
        else:
          rack2.remove(l)

    if len(letters_put) >= self.VISUAL_THRESHOLD:
      self.boardhelper.print_board(temp_board)

    return len(letters_put)

  # Try to find the best play given the board state and rack
  def solve(self, board, rack):
    self.BOARD = board
    self.SIZE = len(board)
    self.boardhelper = BoardHelper(self.SIZE)
    rack = sorted(rack)

    # (score, word)
    candidates = []

    # try each column and each row
    for r in range(self.SIZE):
      extra_chars = list(rack)
      for ch in self.BOARD[r]:
        if ch != '.':
          extra_chars.append(ch.lower())
      words = self.wdict.sub_anagrams(extra_chars)
      # try each one
      for w in words:
        for c in range(self.SIZE - len(w) + 1):
          cscore = self.score(w, r, c, False, rack)
          if cscore is not None:
            candidates.append((cscore, w))

    for c in range(self.SIZE):
      extra_chars = list(rack)
      for r in range(self.SIZE):
        ch = self.BOARD[r][c]
        if ch != '.':
          extra_chars.append(ch.lower())
      words = self.wdict.sub_anagrams(extra_chars)
      # try each one
      for w in words:
        for r in range(self.SIZE - len(w) + 1):
          cscore = self.score(w, r, c, True, rack)
          if cscore is not None:
            candidates.append((cscore, w))
    
    candidates = sorted(list(set(candidates)))
    print candidates

