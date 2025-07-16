import os
import django
from django.core.management import call_command


if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_backend.settings'
django.setup()

from users.models import User
from django.contrib.auth.hashers import make_password

def reset_database():
    
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)

    
    call_command('makemigrations')
    call_command('migrate')

    
    admin_email = 'admin@example.com'
    admin_password = 'admin1234'  

    if User.objects.filter(email=admin_email).exists():
        print(f"Admin user with email {admin_email} already exists.")
    else:
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password,  
            name='Admin User'
        )
        print(f"Admin user created with email: {admin_email}")

if __name__ == '__main__':
    reset_database()
