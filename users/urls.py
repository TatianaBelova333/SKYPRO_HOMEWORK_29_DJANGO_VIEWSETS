from django.urls import path

from users.views import user as user_view


urlpatterns = [
    path('', user_view.UserListView.as_view()),
    path('<int:pk>/', user_view.UserDetailView.as_view()),
    path('create/', user_view.UserCreateView.as_view()),
    path('<int:pk>/update/', user_view.UserUpdateView.as_view()),
    path('<int:pk>/delete/', user_view.UserDeleteView.as_view()),
]