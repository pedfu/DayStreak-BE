import random
import string

PASSWORD_CHARSET = string.ascii_uppercase + string.ascii_lowercase + string.digits

def generate_password():
    return ''.join([random.choice(PASSWORD_CHARSET) for _ in range(random.randint(6, 8))])