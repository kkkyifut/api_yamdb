from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

# from .forms import CommentForm, PostForm
from .models import Review, Comment, User


def index(request) -> HttpResponse:
    """view-функция для главной страницы."""
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'index.html', context)


def page_not_found(request, exception):
    return render(
        request, "misc/404.html", {"path": request.path}, status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
