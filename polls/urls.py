from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # Django에서 지원하는 url 패턴임. 예를 들면, /polls/5/vote
    # 이 패턴이 검출되면 동작함
]