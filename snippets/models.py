from django.conf import settings
from django.db import models
from django.utils import timezone

SHORT_DESCRIPTION_LEN = 10


class PublicSnippetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_draft=False)


class Snippet(models.Model):
    title = models.CharField('Título', max_length=128)
    code = models.TextField('Código', blank=True)
    description = models.TextField('Descripción', blank=True)
    is_draft = models.BooleanField('Borrador', default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="Colaborador",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField("Fecha de publicación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    objects = models.Manager()
    public_objects = PublicSnippetManager()

    class Meta:
        db_table = 'snippets'

    def __repr__(self):
        return f"{self.pk} by {self.title}"

    @property
    def short_description(self):
        if len(self.description) <= SHORT_DESCRIPTION_LEN:
            return self.description
        return self.description[:SHORT_DESCRIPTION_LEN]


class Comment(models.Model):
    text = models.TextField("Texto", blank=False)
    commented_at = models.DateTimeField("Fecha de publicación", default=timezone.now)
    commented_to = models.ForeignKey(Snippet, verbose_name="Fragmentos",
                                     on_delete=models.CASCADE)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     verbose_name="Colaborador",
                                     on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

    def __repr__(self):
        return f"{self.pk} by {self.commented_by}"
