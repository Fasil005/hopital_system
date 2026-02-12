from django.urls import path
from patients.views import PatientIntakeView, PatientRetrieveView

urlpatterns = [
    path("v1/patient-intake/", PatientIntakeView.as_view()),
    path("v1/patients/<str:fhir_id>/", PatientRetrieveView.as_view()),
]