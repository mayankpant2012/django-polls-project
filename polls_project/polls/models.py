from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date Published',default=timezone.now)
    no_of_choices = models.IntegerField('Number of Choices', default=0)
    voted_by = models.ManyToManyField(User, blank=True, related_name='questions_voted')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_total_votes(self):
        total_votes = 0
        for choice in self.choice_set.all():
            total_votes+=choice.votes
        return total_votes
#define a get leader instead
    def get_leader(self):
        total_votes = self.get_total_votes()
        if total_votes == 0:
            total_votes = 1
        leader = []
        choice = self.choice_set.all()[0]
        leader.append(choice.choice_text)
        leader.append(int((choice.votes/total_votes)*100))
        return leader

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-votes']

    def __str__(self):
        return self.choice_text
