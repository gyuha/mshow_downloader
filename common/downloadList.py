import os


def count_file_lines_and_first_line(filename):
    count = 0
    first = ""
    with open(filename, "r", encoding="utf-8") as read_file:
        for line in read_file:
            if count == 0:
                first = line
            count += 1
    return [count, first]


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


def saveListFile(filename, removeId):
    new_list = downloadList(filename)
    filename = os.path.join(os.getcwd(), filename)
    with open(filename, "w", encoding="utf-8") as writeFile:
        for line in new_list:
            if line.strip() == removeId.strip():
                continue
            writeFile.write(line + "\n")


def save_update_list(filename, update_list):
    with open(filename, "wa", encoding="utf-8") as write_file:
        for line in update_list:
            write_file.write(line + "\n")
