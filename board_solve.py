from board_helper import BoardHelper

class BoardSolve:

  def __init__(self, wdict, language):
    self.wdict = wdict
    self.LANGUAGE = language

  def put_word(self, word, pr, pc, vertical, is_first_move):
    """
    Put word on the board, return None if conflicts with something already
    there. Return board after putting word on it.
    
    Don't check for word validity.
    Do check that board is still connected.
    """
    temp_board = []
    letters_put = []
    squares_put = []
    for r in self.BOARD:
      temp_board.append(list(r.upper()))

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
      for nei in self.board_helper.square_neighbors(rc):
        if self.BOARD[nei[0]][nei[1]] != '.':
          is_connected = True
    
    if is_first_move:
      if temp_board[self.SIZE/2][self.SIZE/2] == '.':
        return None
    else:
      if not is_connected:
        return None

    return letters_put, temp_board

  def add_candidate_play(self, score, play_info, play_board):
    """
    play_info: struct containing all information to reconstruct this play
    play_board: board state after this play
    """
    self.candidate_plays.append((score, play_info, play_board))

  def display_top_candidate_plays(self, limit):
    """ Get n top plays """
    self.candidate_plays = sorted(self.candidate_plays, reverse=True)
    for x in xrange(min(len(self.candidate_plays),limit)-1,-1,-1):
      score, play_info, play_board = self.candidate_plays[x]
      print score, play_info
      self.board_helper.print_board(play_board)

  def score(self, word, pr, pc, vertical, rack=None,
      has_blank=False, is_first_move=False):
    """
    Try to place a word in a space and return the score it will get.
    Return None if it's invalid.

    For now, return # of letters placed, don't care about scoring
    """
    assert pr >= 0 and pc >= 0 and pr < self.SIZE and pc < self.SIZE

    # Step 1: put the word on, error out if conflict
    put_result = self.put_word(word, pr, pc, vertical, is_first_move)
    if put_result is None:
      return None
    letters_put, temp_board = put_result

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
    if not has_blank:
      rack2 = rack[:]
      if rack2 is not None:
        for l in letters_put:
          if l not in rack2:
            return None
          else:
            rack2.remove(l)

    # Step 3: score the word
    existing_words = self.board_helper.words_on_board(self.BOARD)
    current_words = self.board_helper.words_on_board(temp_board)
    new_words = current_words.difference(existing_words)

    tot_score = 0
    for w, start, vrt in new_words:
      positions = []
      for ix in xrange(len(w)):
        if vrt:
          positions.append((start[0]+ix, start[1]))
        else:
          positions.append((start[0], start[1]+ix))

      w_score = 0
      w_multiplier = 1
      for psr, psc in positions:
        cur_ch = temp_board[psr][psc]
        cur_ch_score = self.board_helper.letter_value(cur_ch)

        # Logic for special bonus squares
        if self.BOARD[psr][psc] == '.':
          if self.board_helper.board_property(psr,psc) == '2':
            w_multiplier *= 2
          if self.board_helper.board_property(psr,psc) == '3':
            w_multiplier *= 3
          if self.board_helper.board_property(psr,psc) == 'd':
            cur_ch_score *= 2
          if self.board_helper.board_property(psr,psc) == 't':
            cur_ch_score *= 3

        w_score += cur_ch_score

      w_score *= w_multiplier
      tot_score += w_score

    # Bingo bonus
    if len(letters_put) == 7:
      tot_score += 35

    self.add_candidate_play(tot_score, [w[0] for w in new_words], temp_board)


  def solve(self, board, rack, has_blank=False):
    """
    Try to find the best play given the board state and rack
    has_blank: put to true to indicate extra blank tile (max 1)
    """
    self.BOARD = board
    self.SIZE = len(board)
    self.board_helper = BoardHelper(self.SIZE, self.LANGUAGE)
    self.candidate_plays = []
    rack = sorted(rack)

    # is the whole board blank?
    is_first_move = True
    for r in range(self.SIZE):
      for ch in self.BOARD[r]:
        if ch != '.':
          is_first_move = False

    # try each column and each row
    for r in range(self.SIZE):
      extra_chars = list(rack)
      for ch in self.BOARD[r]:
        if ch != '.':
          extra_chars.append(ch.upper())
      words = self.wdict.sub_anagrams(extra_chars, has_blank)
      # try each one
      for w in words:
        for c in range(self.SIZE - len(w) + 1):
          self.score(w, r, c, False, rack, has_blank, is_first_move)

    for c in range(self.SIZE):
      extra_chars = list(rack)
      for r in range(self.SIZE):
        ch = self.BOARD[r][c]
        if ch != '.':
          extra_chars.append(ch.upper())
      words = self.wdict.sub_anagrams(extra_chars, has_blank)
      # try each one
      for w in words:
        for r in range(self.SIZE - len(w) + 1):
          self.score(w, r, c, True, rack, has_blank, is_first_move)
    
    self.display_top_candidate_plays(40)

