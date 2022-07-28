from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):
    """
    Widok wszystkich opublikowanych postów.

    :param request:
    :return: witryna http wyświetlająca posty.
    """
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    """
    Widok wyświetlający szczegóły posta. Pobiera odpowiednie dane, aby wyświetlić post o podanym slug i dacie.

    :param request:
    :param year: int - rok
    :param month: int - miesiąc
    :param day: int - dzień
    :param post: slug - post
    :return:
    """
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
