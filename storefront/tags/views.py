from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem

def generic_relationships_demo(request):
    # Method 1: Direct querying
    content_type = ContentType.objects.get_for_model(Product)
    tags_for_product1 = TaggedItem.objects\
        .select_related('tag')\
        .filter(
            content_type=content_type,
            object_id=1
        )

    # Method 2: Using custom manager
    tags_for_product2 = TaggedItem.objects.get_tags_for(Product, 2)

    return render(request, 'generic_relationships.html', {
        'tags_product1': tags_for_product1,
        'tags_product2': tags_for_product2
    })