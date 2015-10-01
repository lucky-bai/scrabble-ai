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

# Use these in our strategy later
letter_values = [1,4,4,2,1,4,2,3,1,10,5,1,3,1,1,3,10,1,1,1,2,5,5,8,5,10]

def word_val(w):
  s = 0
  for c in w:
    s += letter_values[ord(c)-ord('a')]
  return s
