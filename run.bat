@echo off
REM Quick Start Script for Login Security Classifier
REM Navigate to the project directory

cd /d d:\csvmy

echo.
echo ========================================
echo  Login Security Classifier System
echo ========================================
echo.
echo Choose what to run:
echo.
echo 1. Run Company Login Website (Flask - Port 5000)
echo 2. Run Streamlit Classifier App
echo 3. Train the Model
echo 4. Generate New Dataset
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting Flask Web Server...
    echo Open browser to: http://localhost:5000
    echo.
    .\venv\Scripts\python app.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Streamlit App...
    echo Open browser to: http://localhost:8501
    echo.
    .\venv\Scripts\streamlit run app_streamlit.py
) else if "%choice%"=="3" (
    echo.
    echo Training the model...
    echo.
    .\venv\Scripts\python train_model.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo Generating new dataset...
    echo.
    .\venv\Scripts\python generated_login_dataset.py
    pause
) else if "%choice%"=="5" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto start
)

pause
