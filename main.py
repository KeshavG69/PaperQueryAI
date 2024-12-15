import os

from helper import ask
import shutil





while True:
  query=input('Enter your query: ').lower()
  if query=='exit' or query=='quit':
    shutil.rmtree('pdf_files')
    break

  answer=ask(query)
  print(answer)
