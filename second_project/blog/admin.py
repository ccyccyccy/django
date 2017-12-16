from django.contrib import admin
from blog import models

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'author', 'category',)
    search_fields = ['title', 'content']
    ordering = ['-published_date']
    list_filter = ['published_date']
    date_hierarchy = 'published_date'
    #filter_horizontal = ('tags',)
    fields = ('title', 'slug', 'content', 'author', 'category', 'tags',)
    raw_id_fields = ('tags',)
    #prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ('slug', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)   


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date',)
    search_fields = ('name', 'subject',)
    date_hierarchy = 'date'

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)