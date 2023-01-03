from django.contrib.auth.tokens import PasswordResetTokenGenerator
from urllib3.packages.six import text_type


class AccActivateToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type((user.is_active + user.pk + timestamp))


token_generator = AccActivateToken()