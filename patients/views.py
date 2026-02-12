from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from patients.models import PatientRecord, AccessLog
from patients.serializers import (FHIRPatientIntakeSerializer,
                                 PatientRetrieveSerializer)
from services.common import get_client_ip


class PatientIntakeView(APIView):

    def post(self, request):
        serializer = FHIRPatientIntakeSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

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
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
        )

        serializer = PatientRetrieveSerializer(patient)
        return Response(serializer.data)