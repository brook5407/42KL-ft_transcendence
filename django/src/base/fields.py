import uuid
from django.db import models

class RandomStringIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64)
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            value = uuid.uuid4().hex
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)