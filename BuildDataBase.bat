del db.sqlite3
py -2 manage.py makemigrations
py -2 manage.py migrate --run-syncdb
py -2 manage.py shell 
