from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from .models import *
from login.models import Team
from .forms import *
from django.db.models import Q


def polls(request):
    if request.user.is_authenticated:
        user_polls = Poll.objects.filter(Q(team=request.user.profile.team) | Q(team=None)).exclude(user=request.user)
        return render(request, 'polls/polls.html', locals())
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def poll(request, poll_id):
    if request.user.is_authenticated:
        poll = Poll.objects.get(id=poll_id)
        poll_form = PollForm(poll, request.POST or None)
        if request.POST and poll_form.is_valid() and len(poll_form.cleaned_data) != 0:
            if poll.user != request.user:
                poll_result_object = PollResult.objects.create(user=poll.user)
                for question in poll_form.cleaned_data:
                    answer = poll_form.cleaned_data[question]
                    question_object = Question.objects.get(question=question, poll=poll)
                    try:
                        answer_object = PossibleAnswer.objects.get(answer=answer, question=question_object)
                    except PossibleAnswer.DoesNotExist:
                        answer_object = PossibleAnswer.objects.create(question=question_object, answer=answer, answered=True)
                    qap_object = QuestionAnswerPair.objects.create(poll_result=poll_result_object, question=question_object, answer=answer_object)
                return HttpResponseRedirect(reverse_lazy('polls'))
            return render(request, 'polls/cheat.html', locals())
        return render(request, 'polls/poll.html', locals())
    else:
        return HttpResponseRedirect(reverse_lazy('login'))
    
def new_poll(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return render(request, 'polls/staff_only.html', locals())
        form = NewPollForm(request.POST or None)
        if request.POST:
            if int(form.data['team']) != -1:
                team = Team.objects.get(id=int(form.data['team']))
                n_poll = Poll.objects.create(user=User.objects.get(username=form.data['user']), name=form.data['pollName'], team=team)
            else:
                n_poll = Poll.objects.create(user=User.objects.get(username=form.data['user']), name=form.data['pollName'])
            question_index = 1
            answer_index = 1
            q = 'question'+str(question_index)
            while q in form.data:
                question = form.data[q]
                question_type = form.data[q+'_type']
                q_object = Question.objects.create(question=question, question_type=question_type, poll=n_poll)
                answer_index = 1
                answer = 'answer'+str(question_index)+'_'+str(answer_index)
                while answer in form.data:
                    a_object = PossibleAnswer.objects.create(question=q_object, answer=form.data[answer])
                    answer_index += 1
                    answer = 'answer'+str(question_index)+'_'+str(answer_index)
                question_index += 1
                q = 'question'+str(question_index)
            return HttpResponseRedirect(reverse('polls'))
        return render(request, 'polls/new_poll.html', locals())
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def delete_poll(request, poll_id):
    if request.user.is_authenticated and request.user.is_staff:
        poll = Poll.objects.get(id=poll_id)
        poll.delete()
        return HttpResponseRedirect(reverse_lazy('polls'))
    return render(request, 'polls/staff_only.html', locals())