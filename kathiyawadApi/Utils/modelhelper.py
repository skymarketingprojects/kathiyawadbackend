
from django.db import models
class Names:
    INDEX= "index"
def shiftUp(model_class: models.Model, start_index: int, page, exclude_pk=None):
    """
    Increments the index of all instances from `start_index` onward within the same page.
    """
    objects = model_class.objects.filter(index__gte=start_index, page=page)
    if exclude_pk:
        objects = objects.exclude(pk=exclude_pk)
    objects = list(objects.order_by(f"-{Names.INDEX}"))

    for obj in objects:
        obj.index += 1

    model_class.objects.bulk_update(objects, [Names.INDEX])


def shiftDown(model_class: models.Model, start_index: int, end_index: int, page, exclude_pk=None):
    """
    Decrements the index of all instances between start_index and end_index within the same page.
    """
    objects = model_class.objects.filter(index__gte=start_index, index__lt=end_index+1, page=page)
    if exclude_pk:
        objects = objects.exclude(pk=exclude_pk)
    objects = list(objects.order_by(Names.INDEX))

    for obj in objects:
        obj.index -= 1

    model_class.objects.bulk_update(objects, [Names.INDEX])


def shiftUpRange(model_class: models.Model, start_index: int, end_index: int, page, exclude_pk=None):
    """
    Increments the index of all instances between start_index and end_index within the same page.
    """
    objects = model_class.objects.filter(index__gt=start_index-1, index__lte=end_index, page=page)
    if exclude_pk:
        objects = objects.exclude(pk=exclude_pk)
    objects = list(objects.order_by(f"-{Names.INDEX}"))

    for obj in objects:
        obj.index += 1

    model_class.objects.bulk_update(objects, [Names.INDEX])


def indexShifting(instance: models.Model):
    model_class = instance.__class__
    page = instance.page  # Get the related page

    if instance.pk:
        old_index = model_class.objects.get(pk=instance.pk).index

        if old_index < instance.index:
            shiftDown(model_class, old_index, instance.index, page=page, exclude_pk=instance.pk)
        elif old_index > instance.index:
            shiftUpRange(model_class, instance.index, old_index, page=page, exclude_pk=instance.pk)

    else:
        if model_class.objects.filter(index=instance.index, page=page).exists():
            shiftUp(model_class, instance.index, page=page)
