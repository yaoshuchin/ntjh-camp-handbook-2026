@echo off
chcp 65001 > nul
echo ========================================================
echo   正在啟動「南投國中 115 二年級隔宿露營行動簡報手冊（去個資版）」...
echo   本機伺服器位址：http://localhost:8080
echo ========================================================
start http://localhost:8080
python -m http.server 8080
pause
