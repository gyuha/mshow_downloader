import os


def downloadList(filename):
    # 파일에서 다운로드 목록 받아오기
    print(filename)
    readList = []
    with open(filename, "r", encoding="utf-8") as readFile:
        for line in readFile:
            line = line.strip()
            if len(line) > 0:
                readList.append(line)

    return readList


def saveListFile(filename, downloadList):
    print('📢[downloadList.py:17]:', filename)
    filename = os.path.join(os.getcwd(), filename)
    with open(filename, "w", encoding="utf-8") as writeFile:
        for line in downloadList:
            writeFile.write(line + "\n")
