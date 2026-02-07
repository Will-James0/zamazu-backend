from django.urls import path, include
from apps.users.views import DashboardView, UserListView, UserCreateView, UserUpdateView, StatusToggleView, ProfileMixinView, UserDeleteView

urlpatterns = [
    path('list/', UserListView.as_view(), name='user-list'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('update/<uuid:code>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<uuid:code>/', UserDeleteView.as_view(), name='user-delete'),
    path('toggle-status/<uuid:code>/', StatusToggleView.as_view(), name='toggle-status'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    #profile
    path("profile/", include([
        path("<uuid:code>/", ProfileMixinView.as_view()),
        path("update/<uuid:code>/", ProfileMixinView.as_view())
    ])),
]