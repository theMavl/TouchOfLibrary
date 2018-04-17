DEL "db.sqlite3"
python manage.py migrate
echo from library.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'cakeisalie') | python manage.py shell