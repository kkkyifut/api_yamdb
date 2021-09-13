from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ["id"]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ["id"]


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"


class TitleRatingSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True, many=False
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя дважды оставить отзыв на одно произведение'
            )
        return data

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'title', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True, many=False
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'review', 'pub_date')
