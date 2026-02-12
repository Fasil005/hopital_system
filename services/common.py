from django.http import HttpRequest


def decrypt_field(encryption_service, value):
    """
    Decrypt a value safely.
    """
    if not value:
        return None
    return encryption_service.decrypt(value)


def mask(value, prefix="****"):
    """
    Mask a value by showing only last 4 characters.
    """
    if not value:
        return None
    return f"{prefix}{value[-4:]}"


def get_client_ip(request: HttpRequest):
    """
    Extract client IP address from request.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    return request.META.get("REMOTE_ADDR")
