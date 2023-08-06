from django.db.models import (
    CharField,
    Model as DjangoModel
)


class Model(DjangoModel):

    def from_jsonapi_data(self, data):
        for field in self._meta.fields:
            if isinstance(field, CharField):
                if field.name in data['attributes']:
                    setattr(self, field.name, data['attributes'][field.name])

    def to_jsonapi_data(self):
        data = {
            'id': self.id,
            'type': self.__class__.__name__,
            'attributes': {},
            'relationships': {}
        }
        for field in self._meta.fields:
            if isinstance(field, CharField):
                data['attributes'][field.name] = getattr(self, field.name)
        if len(data['attributes'].keys()) == 0:
            del data['attributes']
        if len(data['relationships'].keys()) == 0:
            del data['relationships']
        return data

    class Meta:
        abstract = True
