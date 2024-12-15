import os

from helper import ask





while True:
  query=input('Enter your query: ').lower()
  if query=='exit' or query=='quit':
    break

  answer=ask(query)
  print(answer)
