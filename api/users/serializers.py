from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio', required=False, allow_blank=True)
    image = serializers.ImageField(source='profile.image', required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", 'bio', 'image']
        extra_kwargs = {
            'password': {'write_only': True}
            }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        # Inherit fields and model from UserSerializer
        extra_kwargs = {
            'password': {'write_only': True},  # Prevent password updates
            'email': {'read_only': True},  # Prevent email updates
            'username': {'required': False},  # Make optional during updates
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        # Extract profile data from validated_data
        if 'password' in validated_data:
            raise serializers.ValidationError({"password": "Updating password is not allowed"})

        profile_data = {
            'bio': validated_data.pop('profile', {}).get('bio', instance.profile.bio),
            'image': validated_data.pop('profile', {}).get('image', instance.profile.image),
        }

        # Update the User instance (excluding email and password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the Profile instance
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # Can be email or username
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("identifier")
        password = data.get("password")

        # Check if identifier is an email
        user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")

