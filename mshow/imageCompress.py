######
# 이미지를 압축해 준다.
from PIL import Image as PILImage
import os


def __convert(image_path):
  try:
    source = PILImage.open(image_path)
    source.save(image_path, quality=95, optimize=True)
  except:
    return


def imagesCompress(savePath):
  for f in os.listdir(savePath):
    fname = os.path.join(savePath, f)
    __convert(fname)


if __name__ == "__main__":
  imagesCompress("...")
