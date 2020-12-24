from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from login.models import Team

"""
PossibleAnswer M->O Question M->O Poll M->O User (completed by)
Question+PossibleAnswer O->O QuestionAnswerPair M->O PollResults M->O User (completed by)
"""


class Poll(models.Model):
    user = models.ForeignKey(User, related_name='Polls', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def questions(self):
        for question in Question.objects.filter(poll=self):
            yield question

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('st', 'smalltext'),
        ('bt', 'bigtext'),
        ('r', 'radio'),
        ('c', 'checkbox')
    ]

    question = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='smalltext')
    poll = models.ForeignKey(Poll, related_name='Questions', on_delete=models.CASCADE)

    def possible_answers(self):
        pa = PossibleAnswer.objects.filter(question=self, answered=False)
        for p in pa:
            yield p.answer, p.answer

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        
    def __str__(self):
        return self.question


class PollResult(models.Model):
    user = models.ForeignKey(User, related_name='PollsResults', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def get_poll_name(self):
        return QuestionAnswerPair.objects.filter(poll_result=self).first().question.poll.name
    
    def get_team_name(self):
        return QuestionAnswerPair.objects.filter(poll_result=self).first().question.poll.team.name
    
    def get_username(self):
        return self.user.username


class PossibleAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    answered = models.BooleanField(default=False) 
    
    def __str__(self):
        res = ''
        l = str(self.answer).replace('[', '').replace(']', '').split("',")
        for i in l:
            res+=i.replace("'", '')+','+'\n'
        return res[:-2]
    

class QuestionAnswerPair(models.Model):
    poll_result = models.ForeignKey(PollResult, related_name='QuestionAnswerPairs', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(PossibleAnswer, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Question Answer Pair'
