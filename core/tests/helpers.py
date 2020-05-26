import random
from core.models import User

DEFAULT_PASSWORD = 'Passw0rd!'


def create_user(password=DEFAULT_PASSWORD):
    user = User.objects.create_user(
        username='jklimber' + str(random.randint(111111,999999)),
        first_name='Joseph',
        last_name='Klimber',
        email='jklimber@wfl.es',
        password=password
    )

    return user