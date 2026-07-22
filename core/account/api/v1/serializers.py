from account.models import User, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from functions import send_email_function, generate_token


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=False)
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(
        max_length=255,
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords must match"})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        birth_date = validated_data.pop("birth_date", None)

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
        )

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        request = self.context.get('request')

        if username and password:

            user = authenticate(request=request,
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_verified:
                msg = _('Please verify your email and try again.')

                token = generate_token(user)
                active_link = 'http://127.0.0.1:8000/'
                active_link = active_link + 'account/api/v1/token/jwt/verify_account/'
                active_link = active_link + '?token=' + token

                send_email_function(['mehran613.niakan@gmail.com'],
                                    'blog@info.com',
                                    'account verify',
                                    message="None",
                                    email_type='html',
                                    template='emails/account_verify.tpl',
                                    context={
                                        'user': user,
                                        'activation_link': active_link
                                    }
                                    )

                raise serializers.ValidationError(msg, code='authorization', )

            if not user.is_active:
                msg = _('Your account has been disabled.')
                raise serializers.ValidationError(msg, code='authorization', )

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class JwtSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(request=request,
                            username=username, password=password)
        data = super().validate(attrs)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        if not user.is_verified:
            msg = _('Please verify your email and try again.')

            token = generate_token(self.user)
            active_link = 'http://127.0.0.1:8000/'
            active_link = active_link+'account/api/v1/token/jwt/verify_account/'
            active_link = active_link+'?token=' + token
            send_email_function(['mehran613.niakan@gmail.com'],
                                'blog@info.com',
                                'account verify',
                                message="None",
                                email_type='html',
                                template='emails/account_verify.tpl',
                                context={
                                    'user': self.user,
                                    'activation_link': active_link
                                }
                                )
            raise serializers.ValidationError(msg, code='authorization', )

        if not user.is_active:
            msg = _('Your account has been disabled.')
            raise serializers.ValidationError(msg, code='authorization', )

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["email"] = attrs["email"]

        User.objects.filter(id=self.user.id).update(last_login=timezone.now())

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Old Password is Wrong"}
            )

        try:
            validate_password(attrs["new_password"], user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "first_name",
            "last_name",
            "birth_date",
        ]
        read_only_fields = ["id", "email", "is_active", "is_staff"]
