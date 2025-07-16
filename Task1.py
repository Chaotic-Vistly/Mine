def palindrome(word):

  word = word.replace(" ", "").lower()

  reversed_string = word[::-1]

  return word == reversed_string

a = str(input("Input a word here:"))
print(palindrome(a))
