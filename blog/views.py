from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post


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
            subject = f'{cd["name"]} ({cd["email"]}) zachęca do przeczytania "{post.title}"'
            message = f'Przeczytaj post "{post.title}" na stronie {post_url}\n\n Komentarz dodany przez {cd["name"]}: {cd["comments"]}'
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            send = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'send': send,
    })


def post_list(request, tag_slug=None):
    """
    Widok wszystkich opublikowanych postów.

    W relacji tags występuje relacja wiele do wielu, dlatego filtrujemy po liście.
    Użyliśmy zapytania __in odpowiadającemu zapytaniu IN w SQL.

    :param request:
    :return: witryna http wyświetlająca posty.
    """
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
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
        'tag': tag,
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

    # Lista aktywnych komentarzy
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # Komentarz został opublikowany
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Utworzenie obiektu Comment; jeszcze jednak nie zapisujemy go w bazie
            new_comment = comment_form.save(commit=False)

            # Przypisanie komentarza do bieżącego posta.
            new_comment.post = post

            # Zapisanie komentarza w bazie
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Lista podobnych postów
    # flat = True zapewnia, że otrzymujemy listę [1, 2, ..] zamiast [(1,), (2,), ..]
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})
