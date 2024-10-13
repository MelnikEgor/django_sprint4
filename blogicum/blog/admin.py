from django.contrib import admin

from .models import Category, Location, Post


admin.site.empty_value_display = 'Не задано'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'is_published',
    )
    list_display_links = (
        'title',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'pub_date',
        'author',
        'location',
        'is_published',
        'category'
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'category',
        'pub_date',
        'location',
    )
    list_display_links = (
        'title',
    )
