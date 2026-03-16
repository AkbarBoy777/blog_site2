from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.PostListView.as_view(paginate_by=3), name='list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/', views.post_detail , name="post_detail"),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]