from django.urls import path
from .views import *

app_name = 'blogapp'

urlpatterns = [
    path('', PostListView.as_view(paginate_by=1), name='list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/', post_detail , name="post_detail")
]