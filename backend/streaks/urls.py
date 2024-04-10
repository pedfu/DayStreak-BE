from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^streaks/categories/$', views.CategoriesViewSet.as_view(), name='categories-list'),
    url(r'^streaks/$', views.UserStreaksView.as_view(), name='streak-list'),
    url(r'^streaks/track/$', views.StreakTrackView.as_view(), name='streak-track'),
    path('category/', views.CategoryViewSet.as_view(), name='category'),
    path('streaks/<int:id>/track/', views.StreakTrackDetailsView.as_view(), name='streak-track-details')
]