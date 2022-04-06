from django.template.defaultfilters import slugify
import itertools


def slugger(instance):
    """
        Object must have slug and id fields in the model.
    """
    if not instance.id: # if created
        Klass = instance.__class__
        instance.slug = slugify(instance.title)

        for x in itertools.count(1):
            if not Klass.objects.filter(slug = instance.slug).exists(): # TODO: Faster ORM
                break
            instance.slug  = '%s-%d' % (instance.slug , x)

