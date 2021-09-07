from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, ReviewForm
from .models import Review, Comment, User


def index(request) -> HttpResponse:
    """view-функция для главной страницы."""
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'index.html', context)


# def title_view(request, username, title_id) -> HttpResponse:
    # """view-функция для просмотра постера"""


def review_view(request, username, review_id) -> HttpResponse:
    """view-функция для просмотра отзыва."""
    review = get_object_or_404(Review, id=review_id, author__username=username)
    comments = Comment.objects.filter(review=review)
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_anonymous:
        form = CommentForm()
    else:
        comment = Comment(author=request.user, review=review)
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            comment.save()
            return HttpResponseRedirect(
                reverse('reviews:review', args=(review.author, review.pk))
            )
    context = {
        'author': review.author, 'review': review,
        'form': form, 'page': page,
    }
    return render(request, 'reviews/review.html', context)


@login_required
def new_review(request) -> HttpResponse:
    """view-функция для создания нового отзыва."""
    review = Review(author=request.user)
    form = ReviewForm(
        request.POST or None, instance=review
    )
    if form.is_valid():
        review.save()
        return HttpResponseRedirect(reverse('reviews:index'))
    context = {'author': request.user, 'review': review, 'form': form}
    return render(request, 'reviews/review_edit.html', context)


@login_required
def review_edit(request, username, review_id):
    """view-функция для редактирования отзыва."""
    review = get_object_or_404(Review, id=review_id, author__username=username)
    form = ReviewForm(
        request.POST or None, instance=review
    )
    if request.user != review.author:
        return HttpResponseRedirect(
            reverse('reviews:review', args=(review.author, review.pk))
        )
    if form.is_valid():
        review.save()
        return HttpResponseRedirect(
            reverse('reviews:review', args=(review.author, review.pk))
        )
    context = {'author': request.user, 'review': review, 'form': form}
    return render(request, 'reviews/review_edit.html', context)


@login_required
def delete_review(request, username, review_id) -> HttpResponse:
    """view-функция для удаления поста"""
    author = get_object_or_404(User, username=username)
    if author == request.user:
        review = get_object_or_404(
            Review, id=review_id, author__username=username)
        review.delete()
    return HttpResponseRedirect(
        reverse('reviews:index', args=(author,))
    )


@login_required
def delete_comment(request, username, review_id, comment_id) -> HttpResponse:
    """view-функция для удаления комментария"""
    author = get_object_or_404(User, username=username)
    if author == request.user:
        review = get_object_or_404(
            Review, id=review_id, author__username=username
        )
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
    return HttpResponseRedirect(
        reverse('reviews:review', args=(review.author, review.pk))
    )


def page_not_found(request, exception):
    return render(
        request, 'misc/404.html', {'path': request.path}, status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
