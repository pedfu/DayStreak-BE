from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^streaks/categories/$', views.CategoriesViewSet.as_view(), name='categories-list'),
    url(r'^streaks/$', views.UserStreaksView.as_view(), name='streak-list'),
    url(r'^streaks/track/$', views.StreakTrackView.as_view(), name='streak-track'),
    path('category/<int:id>/delete/', views.CategoryDeleteViewSet.as_view(), name='category-delete'),
    path('streaks/<int:id>/delete/', views.StreakDeleteViewSet.as_view(), name='streak-delete'),
    path('streaks/<int:id>/', views.UserStreaksView.as_view(), name='streak-edit'),
    path('category/', views.CategoryViewSet.as_view(), name='category'),
    path('streaks/<int:id>/track/', views.StreakTrackDetailsView.as_view(), name='streak-track-details'),
    path('streaks/<int:id>/complete-day/', views.StreakTrackView.as_view(), name='streak-track-complete-days'),
]