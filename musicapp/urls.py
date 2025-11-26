from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreateMusicView.as_view(), name='post'),
    path('post_done/', views.MusicSuccessView.as_view(), name='post_done'),
    path('musics/<int:category>/', views.CategoryView.as_view(), name='musics_cat'),
    path('user-list/<int:user>/', views.UserView.as_view(), name='user_list'),
    path('music-detail/<int:pk>/', views.MusicDetailView.as_view(), name='music_detail'), 
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('music/<int:pk>/delete/', views.MusicDeleteView.as_view(), name='music_delete'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/done/', views.ContactDoneView.as_view(), name='contact_done'),
]
