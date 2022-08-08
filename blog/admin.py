from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Klasa PostAdmin

    Za pomocą atrybutu list_display można ustawić pola, które mają być wyświetlane na stronie listy obiektów administracyjnych,
    list_filter = służy do pokazania pola Filtruj, za pomocą jakich danych ma być filtrowanie,
    search_fields = pojawia się pasek wyszukiwania, za pomocą którego przeszukiwane są pola zawarte w tym atrybucie,
    prepopulated_fields = Django uzupełnia pole slug automatycznie za pomocą pola title,
    raw_id_fields = pokazuje pole wyszukiwania podczas dodawania nowych treści,
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
