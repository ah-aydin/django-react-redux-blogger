from django.contrib import admin

from . import models

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ('title', 'author__username', 'author__email',)
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        ('Blog', {
            'fields': ('title', 'author', 'body'),
        }),
        ('Object information', {
            'fields': ('date_created', 'date_modified')
        }),
    )
    
    list_display = (
        'pk',
        'title',
        'author',
        'date_created',
    )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('author__username', 'blog__title',)
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        ('Comment', {
            'fields': ('author','blog', 'body')    
        }),
        ('Object information', {
            'fields': ('date_created', 'date_modified')
        }),
    )
    
    list_display = (
        'pk',
        'blog',
        'author',
        'date_created',
    )