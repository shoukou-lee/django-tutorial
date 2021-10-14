from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# 코드를 더 깔끔하게 관리할 수 있도록, 함수를 제거하고 클래스 추가 (Generic view 사용)
# 클래스 기반 view보다는 함수 기반 view가 web을 이해하는데 더 좋을수도..
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions.
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


'''
# Create your views here.
# 클라이언트로부터 request를 받게 되면 여러가지 정보가 담겨 있을 것이다. 이를 다시 저장/추출/다운로드 등의 response를 해주는 것.
def index(request):
    # return HttpResponse("웹 걸음마중...")

    # Question 데이터를 pub_date 순으로 정렬해 5개까지만 데이터를 가지고 올 것이며, 이 데이터들을 ','로 연결하고 이를 response 한다.
    # 하지만, 아래 코드에는 페이지 디자인이 하드코딩되었다는 문제가 있다. 
    
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html') # 템플릿을 로드해서 리스폰스한다.
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
   #return HttpResponse(template.render(context, request))

    

def detail(request, question_id):
    #return HttpResponse("You're looking at question %s.", question_id)
    # response or 404를 주기 위해 try/except를 사용했다.
    # 하지만 Django에서는 더 쉬운 방법인 get_object_or_404()를 제공한다.
    
    #try:
    #   question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(requests, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Question을 조회한 후, results 템플릿이 결과 페이지에 보여지게 된다.
    return render(requests, 'polls/results.html', {'question': question})
'''

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try: 
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question, 
            'error_message': "You didn't select a choice.", 
        })
    else: # 데이터가 있는 경우
        selected_choice.votes += 1
        selected_choice.save()
        
        # url을 하드코딩하지 않기 위한 reverse, vote를 한 후에는 results를 보여준다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
