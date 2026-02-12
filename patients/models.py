from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientRecord(models.Model):
    """
    Stores sanitized patient data extracted from FHIR payload.
    Sensitive fields are stored encrypted.
    """

    # FHIR resource id
    fhir_id = models.CharField(max_length=255, unique=True, db_index=True)

    # Basic patient info
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Encrypted sensitive fields (PHI)
    encrypted_ssn = models.TextField(null=True, blank=True)
    encrypted_passport = models.TextField(null=True, blank=True)

    # Full original FHIR payload (for audit purposes)
    raw_payload = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fhir_id} - {self.first_name} {self.last_name}"


class AccessLog(models.Model):
    """
    Logs every access to patient retrieval endpoint.
    Required for audit compliance.
    """

    patient = models.ForeignKey(
        PatientRecord,
        on_delete=models.CASCADE,
        related_name="access_logs"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField()
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Accessed {self.patient.fhir_id} at {self.accessed_at}"
