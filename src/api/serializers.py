from rest_framework import serializers

from .models import Equipment, Facility, FacilityType

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ('id', 'name', 'detail')
        read_only_fields = ('id',)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'quantity', 'facility')
        read_only_fields = ('id',)


class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityType
        fields = ('id', 'type', 'facility')
