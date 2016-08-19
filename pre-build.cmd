if "%1" == "b" (
python pre-build.py -b
)
if "%1" == "p" (
python pre-build.py -p -b
)
if "%1" == "m" (
python pre-build.py -b -p -m
)
python main.py
