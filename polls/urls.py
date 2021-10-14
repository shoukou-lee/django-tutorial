from django.urls import path
from . import views

''' 
app_name = 'polls'
urlpatterns = [
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # Django에서 지원하는 url 패턴임. 예를 들면, /polls/5/vote
    # 이 패턴이 검출되면 동작함
]
'''

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # pk : 중복되지 않는 데이터를 구분할 수 있는 값 (예를 들면 DB 내의 하나의 열)
]