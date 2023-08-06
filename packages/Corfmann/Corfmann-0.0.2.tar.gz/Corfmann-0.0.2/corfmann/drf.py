from rest_framework import viewsets, mixins

class GenericViewSet(viewsets.GenericViewSet):

    def get_serializer(self, *args, **kwargs):
        if hasattr(self, 'serializers'):
            return self.serializers.get(
                self.request.method.lower()
            )(*args, context={'request': self.request}, **kwargs)
        else:
            return super().get_serializer_class()