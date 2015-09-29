
def powerset(iterable):
  from itertools import chain, combinations
  xs = list(iterable)
  return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )

def nub_and_sort_by_length(xs):
  return sorted(list(set(xs)), cmp=lambda x,y:1 if len(x)>len(y) else -1)

class Dictionary:
  """
  Dictionary. Handles checking valid words and finding anagrams.
  We don't really care about letter score here.
  """
  def __init__(self, wordlist):
    self.word_list = open(wordlist,'r').read().split()
    self.word_set = set(self.word_list)

    # Data structure for easy anagramming. Basically store each word
    # as a sorted word bag as its canonical form.
    self.anagram_dict = {}
    for w in self.word_list:
      ws = ''.join(sorted(w))
      if ws not in self.anagram_dict:
        self.anagram_dict[ws] = [w]
      else:
        self.anagram_dict[ws].append(w)
  
  def check_word(self, w):
    # Checks if string is a word in our dictionary
    return w in self.word_set

  def anagrams(self, w):
    # Find full anagrams (using all letters of a word)
    ws = ''.join(sorted(w))
    if ws in self.anagram_dict:
      return self.anagram_dict[ws]
    else:
      return []

  def sub_anagrams(self, w):
    # Find sub-anagrams (using some subsets of a word)
    ans = []
    for wp in powerset(w):
      ws = ''.join(sorted(wp))
      ans.extend(self.anagrams(ws))
    return nub_and_sort_by_length(ans)

  def sub_anagrams_blank(self, w):
    # assume 1 blank
    ans = []
    b = 'a'
    while b <= 'z':
      ans.extend(sub_anagrams(''.join(w+b)))
      b = chr(ord(b)+1)
    return nub_and_sort_by_length(ans)
