from django.urls import path
from .views import *


urlpatterns = [
    path("upload" , UploadVideo , name = "upload_video"),
    path("listvideos" , ListVideos , name = "list_videos"),
    path("addcomment" , AddComment , name = "add comment"),
    path("likevideo" , LikeVideo , name = "likevideo"),
    path("dislikevideo" , DislikeVideo , name = "dislike_video"),
    path("userinfo" , UserInfoView , name = "userinfo" ),
    path('listcomments' , ListComments , name = 'list_comments')
]
