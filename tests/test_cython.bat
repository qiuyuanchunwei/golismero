@echo off
cd ..\golismero
dir /b /s *.py > ..\_tmp.txt
cd ..\plugins
dir /b /s *.py >> ..\_tmp.txt
cd ..
del /s *.pyc > nul 2> nul
del /s *.pyo > nul 2> nul
for /F "tokens=*" %%A in (_tmp.txt) do C:\Python27\python.exe C:\Python27\Scripts\cython.py "%%A"
del _tmp.txt
del /s *.c > nul 2> nul
cd tests