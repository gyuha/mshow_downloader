import os

# 파일에서 다운로드 목록 받아오기


def downloadList(filename):
  print(filename)
  readList = []
  with open(filename, "r", encoding="utf-8-sig") as readFile:
    for line in readFile:
      line = line.strip()
      if len(line) > 0:
        readList.append(line)

  return readList
