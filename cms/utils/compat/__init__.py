from distutils.version import LooseVersion
import django


# These means "at least DJANGO_FOO_BAR
DJANGO_1_7 = LooseVersion(django.get_version()) < LooseVersion('1.8')
