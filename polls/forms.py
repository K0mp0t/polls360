from django import forms
from .models import *
from login.models import Team


class PollForm(forms.Form):
    def __init__(self, poll=None, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        for question in poll.questions():
            if question.question_type == 'st' or question.question_type == 'bt':
                self.fields[question.question] = forms.CharField(label=question.question, 
                                                                 widget=forms.TextInput(attrs={'placeholder': 'Введите ответ', 'class': 'text-field', 'autocomplete': 'off'}))
            elif question.question_type == 'r':
                choices = question.possible_answers()
                self.fields[question.question] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'custom-radio'}), choices=choices, label=question.question)
            elif question.question_type == 'c':
                choices = question.possible_answers()
                self.fields[question.question] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}), choices=choices, label=question.question)


class NewPollForm(forms.Form):
    user = forms.ChoiceField(label='Пользователь', widget=forms.Select(attrs={'class': 'std-select text-second-org'}), choices=[(user.username, user.username) for user in User.objects.all()])
    pollName = forms.CharField(label='Название опроса', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))
    team_choices = [(None, 'All teams')]+[(team.name, team.name) for team in Team.objects.all()]
    team = forms.ChoiceField(label='Команда', widget=forms.Select(attrs={'class': 'std-select text-second-org'}), choices=team_choices)