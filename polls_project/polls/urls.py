from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    #THESE URLS ARE FOR CLASS BASED (GENERIC VIEWS)
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/create/choices', views.create_poll_view, name='choices'),
    path('create/', views.CreateQuestionView.as_view(), name='create'),
    path('<int:pk>/delete/', views.DeleteQuestionView.as_view(), name='delete'),
]
