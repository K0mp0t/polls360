from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileEditForm(forms.Form):
    username = forms.CharField(label='Логин', disabled=True, required=False)
    email = forms.EmailField(label='Email', required=False)
    reg_date = forms.DateField(label='Дата регистрации', disabled=True, required=False)
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    team = forms.CharField(label='Команда', disabled=True, required=False)
    position = forms.CharField(label='Роль в команде', required=False)
    profile_image = forms.ImageField(label='Фото', required=False)
    
class TeamCreationForm(forms.Form):
    name = forms.CharField(label='Название команды', required=True, help_text='Введите название', widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))
    
class EditTeamForm(forms.Form):
    def __init__(self, team=None, *args, **kwargs):
        super(EditTeamForm, self).__init__(*args, **kwargs)
        profiles = Profile.objects.filter(team=team)
        self.fields['name'] = forms.CharField(label='Название команды', required=False, initial=team.name)
        for profile in profiles:
            self.fields[str(profile.id)+'_position'] = forms.CharField(label='Роль '+profile.user.username,
                                                                             required=False, initial=profile.position)
    