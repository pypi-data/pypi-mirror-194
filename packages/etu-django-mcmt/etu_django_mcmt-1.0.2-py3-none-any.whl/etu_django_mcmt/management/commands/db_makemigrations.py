from django import get_version

if get_version() < '2.2.2':
    raise RuntimeError('The Django version must be >= 2.2.2')

elif '2.2.1' < get_version() < '3.0.0':
    from etu_django_mcmt.core.ver_222.makemigrations import Command as CustomCommand

else:
    from etu_django_mcmt.core.ver_3213.makemigrations import Command as CustomCommand


class Command(CustomCommand):
    pass
