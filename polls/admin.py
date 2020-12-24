from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import *


class PossibleAnswerInline(admin.TabularInline):
    model = PossibleAnswer
    extra = 0
    
    fields = ('answer', )

    def get_queryset(self, request):
        qs = super().get_queryset(request).exclude(answered=True)
        return qs

class QuestionAdmin(admin.ModelAdmin):
    fields = ('question', 'question_type')
    list_display = ('question', 'poll_name', 'question_type')
    inlines = [
        PossibleAnswerInline
    ]
    
    def poll_name(self, obj):
        return obj.poll.name


class QuestionInline(admin.StackedInline):
    model = Question
    show_change_link = True
    extra = 0


class QuestionAnswerPairInline(admin.TabularInline):
    model = QuestionAnswerPair
    extra = 0
    
    readonly_fields = ('question', 'answer')
    
    def has_add_permission(self, request, obj):
        return False


class PollAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'team')
    list_display = ('user', 'name', 'team', 'questions_number')

    inlines = [
        QuestionInline,
    ]

    def questions_number(self, obj):
        return len(Question.objects.filter(poll=obj))


class PollResultAdmin(admin.ModelAdmin):
    fields = ['user',]
    list_display = ['poll_name', 'username', 'team_name', 'created']
    search_fields = ['user__username',]

    inlines = [
        QuestionAnswerPairInline
    ]
    
    def poll_name(self, obj):
        return obj.get_poll_name()
    
    def team_name(self, obj):
        return obj.get_team_name()
    
    def username(self, obj):
        return obj.get_username()

    def has_add_permission(self, request):
        return False
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(PollResult, PollResultAdmin)
AdminSite.enable_nav_sidebar = False

"""
TODO:
1.
"""
 