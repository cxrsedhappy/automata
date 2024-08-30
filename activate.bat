@echo off

where conda >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Miniconda are not found in PATH. Please, install Miniconda and add it to PATH.
    exit /b 1
)

CALL conda activate

if not exist "requirements.txt" (
    echo File requirements.txt not found.
    exit /b 1
)

echo Installing dependencies requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error occurred.
    exit /b 1
)

echo Starting Streamlit...
streamlit run main.py --server.enableXsrfProtection false
if %ERRORLEVEL% neq 0 (
    echo Streamlit app error.
    exit /b 1
)

pause