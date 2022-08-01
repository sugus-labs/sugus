from django.contrib import admin
from .models import Name

# admin.site.register(Name)

class NameAdmin(admin.ModelAdmin):
    fields = ['text', 'prob_f', 'prob_m', 
        'gender']
    list_display = ('text', 'prob_f', 
        'prob_m', 'gender', 'pub_date')

admin.site.register(Name, NameAdmin)
