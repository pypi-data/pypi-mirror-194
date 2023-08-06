"""
Course export API endpoint urls.
"""

from django.conf import settings
from django.urls import re_path

from openedx_course_export.views import CourseExportView

urlpatterns = [
    re_path(
        r"^{}/$".format(settings.COURSE_ID_PATTERN),
        CourseExportView.as_view(),
        name="course_export_status",
    ),
    re_path(r"^", CourseExportView.as_view(), name="course_export"),
]
