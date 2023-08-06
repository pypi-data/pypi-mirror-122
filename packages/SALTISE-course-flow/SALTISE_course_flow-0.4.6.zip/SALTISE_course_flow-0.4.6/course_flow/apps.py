from django.apps import AppConfig
from .checks import check_return_url
from django.core.checks import register

class CourseFlowConfig(AppConfig):
    name = "course_flow"
    verbose_name = "Course Flow"

    def ready(self):
        from django_lti_tool_provider.views import LTIView  # noqa
        from .lti import ApplicationHookManager  # noqa

        LTIView.register_authentication_manager(ApplicationHookManager())
        register(check_return_url)
