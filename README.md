# MShow downloader



## Description
Download the comics registered on the web site

이 프로젝트를 실행하기 위해서는 Python 3.6.8이 필요 함.
왜 인지를 모르겠음 ㅜ.ㅜ


## Use
### Install files...

#### Windows
파이썬을 3.6.8을 설치해 준다.
pyenv-win으로 설치하면 조금 쉽다.


```cmd
> C:/Users/gyuha/.pyenv/pyenv-win/versions/3.6.8/python.exe -m pip install virtualenv
> C:/Users/gyuha/.pyenv/pyenv-win/versions/3.6.8/python.exe -m virtualenv venv
> .\venv\Scripts\activate.bat
> pip install -r requirements.txt
```


```cmd
> python -m venv venv
> .\venv\Scripts\activate.bat
> pip install -r requirements.txt
```

#### Linux
```bash
$ sudo apt-get install chromium-chromedriver
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

------

## How to use
```cmd
$ python mangashowme.py
```

## Make Install file..
빌드 할 때는 python이 3.6 버전이여야 한다.
```cmd
auto-pi-to-exe
```

Or
```cmd
pyinstaller -y -F "mangashowme.py"
```

## 참고

- [문과생도 할 수 있는 웹 크롤링 (1) - 웹 데이터 크롤링 준비](http://sacko.tistory.com/12)
- [문과생도 할 수 있는 웹 크롤링 (2) - Selenium 사용 준비](http://sacko.tistory.com/13)
- [문과생도 할 수 있는 웹 크롤링 (3) - Selenium 실습 기초](http://sacko.tistory.com/14)
- [문과생도 할 수 있는 웹 크롤링 (4) - Selenium 제대로 사용하기](http://sacko.tistory.com/15)
- [Auto Py To Exe](https://nitratine.net/blog/post/auto-py-to-exe/)
