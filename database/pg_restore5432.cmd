:: set default code page
chcp 1251 > nul
SET LANGUAGE=en

App\PgSQL\bin\psql.exe --dbname=udse --host=127.0.0.1 --port=5432 --username=postgres < udse.sql
PAUSE
