:: set default code page
chcp 1251 > nul
SET LANGUAGE=en

App\PgSQL\bin\pg_dump.exe --dbname=udse --host=127.0.0.1 --port=65432 --username=postgres > udse.sql
PAUSE
