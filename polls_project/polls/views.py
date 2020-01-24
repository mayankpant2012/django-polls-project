from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'


class AboutView(generic.TemplateView):
    template_name = 'about.html'


class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def create_poll_view(request, pk):
    q = get_object_or_404(Question, pk=pk)
    n = q.no_of_choices
    if request.method == 'POST':
        for i in range(1,q.no_of_choices+1):
            q.choice_set.create(choice_text=request.POST['choice'+str(i)], votes=0)
        q.save()
        return(redirect(reverse('polls:index')))
    else:
        return(render(request,'polls/create_poll.html',
                                context={'question':q,'n':range(n)}))


class CreateQuestionView(LoginRequiredMixin,generic.edit.CreateView):
    model = Question
    fields = ['question_text', 'no_of_choices']
    login_url = '/'

    def get_success_url(self):
        return reverse('polls:choices', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteQuestionView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Question
    success_url = reverse_lazy("polls:index")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #changed start
        voted_by_user = request.user
        if voted_by_user in question.voted_by.all():
           return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        question.voted_by.add(voted_by_user)
        question.save()
        #changed end
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
