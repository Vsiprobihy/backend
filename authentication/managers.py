from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, role, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if role not in ['user', 'organizer', 'admin']:
            raise ValueError('Invalid role')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, role='user', **extra_fields):
        extra_fields.setdefault('isStaff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, role, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('isStaff', True)
        extra_fields.setdefault('is_superuser', True)
        role = 'admin'

        if extra_fields.get('isStaff') is not True:
            raise ValueError('Superuser must have isStaff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, role, **extra_fields)
