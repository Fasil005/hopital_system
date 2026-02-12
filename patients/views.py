from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from patients.models import PatientRecord, AccessLog
from patients.serializers import (FHIRPatientIntakeSerializer,
                                 PatientRetrieveSerializer)
from services.common import get_client_ip
from patients.tasks import send_welcome_email


class PatientIntakeView(APIView):

    def post(self, request):
        serializer = FHIRPatientIntakeSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        # Send welcome email asynchronously if email is provided
        if patient.email:
            send_welcome_email.delay(patient.fhir_id, patient.email)

        return Response(
            {"message": "Patient successfully ingested."},
            status=status.HTTP_201_CREATED
        )


class PatientRetrieveView(APIView):

    def get(self, request, fhir_id):
        patient = get_object_or_404(PatientRecord, fhir_id=fhir_id)

        # Log access
        AccessLog.objects.create(
            patient=patient,
            user=request.user,
            ip_address=get_client_ip(request),
        )

        serializer = PatientRetrieveSerializer(patient)
        return Response(serializer.data)