from rest_framework import serializers
from .models import Review, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name","description"]


class ReviewSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Review
        fields = ["mark","comment","company"]