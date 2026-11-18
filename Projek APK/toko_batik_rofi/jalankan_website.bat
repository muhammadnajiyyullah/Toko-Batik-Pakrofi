@echo off
cd /d "%~dp0"
echo Memasang dependensi (jika belum ada)...
python -m pip install -r requirements.txt
echo.
echo Menjalankan website Toko Batik Rofi di http://127.0.0.1:5000
python app.py
pause
