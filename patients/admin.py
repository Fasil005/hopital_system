from django.contrib import admin

from patients.models import PatientRecord, AccessLog

admin.site.register(PatientRecord)
admin.site.register(AccessLog)