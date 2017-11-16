# no_dev_fee

This is bitcoin no dev fee tool, support all use stratum protocol miner, such as eth, etc, zec, sc.
 
We use [pydivert](https://pypi.python.org/pypi/pydivert/2.0.1) capture and inject miner network packet  with user bitcoin address replacing dev address.

package exe: 
```bash
  pip install pyinstaller
  pyinstaller no_dev_fee.py -F -i logo.ico
```

```py
# !Notice before package, we must modify C:\Python27\Lib\site-packages\pydivert\windivert_dll\__init__.py 35 line
# In this way, we can load WinDivert64.dll in current path avoid pyinstaller dll bug.

if platform.architecture()[0] == "64bit":
    #DLL_PATH = os.path.join(here, "WinDivert64.dll")
    DLL_PATH = "WinDivert64.dll"
else:
    #DLL_PATH = os.path.join(here, "WinDivert32.dll")
   DLL_PATH = "WinDivert32.dll"
```


### usage

```bash
python no_dev_fee.py {coin_adress} {stratum_port}

# eg:
python no_dev_fee.py t1T3Q9rdqR8jWk4g7yaWoDKa2dcyG8QLcgU 3329
```
