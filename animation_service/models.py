from django.db import models
import uuid

class Animation(models.Model):
    animation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    duration = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    animation_path = models.FileField(upload_to='animations/')

    class Meta:
        app_label = 'animation_service'

    def __str__(self):
        return str(self.animation_id)
