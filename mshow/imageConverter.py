import math
from PIL import Image as PILImage

_seed = 1
_CX = 5
_CY = 5

def vertor(chapter):
    global _seed
    if chapter < 554714:
        e = 10000 * math.sin(_seed)
        return math.floor(100000 * (e - math.floor(e)))

    _seed = _seed + 1
    mSin = 100 * math.sin(10 * _seed)
    mCos = 1000 * math.cos(13 * _seed)
    mTan = 10000* math.tan(14 * _seed)
    mSin = math.floor(100 * (mSin - math.floor(mSin)))
    mCos = math.floor(1000 * (mCos - math.floor(mCos)))
    mTan = math.floor(10000 * (mTan - math.floor(mTan)))

    return mSin + mCos + mTan

def convert(image_path, chapter, seed):
    global _seed, _CX, _CY
    _seed = math.floor(seed/10)
    order = []
    
    for i in range(_CX * _CY):
        order.append([i, vertor(chapter)])
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
            img = source.crop((imgX,imgY,imgX + cropWidth,imgY+cropHeight))
            canvas.paste(img, (x, y))
            i = i + 1
        canvas.save(image_path)
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    convert("test.jpg", 554724, 24520)