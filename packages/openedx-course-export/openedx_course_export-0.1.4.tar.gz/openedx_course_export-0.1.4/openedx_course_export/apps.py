"""
Course Export Application Configuration
"""

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    PluginSettings, PluginURLs, ProjectType, SettingsType
)

class CourseExportConfig(AppConfig):
    """
    Configuration class for course export app
    """
    name = "openedx_course_export"
    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: "",
                PluginURLs.REGEX: "^api/courses/v0/export/",
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.CMS: {
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: "settings.production"
                },
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            }
        },
    }
