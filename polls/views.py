from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice


def get_set(Klass, order_param, **filter_data):
    return Klass.objects.order_by(order_param).\
        filter(**filter_data)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return get_set(Question, '-pub_date', pub_date__lte=timezone.now())[:10]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_queryset(self):
        return get_set(Question, '-pub_date', pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

    except (KeyError, Choice.DoesNotExist):
        return render(request,
                      'polls/detail.html',
                      {'question': question, 'error_message': 'You didn\'t select a choice'})

