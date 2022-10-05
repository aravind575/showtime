from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from .views import MoviesView, CollectionView, CollectionEditView
from .views import RequestCountView, RequestCountResetView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('movies/', MoviesView.as_view(), name='movies'),
    path('collection/', CollectionView.as_view(), name='collection'),
    path('collection/<slug:collection_uuid>/', CollectionEditView.as_view(), name='collection_edit'),
    path('request-count/', RequestCountView.as_view(), name='request_count'),
    path('request-count/reset/', RequestCountResetView.as_view(), name='request_count_reset')
]
