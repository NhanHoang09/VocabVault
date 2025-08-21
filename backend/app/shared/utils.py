import hashlib
import uuid
from datetime import datetime, timezone
from typing import Optional, Any, Dict
import re


def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


def hash_string(text: str) -> str:
    """Hash a string using SHA-256"""
    return hashlib.sha256(text.encode()).hexdigest()


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO datetime string"""
    return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:255-len(ext)-1] + '.' + ext
    return filename


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """Validate username format"""
    pattern = r'^[a-zA-Z0-9_-]{3,50}$'
    return re.match(pattern, username) is not None


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def build_cache_key(*args: Any) -> str:
    """Build cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    return ":".join(key_parts)


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries, dict2 takes precedence"""
    result = dict1.copy()
    result.update(dict2)
    return result


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""


def is_valid_file_type(filename: str, allowed_types: list) -> bool:
    """Check if file type is allowed"""
    ext = get_file_extension(filename)
    return ext in allowed_types


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def mask_sensitive_data(data: str, mask_char: str = '*') -> str:
    """Mask sensitive data like email or phone"""
    if '@' in data:  # Email
        username, domain = data.split('@')
        masked_username = username[0] + mask_char * (len(username) - 2) + username[-1] if len(username) > 2 else username
        return f"{masked_username}@{domain}"
    else:  # Phone or other
        if len(data) <= 4:
            return data
        return data[0] + mask_char * (len(data) - 2) + data[-1]
