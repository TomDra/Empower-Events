"""
Validators for the FeedbackAPI app.
"""
from django.core.exceptions import ValidationError
from textblob import TextBlob


def validate_feedback_text(value):
    """
    A method to validate the feedback text by spellchecking it and checking its length.

    :param value: The feedback text to validate.
    :return: The spellchecked feedback text.
    """

    # Check if the feedback text is too long
    if value:
        if len(value) > 500:
            raise ValidationError('Feedback text is too long. Maximum length is 500 characters.')

        # Spellcheck the feedback text
        spellchecked_text = TextBlob(value).correct()

        return str(spellchecked_text)
    else:
        return value

