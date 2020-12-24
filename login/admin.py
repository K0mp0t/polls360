from django.contrib import admin
from .models import *

class TeamMembersInline(admin.StackedInline):
    model = Profile
    extra = 0
    readonly_fields = ['user', 'position']

    def has_add_permission(self, request, obj=None):
        return False

class ProfileAdmin(admin.ModelAdmin):
    #
    readonly_fields = ['user',]
    fields = ['user', 'profile_image', 'team', 'position']
    list_display = ['user', 'team_name', 'position']

    def team_name(self, obj):
        if obj.team is not None:
            return obj.team.name
        return '-'

    def has_add_permission(self, request, obj=None):
        return False


class TeamAdmin(admin.ModelAdmin):
    fields = ['name',]
    list_display = ['name', 'teammates_number', 'teammates']
    inlines = [
        TeamMembersInline
    ]
    
    def teammates_number(self, obj):
        return len(Profile.objects.filter(team=obj))
    
    def teammates(self, obj):
        return list(Profile.objects.filter(team=obj))

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)