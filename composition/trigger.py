from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import SimpleLazyObject
from django.utils.itercompat import is_iterable

class Trigger(object):
    def __init__(self, do, on, field_name, sender, sender_model, commit,\
                 field_holder_getter):
        self.freeze = False
        self.field_name = field_name
        self.commit = commit

        if sender_model and not sender:
            if isinstance(sender_model, basestring):
                sender_model = models.get_model(*sender_model.split(".", 1))

            self.sender = self.sender_model = sender_model
        else:
            self.sender = sender
            self.sender_model = sender_model

        if not do:
            raise ValueError("`do` action not defined for trigger")
        self.do = do

        if not is_iterable(on):
            on = [on]
        self.on = on

        self.field_holder_getter = field_holder_getter

    def connect(self):
        """
           Connects trigger's handler to all of its signals
        """
        for signal in self.on:
            signal.connect(self.handler, sender=self.sender)

    def handler(self, signal, instance=None, **kwargs):
        """
            Signal handler
        """
        if self.freeze:
            return

        try:
            objects = self.field_holder_getter(instance)
        except ObjectDoesNotExist:
            return

        if not objects:
            return

        if not is_iterable(objects) or isinstance(objects, SimpleLazyObject):
            objects = [objects]

        for obj in objects:
            setattr(obj, self.field_name, self.do(obj, instance, signal))

            if self.commit:
                obj.save()
