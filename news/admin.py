from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'date', 'short_body')
    list_filter = ('date',)
    search_fields = ('headline', 'body')
    ordering = ('-date',)
    
    def short_body(self, obj):
        return obj.body[:100] + '...' if len(obj.body) > 100 else obj.body
    short_body.short_description = 'Cuerpo de la noticia'
