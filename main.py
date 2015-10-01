from dictionary import Dictionary
from boardsolve import BoardSolve

wdict = Dictionary('wordlist.txt')
boardsv = BoardSolve(wdict)

def nub_and_sort_by_length(xs):
  return sorted(list(set(xs)), cmp=lambda x,y:1 if len(x)>len(y) else -1)

def form_with_board(rack, board):
  # use any from rack and exactly 1 from board
  if board == '':
    return wdict.sub_anagrams(rack)
  ans = []
  for b in board:
    ws = ''.join(sorted(rack + b))
    ans.extend(wdict.sub_anagrams(ws))
  return nub_and_sort_by_length(ans)

def form_with_board_blank(rack,board):
  ans = []
  b = 'a'
  while b <= 'z':
    ans.extend(form_with_board(''.join(rack+b), board))
    b = chr(ord(b)+1)
  return nub_and_sort_by_length(ans)

def solve_from_file(filename):
  f = open(filename, 'r')
  size = int(f.readline())
  board = []
  for r in xrange(size):
    board.append(f.readline()[:-1])
  rack = f.readline()

  boardsv.solve(board, rack)


def main():
  #print form_with_board('ilseixw', '')
  solve_from_file('testcase/jgfran30.in')


if __name__ == '__main__':
  main()
