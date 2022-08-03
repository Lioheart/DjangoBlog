from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    """
    Klasa Post

    title = odpowiada polu VARCHAR w bazie danych,
    slug = pole przeznaczone do użycia w adresach URL. Za pomocą unique_for_date Django nie dopuści, aby więcej niż jeden post miał taką samą wartość pola slug dla danej daty,
    author = klucz obcy w relacji wiele do jednego (użytkownik może napisać wiele postów). Parametr on_delete ustawiony na CASCADE oznacza, że po usunięciu użytkownika z bazy usuniemy także jego posty,
    body = odpowiada polu TEXT w bazie danych,
    publish = data i godzina opublikowania postu. Metoda wartości domyślnej zwraca bieżącą datę i godzinę strefy czasowej.
    created = używając opcji auto_now_add, data zostanie zapisana podczas tworzenia obiektu,
    updated = używając opcji auto_now data zostanie zaktualizowana podczas zapisywania obiektu,
    status = używając parametru choices określamy, że wartość tego pola może być wyłącznie jedną z podanych wartości.

    verbose_name odpowiada za wyświetlanie na stronie administracyjnej, verbose_name_plural za liczbę mnogą.

    W klasie Meta określamy, że wyniki zwracane z bazy mają być domyślnie sortowane według publish w porządku malejącym.
    """
    STATUS_CHOICES = (
        ('draft', 'Szkic'),
        ('published', 'Opublikowany'),
    )
    title = models.CharField(max_length=250, verbose_name='Tytuł')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Autor')
    body = models.TextField(verbose_name='Tekst')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Opublikowane')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    # Menedżer wyszukiwania po ORM
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        """
        Metoda tworząca URL absolutny według schematu rok/miesiąc/dzień/slug dla szczegółów posta.
        :return:
        """
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posty'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Commentjest modelem do przechowywania komentarzy.

    Zawarty jest tu klucz obcy dla konkretnego posta. Każdy komentarz przeznaczony jest dla konkretnego posta,
    a sam post może mieć wiele komentarzy. Atrybut related_name umożliwia nadanie nazwy atrybutowi, dzięki czemu
    możemy uzyć comment.post() do pobrania konkretnego posta, lub post.comments.all() do pobrania wszystkich
    komentarzy.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, verbose_name='Imię')
    email = models.EmailField(verbose_name='Email')
    body = models.TextField(verbose_name='Komentarz')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    updated = models.DateTimeField(auto_now=True, verbose_name='Zmodyfikowano')
    active = models.BooleanField(default=True, verbose_name='Aktywny')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'

    def __str__(self):
        return f'Komentarz dodany przez {self.name} dla posta {self.post}'
