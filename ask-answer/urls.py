from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('tag/<str:tag_name>/', views.tag, name="tag"),
    path('settings/', views.settings, name="settings"),
    path('admin/', admin.site.urls),
]
