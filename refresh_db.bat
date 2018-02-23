DEL "db.sqlite3"
python manage.py migrate
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'cakeisalie') | python manage.py shell