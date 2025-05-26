from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

User = get_user_model()

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Kullanıcı adı zaten mevcut.")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanılıyor.")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user

    @staticmethod
    def verify_credentials(username: str, password: str):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("Kullanıcı bulunamadı.")

        if not check_password(password, user.password):
            raise ValidationError("Şifre yanlış.")

        return user
