from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^streaks/categories/$', views.CategoriesViewSet.as_view(), name='categories-list'),
    url(r'^streaks/$', views.UserStreaksView.as_view(), name='streak-list'),
]