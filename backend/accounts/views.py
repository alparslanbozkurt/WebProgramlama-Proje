from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from accounts.serializers import LoginSerializer, RegisterSerializer
from django.http        import JsonResponse
from django.views.decorators.http import require_POST

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
@require_POST
def csrf_test(request):
    return JsonResponse({'ok': True})