from datetime import date

from rest_framework import serializers

from patients.models import PatientRecord
from services.encryption import EncryptionService
from services.common import mask

class FHIRPatientIntakeSerializer(serializers.Serializer):
    
    resourceType = serializers.CharField()
    id = serializers.CharField()
    birthDate = serializers.DateField()
    gender = serializers.CharField()
    name = serializers.ListField()
    identifier = serializers.ListField(required=False)

    def validate_birthDate(self, value):
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 18:
            raise serializers.ValidationError(
                "Patient must be 18 years or older."
            )

        return value

    def validate_resourceType(self, value):
        if value != "Patient":
            raise serializers.ValidationError(
                "This API is for patients."
            )
        return value

    def create(self, validated_data):
        encryption_service = EncryptionService()

        # Extract Name
        name_data = validated_data["name"][0]
        first_name = name_data.get("given", [""])[0]
        last_name = name_data.get("family", "")

        # Extract SSN
        ssn = None
        identifiers = validated_data.get("identifier", [])

        for identifier in identifiers:
            if identifier.get("system") == "http://hl7.org/fhir/sid/us-ssn":
                ssn = identifier.get("value")

        encrypted_ssn = (
            encryption_service.encrypt(ssn) if ssn else None
        )

        return PatientRecord.objects.create(
            fhir_id=validated_data["id"],
            first_name=first_name,
            last_name=last_name,
            gender=validated_data["gender"],
            birth_date=validated_data["birthDate"],
            encrypted_ssn=encrypted_ssn,
            raw_payload=self.context["request"].data,
        )


class PatientRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for returning sanitized patient data.
    Decrypts and masks sensitive fields before output.
    """

    ssn = serializers.SerializerMethodField()
    passport = serializers.SerializerMethodField()

    class Meta:
        model = PatientRecord
        fields = [
            "fhir_id",
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "ssn",
            "passport",
        ]

    def get_ssn(self, obj):
        encryption_service = EncryptionService()

        if not obj.encrypted_ssn:
            return None

        decrypted = encryption_service.decrypt(obj.encrypted_ssn)
        return mask(decrypted, prefix="***-**-")

    def get_passport(self, obj):
        encryption_service = EncryptionService()

        if not obj.encrypted_passport:
            return None

        decrypted = encryption_service.decrypt(obj.encrypted_passport)
        return mask(decrypted, prefix="****")