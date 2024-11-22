import secrets
import string

def generate_password(length=16):
    """Generate a secure password with letters, digits, and special characters."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_django_secret_key(length=50):
    """Generate a Django SECRET_KEY."""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_credentials():
    """Generate secure credentials for environment variables."""
    credentials = {
        "POSTGRES_PASSWORD": generate_password(20),
        "RABBITMQ_DEFAULT_PASS": generate_password(20),
        "DJANGO_SECRET_KEY": generate_django_secret_key(),
        "DJANGO_ADMIN_PASSWORD": generate_password(20)
    }
    return credentials

# Example Usage
if __name__ == "__main__":
    credentials = generate_credentials()
    for key, value in credentials.items():
        print(f"{key}: {value}")
