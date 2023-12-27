from django.contrib import admin
from .models import Applications,Interests,Match

class ApplicationsAdmin(admin.ModelAdmin):
    search_fields = ['user__username']  # Add other fields if needed


class MatchAdmin(admin.ModelAdmin):
    search_fields = ['male_application__user__username','female_application__user__username']
admin.site.register(Applications, ApplicationsAdmin)
admin.site.register(Interests)
admin.site.register(Match,MatchAdmin)
