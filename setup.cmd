@ECHO OFF
cd %~dp0
IF NOT EXIST %~dp0\venv\Scripts\activate.bat (
    echo Virtualenv directory not found.
    pip install virtualenv 1> nul
    echo Setting up venv.
    virtualenv venv
) ELSE (
    echo Virtualenv directory found.
)
echo Activating virtualenv.
call venv\Scripts\activate.bat
echo Installing requirements.
pip install -r requirements.txt
echo Runserver on port 5000
python src\app.py
