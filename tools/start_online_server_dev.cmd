REM need call from project top
CALL .\tools\emurater_env.cmd
cd .\online_server
uvicorn main:app --reload