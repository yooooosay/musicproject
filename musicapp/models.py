from django.db import models
from accounts.models import CustomUser
# Create your models here.
class PlayListName(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20)
    
    def __str__(self):
        return self.title
class MusicPost(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        PlayListName,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )

    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )

    comment = models.TextField(
        verbose_name='コメント'
    )

    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to= 'photos'
    )

    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    youtube_link = models.URLField(
        verbose_name='YouTubeリンク', 
        blank=True, null=True
    )

    def __str__(self):
        return self.title