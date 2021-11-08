from django.urls import path 

from . import views 

app_name="blog"
urlpatterns = [ 
    path("", views.HomeView.as_view(), name="home"),
    path("posts/search", views.PostSearchView.as_view(),name="post-search" ),
    path("posts/create", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<slug:slug>/update", views.PostUpdateView.as_view(), name="post-update" ),
    path("posts/<slug:slug>/delete", views.PostDeleteView.as_view(), name="post-delete" ),
    path("posts/<slug:slug>/comment", views.CommentHandleView.as_view(), name="comment"),
    path("posts/<slug:slug>/vote", views.VoteCountView.as_view(),name="vote-count" ),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail"),

]