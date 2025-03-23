from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **args):
        user = self.model(phone_number=phone_number, **args)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **args):
        args.setdefault("is_staff", True)
        return self.create_user(phone_number, password, **args)