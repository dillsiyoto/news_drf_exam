from django.db import models


class Article(models.Model):
    source_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="id источника"
    )
    source_name = models.CharField(
        max_length=70,
        verbose_name="название источника"
    )
    author = models.CharField(
        max_length=70,
        null=True,
        blank=True,
        verbose_name="автор"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="заголовок"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="описание"
    )
    url = models.URLField(
        unique=True,
        verbose_name="ссылка"
    )
    url_to_image = models.URLField(
        null=True,
        blank=True,
        verbose_name="ссылка на картинку"
    )
    published_at = models.DateTimeField(
        verbose_name="дата публикации"
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="контент",
    )

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} ({self.source_name})"