import math

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
    mTan = 1000* math.tan(14 * _seed)
    mSin = math.floor(100 * (mSin - math.floor(mSin)))
    mCos = math.floor(1000 * (mCos - math.floor(mCos)))
    mTan = math.floor(10000 * (mTan - math.floor(mTan)))

    return mSin + mCos + mTan

def convert(image, seed):
    