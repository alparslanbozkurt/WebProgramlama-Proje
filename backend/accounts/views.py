# backend/accounts/views.py

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import RegisterSerializer, LoginSerializer


@ensure_csrf_cookie
def csrf_token(request):
    """
    GET /api/accounts/csrf/
    Bu endpoint, sadece tarayıcıya CSRF çerezini set eder.
    İstemcide (Vue’da) sayfa açıldığında bu URL’ye bir GET atarak
    X-CSRFToken çerezi tarayıcıya düşürülür.
    """
    return JsonResponse({"detail": "CSRF cookie set"})


class RegisterView(generics.GenericAPIView):
    """
    POST /api/accounts/register/
    Yeni kullanıcı oluşturur. Yalnızca AllowAny (oturumsuz) erişim izni var.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = {
            'user_id': user.id,
            'username': user.username
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    POST /api/accounts/login/
    Kullanıcı adı + şifre doğrulaması yapar. 
    Eğer authenticate başarılıysa, django_login() ile session oluşturur,
    client’a sadece temel user bilgilerini (id, username) döner.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        # 1) Serializer ile raw input verisini kontrol et:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2) Authenticate: validated_data içinde kesin "username" ve "password" var.
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Kullanıcı bulunamadı veya şifre yanlış.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Oturum açma (session cookie set etme):
        django_login(request, user)

        # 4) Response: client’a sadece user_id ve username dönebiliriz.
        return Response({
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)


class MeView(APIView):
    """
    GET /api/accounts/me/
    Eğer geçerli bir session cookie (oturum) varsa user bilgilerini döndürür.
    İzin: Sadece IsAuthenticated (yani oturum açıksa).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Bu noktada request.user, authenticate edilmiş user nesnesidir.
        return Response({
            'user_id': user.id,
            'username': user.username
        })


class LogoutView(APIView):
    """
    POST /api/accounts/logout/
    Oturumu sonlandırır (session flush). 
    İzin: Sadece oturum açmış user bu işlemi yapabilir.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return Response({'detail': 'Çıkış yapıldı.'}, status=status.HTTP_200_OK)
