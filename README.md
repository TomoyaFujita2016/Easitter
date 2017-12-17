# Easitter ver2.0 !!!
Even if your account is frozen by this program, TomoyaFujita2016 assumes no responsibility.
## Requirements
1. python3
2. tweepy
3. tqdm
4. (opencv3) If you'd like to use face detection when you use sc mode, you must install opencv3.

## Usage
```
$ git clone https://github.com/TomoyaFujita2016/Easitter.git
$ cd Easitter
$ pip3 install tweepy tqdm
$ python3 easitter.py
=================================================
==== (´･ω･･`) Welcome to Easitter ! (･Д･｀) ====
=================================================
==== ***Please choose a mode !***
==== 'python3 easitter.py --run [option]'
==== fv: favorite, fl: flatter, sc: scraping,uf: unfollow, fo: follow, fb: followBack
$ python3 easitter.py --help
usage: easitter.py [-h] [--run RUN] [--tag TAG] [--url URL] [-face]

optional arguments:
  -h, --help  show this help message and exit
  --run RUN   Please choose a mode. (fv: favorite, fl: flatter, sc: scraping,
              uf: unfollow, fo: follow, fb: followBack)
  --tag TAG   When you use '--run sc', you can choose search tag. example: '--
              tag cat,dog,mouse' (default: クラフトビール)
  --url URL   Search from hint of image url.
  -face       Detect face

```
As you can see, you can choose MODE and some options.
The following examples are ways to use Easitter !

If you'd like to ...
1. get more followers,
```
$ python3 easitter.py --run fv
```
2. favorite tweets on your timeline,
```
$ python3 easitter.py --run fl
```
3. collect images on twitter,(This example will collect Apple images. you can change after "--tag")
```
$ python3 easitter.py --run sc --tag Apple
```
4. unfollow some bad user in your followers,
```
$ python3 easitter.py --run uf
```
5. follow the users who tweet about what you are interested in,(This example will follow the users who tweet about PC)
```
$ python3 easitter.py --run fo --tag PC
```
6. follow Back some good user,
```
$ python3 easitter.py --run fb
```
