from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from .views import MoviesView, CollectionView, CollectionEditView
from .views import RequestCountView, RequestCountResetView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('movies/', MoviesView.as_view()),
    path('collection/', CollectionView.as_view()),
    path('collection/<slug:collection_uuid>/', CollectionEditView.as_view()),
    path('request-count/', RequestCountView.as_view()),
    path('request-count/reset/', RequestCountResetView.as_view())
]
