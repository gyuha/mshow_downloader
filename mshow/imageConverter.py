import math
import os
from PIL import Image as PILImage

_seed = 1
_CX = 5
_CY = 5


def __vertor(chapter):
    global _seed
    if chapter < 554714:
        e = 10000 * math.sin(_seed)
        _seed = _seed + 1
        return math.floor(100000 * (e - math.floor(e)))

    _seed = _seed + 1
    mSin = 100 * math.sin(10 * _seed)
    mCos = 1000 * math.cos(13 * _seed)
    mTan = 10000 * math.tan(14 * _seed)
    mSin = math.floor(100 * (mSin - math.floor(mSin)))
    mCos = math.floor(1000 * (mCos - math.floor(mCos)))
    mTan = math.floor(10000 * (mTan - math.floor(mTan)))

    return mSin + mCos + mTan


def __convert(image_path, chapter, seed):
    # 책의 이미지를 섞어 둔걸 원복 하는 코드
    global _seed, _CX, _CY
    _seed = math.floor(seed/10)
    order = []

    for i in range(_CX * _CY):
        order.append([i, __vertor(chapter)])
    order = sorted(order, key=lambda x: x[1])
    try:
        source = PILImage.open(image_path)
        width, height = source.size
        canvas = PILImage.new('RGB', source.size, 'white')
        cropWidth = math.floor(width/_CX)
        cropHeight = math.floor(height/_CY)
        i = 0
        for o in order:
            imgX = (i % _CX) * cropWidth
            imgY = math.floor(i/_CX) * cropHeight
            x = (o[0] % _CX) * cropWidth
            y = (math.floor(o[0] / _CX)) * cropHeight
            img = source.crop((imgX, imgY, imgX + cropWidth, imgY+cropHeight))
            canvas.paste(img, (x, y))
            i = i + 1
        canvas.save(image_path)
    except Exception as e:
        print(e)
        return


def convertImages(savePath, chapter, seed):
    global _CX, _CY
    if seed / 10 > 30000:
        _CX = 1
        _CY = 6
    elif seed / 10 > 20000:
        _CX = 1
    elif seed / 10 > 10000:
        _CY = 1
    else:
        _CX = 5
        _CY = 5

    for f in os.listdir(savePath):
        fname = os.path.join(savePath, f)
        __convert(fname, chapter, seed)


if __name__ == "__main__":
    __convert("test.jpg", 554724, 24520)
