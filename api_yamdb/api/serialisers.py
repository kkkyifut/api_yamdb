from rest_framework import serializers

from users.models import User
from reviews.models import Review, Comment, Title


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return value


class UserGetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, validators=[])
    confirmation_code = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id', queryset=Review.objects.all(), required=False
    )
    author = serializers.CharField(source='author.username', read_only=True)
    comments = serializers.SlugRelatedField(
        slug_field='text', queryset=Comment.objects.all(),
        many=True, required=False
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
