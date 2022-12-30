from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail


class AppUsersManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),  # undo capitalize letter
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    # def email_user(self, *args, **kwargs):
    #     send_mail(
    #         '{}'.format(args[0]),
    #         '{}'.format(args[1]),
    #         '{}'.format(args[2]),
    #         [self.email],
    #         fail_silently=False,
    #     )
