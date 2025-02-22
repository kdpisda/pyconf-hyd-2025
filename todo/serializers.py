from rest_framework import serializers

from todo.models import Item
from todo.models import List


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "due_date",
            "completed",
            "priority",
            "todo_list",
        ]
        read_only_fields = ["created_at"]


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = List
        fields = ["id", "title", "description", "created_at", "owner", "items"]
        read_only_fields = ["created_at"]
