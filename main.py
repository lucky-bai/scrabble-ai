from dictionary import Dictionary
from boardsolve import BoardSolve

wdict = Dictionary('wordlist.txt')
board = BoardSolve(wdict)

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

def main():
  #print form_with_board('auib', 'vye')
  board.solve('hsadiaa')


if __name__ == '__main__':
  main()
