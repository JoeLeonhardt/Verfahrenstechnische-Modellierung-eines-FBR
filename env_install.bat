@echo off
echo Setup des virtuellen Enviroments für Python
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Virtuelle Umgebung und Abhängigkeiten installiert!
pause