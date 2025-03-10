from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ResetPwdSerializer
from rest_framework import status


class LoginView(APIView):
    def post(self, request):
        # 1. 验证数据是否可用
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({"token": token, "user": UserSerializer(user).data})
        else:
            detail = list(serializer.errors.values())[0][0]
            # drf在返回响应是非200的时候，错误参数名叫detail，所以这里也叫detail
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedRequiredView:
    permission_classes = [IsAuthenticated]


class ResetPwdView(APIView):
    def post(self, request):

        # request：是DRF封装的，rest_framework.request.Request
        # 这个对象是针对django的HttpRequest对象进行了封装
        serializer = ResetPwdSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            pwd1 = serializer.validated_data.get("pwd1")
            request.user.set_password(pwd1)
            request.user.save()
            return Response()
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
