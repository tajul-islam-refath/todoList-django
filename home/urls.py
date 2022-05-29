from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-todo/', views.createTodo, name='create-todo'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('todo_update_is_done/<int:id>',
         views.updateTodoIsDone, name='todo_update_is_done'),
    path('todo_delete/<int:id>',
         views.todoDelete, name='todo_delete'),

]
