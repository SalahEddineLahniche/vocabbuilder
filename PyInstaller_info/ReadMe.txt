
to install pysintaller the syntaxe in the command line is simply : pip install pyinstaller
of course you will have to install first pip.
if it does not work, please read the documentation in the link : https://pyinstaller.readthedocs.io/en/stable/installation.html#installing-in-windows


now once you've installed pyinstaller, go to the directory of the .py file (named scripts.py for exemple) that you want to distribute and enter the command :
pyinstaller.exe --onefile --debug scripts.py
there are other --options that you can add, you can see that in the documentation (--debug for instance is very important to detect any disfuctions or tracebacks)

You can also install another package of pysintaller containing a pyinstaller.py file, in this case your command would be :
python C:\directory\to\pyinstaller.py --onefile --debug scripts.py












""""""""""" if you use a special module just for your project :you should create a .py file in the same directory as the scripts.py named hook-modulename.py
the hook .py file should contain this statement : hiddenimports=['module name'] """""""""""""""