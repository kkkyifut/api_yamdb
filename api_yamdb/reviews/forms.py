from django.forms import ModelForm

from .models import Comment, Review


class ReviewForm(ModelForm):
    """Форма для отзывов."""

    class Meta:
        model = Review
        fields = ('text', 'score',)


class CommentForm(ModelForm):
    """Форма для комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
