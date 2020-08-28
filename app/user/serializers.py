from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_style': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authentication the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            raise serializers.ValidationError(
                'Unable to authenticate with provided creadentials',
                code='authentication'
            )
        attrs['user'] = user
        return attrs