from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.sign_up, name="signup"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('tag/<str:tag_name>/', views.tag, name="tag"),
    path('settings/', views.settings, name="settings"),
    path('admin/', admin.site.urls),
    path('question/like', views.react_question, name='question-like'),
    path('answer/like', views.react_answer, name='asnwer-like')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
