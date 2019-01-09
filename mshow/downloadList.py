import os

# 파일에서 다운로드 목록 받아오기
def downloadList(filename):
    print(filename)
    readList = []
    with open(filename, "r", encoding="utf8") as readFile:
        readList = readFile.readlines()
    
    downList = []
    for l in readList:
        l = l.strip()
        if len(l) > 0:
            downList.append(l)
    return downList