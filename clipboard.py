import os
from manatoki.config import Config
from tkinter import Tk, Label, RAISED
import pyperclip
from urllib.parse import urlparse, parse_qs

clip = ''


def addClipToText(str):
  global clip
  if (clip == str):
    return
  config = Config()
  if 'manatoki' not in str:
    return
  clip = str
  # q = parse_qs(urlparse(str).query).get('manga_id')
  a = clip.split('/')
  last = a[len(a) - 1].split('?')
  id = last[0]
  print("ID : " + id)
  f = open("list.txt", "a")
  f.write(id + "\r")
  f.close()


def updateClipboard():
  cliptext = pyperclip.paste()
  processClipping(cliptext=cliptext)
  addClipToText(cliptext)
  root.after(ms=100, func=updateClipboard)


def processClipping(cliptext):
  cliptextCleaned = cleanClipText(cliptext=cliptext)
  label["text"] = cliptextCleaned


def cleanClipText(cliptext):
  # Removing all characters > 65535 (that's the range for tcl)
  cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
  return cliptext


def onClick(labelElem):
  labelText = labelElem["text"]
  print(labelText)
  pyperclip.copy(labelText)


def loadConfig():
  defaultIni = "manatoki.ini"
  if os.path.exists(defaultIni):
    config = Config()
    config.loadConfig(defaultIni)
    print(config.getDomain())


if __name__ == '__main__':
  root = Tk()
  label = Label(root, text="", cursor="plus",
                relief=RAISED, pady=5,  wraplength=500)
  label.bind("<Button-1>", lambda event, labelElem=label: onClick(labelElem))
  label.pack()
  loadConfig()
  updateClipboard()
  root.mainloop()
