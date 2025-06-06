from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from movies.models import Genre
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Kayıt işlemi için ModelSerializer.
    Kullanıcı yaratma işlemi, create_user() aracılığıyla yapılacak.
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # create_user metodu, password hashing dahil tüm işlemleri yapar.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', None),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Login işlemi için basit Serializer.
    Burada validate() metodu sadece girdi verisinin (username,password)
    DRF tarafından kontrol edilmesini sağlar; authenticate() metodu View'de çağrılacak.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Tüm incoming alanların varlığı kontrol edilir (DRF otomatik).
        Sadece raw data’yı geri döndürüyoruz, 
        gerçek kullanıcı doğrulamasını View katmanında authenticate() ile yapacağız.
        """
        return data
    
class FavoriteGenresSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source='favorite_genres'
    )

    class Meta:
        model = CustomUser
        fields = ['genres']
