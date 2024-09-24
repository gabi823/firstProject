from django.core.exceptions import ValidationError
import re

class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not re.search(r'[\W_]', password):
            raise ValidationError(
                "Password must contain at least one special character."
            )

    def get_help_text(self):
        return "Your password must contain at least one special character."