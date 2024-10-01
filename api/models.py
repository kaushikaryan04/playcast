from cloudinary import CloudinaryImage
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from .cloudinary import GetUrlOnSave





class Video(models.Model) :
    title = models.CharField(max_length = 100 )
    thumbnail = CloudinaryField('image',blank = True )
    category = models.CharField(max_length = 100) # ToDo -> Change to choice field
    video_url = models.URLField(blank = True)
    uploaded_by = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True )

    def setUrl(self , video_file) :
        url = GetUrlOnSave(video_file)
        self.video_url = url
        self.setThumbnail(url)


    def setThumbnail(self , url) :
        # change video url extension to jpg3
        url = url.replace(".mp4",".jpg")
        self.thumbnail = url







class Comments(models.Model):
    user = models.ForeignKey(User , on_delete= models.CASCADE)
    video = models.ForeignKey(Video , on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class Like(models.Model) :
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True )

    class Meta :
        unique_together = ('video','user')
    def __str__(self) :
         return f'{self.user.username} liked this video {self.video.title}'
