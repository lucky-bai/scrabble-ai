
# original from http://www.winedt.org/Dict/
lines = open('wordlist-fr.txt','r').readlines()

final_list = []
for w in lines:
  # remove trailing \n
  w = w[:-1]
  w = w.lower()

  # Try our best with random french accents
  w = w.replace(chr(224), 'a') # a down
  w = w.replace(chr(226), 'a') # a hat
  w = w.replace(chr(231), 'c') # cidilla
  w = w.replace(chr(233), 'e') # e up
  w = w.replace(chr(232), 'e') # e down
  w = w.replace(chr(234), 'e') # e hat
  w = w.replace(chr(235), 'e') # e :
  w = w.replace(chr(239), 'i') # i :
  w = w.replace(chr(238), 'i') # i hat
  w = w.replace(chr(244), 'o') # o hat
  w = w.replace(chr(251), 'u') # u hat
  w = w.replace(chr(249), 'u') # u down
  w = w.replace(chr(252), 'u') # u :

  valid = True
  if '-' in w or '\'' in w:
    valid = False

  for c in w:
    if not (c >= 'a' and c <= 'z'):
      valid = False

  if valid:
    final_list.append(w)

# output it
for w in final_list:
  print w
