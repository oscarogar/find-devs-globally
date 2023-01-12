from django.urls import path
from . import views

urlpatterns = [
    path('', views.project, name='project' ),
    path('project/<str:pk>/', views.projects, name='projects'),
    path('create-project/', views.createProject, name='create-project'),
    path('update-project/<str:id>', views.updateProject, name='update-project'),
    path('delete-project/<str:id>', views.deleteProject, name='delete-project'),
]