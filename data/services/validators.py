import re


async def validate_email(email):
    result = await re.match("[^@]+@[^@]+\.[^@]+", email)
    if result:
        return True
