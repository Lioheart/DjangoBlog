from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.forms import EmailPostForm
from blog.models import Post


class PostListView(ListView):
    """
    PostListView

    Używamy konkretnej kolekcji QuerySet, zamiast domyślnej (model = Post pobiera Post.objects.all()).
    Dla wyników zapytania używamy zmiennej kontekstu post. Wartością domyślną jest object_list.
    Stronicowanie powoduje wyświetlanie po 3 obiekty na stronie.
    Używamy własnego szablonu do wygenerowania strony.
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    """
    Pobranie posta na podstawie jego identyfikatora.

    :param request:
    :param post_id: int
    :return: witryna http wyświetlająca formularz.
    """
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Weryfikacja pól formularza zakończona powodzeniem.
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title,
                                                                                                    post_url,
                                                                                                    cd['name'],
                                                                                                    cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            send = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'send': send,
    })


def post_list(request):
    """
    Widok wszystkich opublikowanych postów.

    :param request:
    :return: witryna http wyświetlająca posty.
    """
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {
        'page': page,
        'posts': posts,
    })


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
