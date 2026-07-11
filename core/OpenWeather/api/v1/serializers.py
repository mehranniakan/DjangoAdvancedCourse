from rest_framework import serializers


class OpenWeatherSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    def validate(self, attrs):
        lat = attrs.get('lat')
        lng = attrs.get('lng')

        if not -90 <= lat <= 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )

        if not -180 <= lng <= 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )
        return super().validate(attrs)
