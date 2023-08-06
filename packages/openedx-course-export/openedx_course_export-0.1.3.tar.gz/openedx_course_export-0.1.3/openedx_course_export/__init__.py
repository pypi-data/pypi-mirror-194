"""
A django app plugin to add a new API to Open edX to export courses to S3 buckets
"""

__version__ = '0.1.3'

default_app_config = 'openedx_course_export.apps:CourseExportConfig'  # pylint: disable=invalid-name
