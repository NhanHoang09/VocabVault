# Application constants

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/ogg"]

# Learning
MEMORY_STRENGTH_MIN = 1
MEMORY_STRENGTH_MAX = 5
EASE_FACTOR_MIN = 130
EASE_FACTOR_MAX = 250
EASE_FACTOR_DEFAULT = 250

# Quiz
QUIZ_TYPES = ["multiple_choice", "fill_blank", "matching", "speaking"]
QUIZ_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

# Conversation
CONVERSATION_TYPES = ["casual", "business", "academic", "travel"]
AI_PERSONALITY_TYPES = ["friendly", "professional", "casual", "formal"]

# Cache
CACHE_TTL = 3600  # 1 hour
REDIS_KEY_PREFIX = "vocabulary_vault:"

# Security
PASSWORD_MIN_LENGTH = 6
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 50
