from rest_framework import serializers

from myapp.models import Books

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Books
        fields="__all__"
        