from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Registration successful.",
                "username": user.username
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):

    login_value = request.data.get(
        "login",
        ""
    ).strip()

    password = request.data.get(
        "password",
        ""
    )

    if not login_value:

        return Response(
            {
                "success": False,
                "message":
                "Email or username is required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if not password:

        return Response(
            {
                "success": False,
                "message":
                "Password is required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = None

    try:

        user = User.objects.get(
            username__iexact=login_value
        )

    except User.DoesNotExist:

        try:

            user = User.objects.get(
                email__iexact=login_value
            )

        except User.DoesNotExist:

            user = None

    if user is None:

        return Response(
            {
                "success": False,
                "message":
                "Invalid email/username or password."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    authenticated_user = authenticate(
        username=user.username,
        password=password
    )

    if authenticated_user is None:

        return Response(
            {
                "success": False,
                "message":
                "Invalid email/username or password."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(
        authenticated_user
    )

    return Response(
        {
            "success": True,
            "message": "Login successful.",

            "access": str(
                refresh.access_token
            ),

            "refresh": str(
                refresh
            ),

            "username":
                authenticated_user.username,

            "email":
                authenticated_user.email,

            "name":
                authenticated_user.first_name,

            "is_staff":
                authenticated_user.is_staff
        },
        status=status.HTTP_200_OK
    )