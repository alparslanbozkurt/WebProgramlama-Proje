from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from accounts.serializers import LoginSerializer, RegisterSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def csrf_token(request):
    """
    GET /api/accounts/csrf/
    Sadece CSRF çerezini set eder.
    """
    return JsonResponse({"detail": "CSRF cookie set"})

class RegisterView(generics.GenericAPIView):
    """
    POST /api/accounts/register/
    Yeni kullanıcı kaydı.
    """
    permission_classes = [AllowAny] 
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"id": user.id, "username": user.username},
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """
    POST /api/accounts/login/
    Kullanıcı doğrulaması yapar ve session cookie set eder.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # --- Session'a kullanıcı bilgilerini yaz ---
        request.session['user_id']  = data['user_id']
        request.session['username'] = data['username']
        # ---------------------------------------------

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/accounts/logout/
    Oturumu sonlandırır (session flush).
    """
    permission_classes = [AllowAny] 
    def post(self, request):
        request.session.flush()
        return Response(
            {"detail": "Başarıyla çıkış yapıldı."},
            status=status.HTTP_200_OK
        )
