#1: from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect, Http404, HttpResponse
# from django.core.urlresolvers import reverse
# from django.views import generic

# from polls.models import Poll, Choice


# def index(request):
#   #1: return HttpResponse("Hello, world. You're at the poll index.")
#   #
#   #2: latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#   #   output = ', '.join([p.question for p in latest_poll_list])
#   #   return HttpResponse(output)
#   #
#   #3: latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#   #   template = loader.get_template('polls/index.html')
#   #   context = RequestContext(request, {
#   #     'latest_poll_list': latest_poll_list,
#   #   })
#   #   return HttpResponse(template.render(context))
#   latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#   context = {'latest_poll_list': latest_poll_list}
#   return render(request, 'polls/index.html', context)

# def detail(request, poll_id):
#   #1:   return HttpResponse("You're looking at poll %s." % poll_id)
#   #2:   try:
#   #       poll = Poll.objects.get(pk=poll_id)
#   #     except Poll.DoesNotExist:
#   #       raise Http404
#   #     return render(request, 'polls/detail.html', {'poll': poll})
#   poll = get_object_or_404(Poll, pk=poll_id)
#   return render(request, 'polls/detail.html', {'poll': poll})

# def results(request, poll_id):
#   #1:   return HttpResponse("You're looking at the results of poll %s." % poll_id)
#   #
#   poll = get_object_or_404(Poll, pk=poll_id)
#   return render(request, 'polls/results.html', {'poll': poll})


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Poll

class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_poll_list'

  def get_queryset(self):
    """Return the last five published polls."""
    #1: return Poll.objects.order_by('-pub_date')[:5]
    return Poll.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
  model = Poll
  template_name = 'polls/detail.html'

  def get_queryset(self):
    """
    Excludes any polls that aren't published yet.
    """
    return Poll.objects.filter(pub_date__lte=timezone.now())
    


class ResultsView(generic.DetailView):
  model = Poll
  template_name = 'polls/results.html'


def vote(request, poll_id):
  #1:   return HttpResponse("You're voting on poll %s." % poll_id)
  #
  p = get_object_or_404(Poll, pk=poll_id)
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    #redisplay the poll voting form
    return render(request, 'polls/detail.html', {
      'poll': p,
      'error_message': "You didn't select a choice! ",
      })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    #Always return an HttpResponseRedirect after successfully dealing
    #with POST data. This prevents data from being posted twice if a
    #user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


