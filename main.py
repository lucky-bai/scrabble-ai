from dictionary import Dictionary
from board_solve import BoardSolve
import sys
import traceback

wdict = Dictionary('wordlist.txt')
boardsv = BoardSolve(wdict)

def solve_from_file(filename):
  f = open(filename, 'r')
  size = int(f.readline())
  board = []
  for r in xrange(size):
    board.append(f.readline()[:-1])

  # Sanitize rack
  rack = []
  has_blank = False
  for c in f.readline().upper()[:-1]:
    if c >= 'A' and c <= 'Z':
      rack.append(c)
    elif c == '?':
      if has_blank:
        raise Exception('Maximum of 1 blank supported!')
      else:
        has_blank = True
    else:
      raise Exception('Invalid character: ' + c)
  
  boardsv.solve(board, rack, has_blank)


def main():
  try:
    if len(sys.argv) != 2:
      raise Exception('Need to specify input file!')
    else:
      solve_from_file(sys.argv[1])
  except Exception, e:
    print traceback.format_exc()


if __name__ == '__main__':
  main()
