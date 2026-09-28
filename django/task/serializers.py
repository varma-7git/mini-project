import re

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            "name",
            "email",
            "username",
            "password",
            "confirm_password"
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Name is required."
            )

        return value

    def validate_username(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Username is required."
            )

        if User.objects.filter(
            username__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):

        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError(
                "Email is required."
            )

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_password(self, value):

        if not re.search(
            r"[A-Z]",
            value
        ):

            raise serializers.ValidationError(
                "Password must contain an uppercase letter."
            )

        if not re.search(
            r"[a-z]",
            value
        ):

            raise serializers.ValidationError(
                "Password must contain a lowercase letter."
            )

        if not re.search(
            r"[0-9]",
            value
        ):

            raise serializers.ValidationError(
                "Password must contain a number."
            )

        if not re.search(
            r"[^A-Za-z0-9]",
            value
        ):

            raise serializers.ValidationError(
                "Password must contain a special character."
            )

        validate_password(value)

        return value

    def validate(self, data):

        if (
            data["password"]
            !=
            data["confirm_password"]
        ):

            raise serializers.ValidationError({
                "confirm_password":
                "Passwords do not match."
            })

        return data

    def create(self, validated_data):

        name = validated_data.pop(
            "name"
        )

        validated_data.pop(
            "confirm_password"
        )

        password = validated_data.pop(
            "password"
        )

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=password,
            first_name=name
        )

        user.is_staff = False

        user.save()

        return user