from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import generic
from polls.models import Poll, PollResult
from .models import Team
from .forms import *
from django.core.files.storage import default_storage

from django.contrib.auth.models import User

# 
# def handler404(request, exception):
#     context = {}
#     response = render(request, "404.html", context=context)
#     response.status_code = 404
#     return response


class SingUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'login/sign_up.html'


class LoginView(generic.CreateView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'login/login.html'


def profile(request):
    user = request.user
    if user.is_authenticated:
        completed_polls_num = PollResult.objects.filter(user=user)
        user_polls_num = Poll.objects.filter(user=user)
        return render(request, 'login/profile.html', locals())
    return reverse_lazy('login')

def edit_profile(request):
    user = request.user
    if user.is_authenticated:
        form_initial = {'username': user.username,
                         'email': user.email,
                         'reg_date': user.date_joined,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'team': user.profile.team.name if user.profile.team is not None else 'Нет команды',
                         'position': user.profile.position}
        form = ProfileEditForm(request.POST or None, request.FILES or None, initial=form_initial)
        if form.is_valid():
            if request.POST:
                for e in form.changed_data:
                    if e != 'position' and e != 'profile_image':
                        setattr(user, e, form.cleaned_data[e])
                    else:
                        if e == 'profile_image':
                            default_storage.delete(user.profile.profile_image.path)
                        setattr(user.profile, e, form.cleaned_data[e])
            user.save()
            user.profile.save()
            return HttpResponseRedirect(reverse('profile'))
        return render(request, 'login/edit_profile.html', locals())
    return reverse_lazy('login')

def teams(request):
    if request.user.is_authenticated:
        if request.user.profile.team:
            return team_info(request, request.user.profile.team.id)
        available_teams = Team.objects.all()
        return render(request, 'login/teams.html', locals())
    return reverse_lazy('login')
    

def team_info(request, team_id):
    user = request.user
    if user.is_authenticated:
        team = Team.objects.get(id=team_id)
        teammates = Profile.objects.filter(team=team)
        teammates_count = len(teammates)
        if user.profile.team:  
            available_teams = Team.objects.all().exclude(id=team_id)
        else:
            available_teams = Team.objects.all().exclude(id=team_id)
        return render(request, 'login/team_info.html', locals())
    return reverse_lazy('login')

def leave_team(request):
    user = request.user
    user.profile.team = None
    user.profile.save()
    return HttpResponseRedirect(reverse('teams'))

def join_team(request, team_id):
    user = request.user
    if user.is_authenticated:
        user.profile.team = Team.objects.get(id=team_id)
        user.save()
        return HttpResponseRedirect(reverse('teams'))
    return reverse_lazy('login')

def create_team(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            if user.profile.team is None:
                form = TeamCreationForm(request.POST or None)
                if request.POST and form.is_valid():
                    team = Team.objects.create(name=form.cleaned_data['name'])
                    user.profile.team = team
                    user.profile.position = 'Team Leader'
                    user.profile.save()
                    user.save()
                    return HttpResponseRedirect(reverse('teams'))
                return render(request, 'login/create_team.html', locals())
            return render(request, 'login/already_have_team.html', locals())
        return render(request, 'polls/staff_only.html', locals())
    return reverse_lazy('login')

def delete_team(request, team_id):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            if team_id == user.profile.team.id and user.profile.team.get_team_members_count() == 1:
                user.profile.team = None
                user.profile.position = ''
                user.profile.save()
                user.save()
                Team.objects.get(id=team_id).delete()
                return HttpResponseRedirect(reverse('teams'))
            return render(request, 'login/already_have_team.html', locals())
        return render(request, 'polls/staff_only.html', locals())
    return reverse_lazy('login')

def edit_team(request, team_id):
    user = request.user
    team = Team.objects.get(id=team_id)
    if user.is_authenticated:
        if user.is_staff:
            if team_id==user.profile.team.id:
                form = EditTeamForm(user.profile.team, request.POST or None)
                if request.POST and form.is_valid():
                    if form.cleaned_data['name'] != team.name:
                        team.name = form.cleaned_data['name']
                        team.save()
                    del form.cleaned_data['name']
                    for field in form.changed_data:
                        if field == 'name': continue
                        profile = Profile.objects.get(id=field.split('_')[0])
                        profile.position = form.cleaned_data[field]
                        profile.save()
                    return HttpResponseRedirect(reverse('teams'))
                return render(request, 'login/edit_team.html', locals())
            return render(request, 'login/already_have_team.html', locals())
        return render(request, 'polls/staff_only.html', locals())
    return reverse_lazy('login')