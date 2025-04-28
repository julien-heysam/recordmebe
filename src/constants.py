from enum import Enum


class Envs(Enum):
    DEV = "DEV"
    PROD = "PROD"
    LOCAL = "LOCAL"
    STAGING = "STAGING"


class LogLevels(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Statues(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
