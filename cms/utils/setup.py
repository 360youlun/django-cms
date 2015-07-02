import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django import template

from cms.utils.compat.dj import is_installed as app_is_installed


def validate_dependencies():
    """
    Check for installed apps, their versions and configuration options
    """
    if not app_is_installed('mptt'):
        raise ImproperlyConfigured('django CMS requires django-mptt package.')

    if app_is_installed('reversion'):
        from reversion.admin import VersionAdmin
        if not hasattr(VersionAdmin, 'get_urls'):
            raise ImproperlyConfigured('django CMS requires newer version of reversion (VersionAdmin must contain get_urls method)')


def validate_settings():
    """
    Check project settings file for required options
    """
    ctx_present = False

    if django.VERSION < (1, 8,):
        request_ctx = 'django.core.context_processors.request'
        if 'django.core.context_processors.request' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            ctx_present = True
    else:
        request_ctx = 'django.template.context_processors.request'
        for engine in template.engines.templates.values():
            if request_ctx in engine.get('OPTIONS', {})\
                    .get('context_processors', []):
                ctx_present = True
                break

    if not ctx_present:
        raise ImproperlyConfigured(
            'django CMS requires %s in settings.TEMPLATE_CONTEXT_PROCESSORS to work correctly.' % request_ctx
        )


def setup():
    """
    Gather all checks and validations
    """
    validate_dependencies()
    validate_settings()
