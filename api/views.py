from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.views import Response
from .serializers import RegistrationSerializer, VideoSerializer , UserSerializer
from .models import Video , Comments , Like
from rest_framework.decorators import api_view, permission_classes


def get_authenticated_view(func) :
    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def wrapper(*args , **kwargs) :
        return func(*args , **kwargs)
    return wrapper


def post_authenticated_view(func) :
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def wrapper(*args , **kwargs) :
        return func(*args , **kwargs)
    return wrapper


class RegisterNewUser(generics.CreateAPIView) :
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self , request) :
        serializer = self.get_serializer(data = request.data )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"User Creation Successfull" : "User created"} , status = status.HTTP_201_CREATED)

@post_authenticated_view
def UploadVideo(request) :
    video = Video.objects.create(
        title = request.POST.get("title"),
        category = request.POST.get("category"),
        uploaded_by = request.user
    )
    video.setUrl(request.FILES.get("video_file"))
    video.save()
    return Response({
        "video_id" : video.id,
        "video_url" : video.video_url,
        "thumbnail" : video.thumbnail
    })

@post_authenticated_view
def AddComment(request) :
    # video = get_object_or_404(Video , pk = int(request.POST.get("video_id")))
    print(request.POST)
    video = Video.objects.get(pk = int(request.data.get("video_id")))
    user  = request.user

    c = Comments.objects.create(
        user = user ,
        video = video ,
        content = request.data.get("content")
    )
    c.save()
    return Response({
        "Comment added" : "comment added"
    })

@get_authenticated_view
def ListVideos(request) :
    videos = Video.objects.all()
    data = VideoSerializer(videos , many = True).data
    return Response(data)

@post_authenticated_view
def LikeVideo(request) :
    l = Like.objects.create(
        user = request.user ,
        video = Video.objects.get(pk = request.data.get("video_id")),
    )
    l.save()
    return Response({"success" : "video liked"})

@post_authenticated_view
def DislikeVideo(request) :
    Like.objects.get(video__pk = request.data.get("video_id")).delete()
    return Response({"success" : "video disliked"})

@get_authenticated_view
def UserInfoView(request) :
    user = request.user
    data = UserSerializer(user).data
    return Response(data)
