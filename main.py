from dictionary import Dictionary
from board_solve import BoardSolve
import sys

wdict = Dictionary('wordlist.txt')
boardsv = BoardSolve(wdict)

def solve_from_file(filename):
  f = open(filename, 'r')
  size = int(f.readline())
  board = []
  for r in xrange(size):
    board.append(f.readline()[:-1])
  rack = f.readline()

  boardsv.solve(board, rack)


def main():
  if len(sys.argv) != 2:
    print 'Need to specify input file!'
  else:
    solve_from_file(sys.argv[1])


if __name__ == '__main__':
  main()
