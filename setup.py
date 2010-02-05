from distutils.core import setup

setup(
    name = "django-lighty",
    version = '0.1',
    url = '',
    author = 'Justin Quick',
    description = 'Validates form input before submitting',
    packages = ['lighty','lighty.management','lighty.management.commands']
)
