from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return self\
            .select_related('tag')\
            .filter(
                content_type=content_type,
                object_id=obj_id
            )

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # What tag is applied
    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE
    )

    # Three parts needed for generic relationship:
    # 1. Type of model being tagged
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2. ID of the specific object being tagged
    object_id = models.PositiveIntegerField()
    # 3. Combines the above two to get actual object
    content_object = GenericForeignKey()

class Tag(models.Model):
    label = models.CharField(max_length=255)