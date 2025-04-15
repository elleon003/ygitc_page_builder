from rest_framework import serializers
from .models import Page, Asset, Template


class PageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Page model
    """
    created_by_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'content', 'html', 'css',
            'is_published', 'created_by', 'created_by_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_by_email', 'created_at', 'updated_at']
    
    def get_created_by_email(self, obj):
        return obj.created_by.email
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class AssetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Asset model
    """
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = ['id', 'name', 'file', 'file_url', 'file_type', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at', 'file_url']
    
    def get_file_url(self, obj):
        return obj.file.url
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Template model
    """
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'content', 'thumbnail', 'thumbnail_url',
            'is_public', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'thumbnail_url']
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
