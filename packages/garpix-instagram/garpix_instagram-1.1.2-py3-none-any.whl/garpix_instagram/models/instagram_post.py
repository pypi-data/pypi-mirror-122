from django.db import models
from django.conf import settings
from django.utils.module_loading import import_string
from garpix_utils.file import get_file_path

InstagramPostMixin = import_string(settings.GARPIX_INSTAGRAM_POST_MIXIN)


class InstagramPost(InstagramPostMixin, models.Model):
    user_name = models.CharField(max_length=250, verbose_name='Ник пользователя', null=True)
    user_image = models.ImageField(verbose_name="Изображение пользователя", null=True,
                                   upload_to=get_file_path)
    post_link = models.CharField(max_length=1000, verbose_name='Ссылка на пост', null=True)
    post_image = models.ImageField(verbose_name="Изображение поста", null=True, upload_to=get_file_path)
    like_count = models.PositiveIntegerField(verbose_name='Количество лайков', default=0)
    active = models.BooleanField(default=False, verbose_name='Отображать пост?')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Пост Instagram"
        verbose_name_plural = "Посты Instagram"
        ordering = ('-like_count',)
