from django.urls import path  , include  
from tickets import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('guests', views.GuestViewSet, basename='viewset')
router.register('movies', views.MovieViewSet, basename='viewset')
urlpatterns = [
  # 1 without Rest and without Model query
    path('no_rest_no_model_query/', views.no_rest_no_model_query),
    # 2 without Rest and with Model query
    path('no_rest_with_model_query/', views.no_rest_with_model_query),
    # 3 Function Based View 
    # 3.1 GET POST
    path('fbv/', views.FBV_List),
    # 3.2 GET PUT DELETE
    path('fbv/<int:pk>/', views.FBV_pk),
    # 4 Class Based View
    # 4.1 GET POST
    path('cbv/', views.CBV_List.as_view()),
    # 4.2 GET PUT DELETE
    path('cbv/<int:pk>/', views.CBV_pk.as_view()),
    # 5 mixin View
    # 5.1 GET POST
    path('mixin/', views.Mixins_List.as_view()),
    # 5.2 GET PUT DELETE
    path('mixin/<int:pk>/', views.Mixins_pk.as_view()),
    # 6 Generic View
    # 6.1 GET POST
    path('generic/', views.Generic_List.as_view()),
    # 6.2 GET PUT DELETE
    path('generic/<int:pk>/', views.Generic_pk.as_view()),
    # 7 ViewSet
    path('viewset/', include(router.urls)),
    path('find_movies/', views.find_movies, name='find_movie'),
    path('create_reservation/', views.create_reservation, name='crate_reservation'),
]