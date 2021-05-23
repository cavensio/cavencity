# Cavencity



## Build

Install requirements:
```shell
pip install -r requirements.txt
```

Build executable application:
```shell
pyinstaller --icon=cavencity.ico --add-data="cavencity.ico;." --add-data="cavencity.ini;." cavencity.py
```
Possible addition`al options
- `--onefile`
- `--noconsole`
