from tkinter import Tk, Label, RAISED
import pyperclip
from urllib.parse import urlparse, parse_qs

clip = ''

def addClipToText(str):
  global clip
  if (clip == str):
    return
  if "manamoa" not in str and "manga_id" not in str:
    return
  clip = str
  q = parse_qs(urlparse(str).query).get('manga_id')
  f = open("list.txt", "a")
  f.write(q[0] + "\r")
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
  #Removing all characters > 65535 (that's the range for tcl)
  cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
  return cliptext

def onClick(labelElem):
  labelText = labelElem["text"]
  print(labelText)
  pyperclip.copy(labelText)

if __name__ == '__main__':
  root = Tk()
  label = Label(root, text="", cursor="plus", relief=RAISED, pady=5,  wraplength=500)
  label.bind("<Button-1>", lambda event, labelElem=label: onClick(labelElem))
  label.pack()
  updateClipboard()
  root.mainloop()