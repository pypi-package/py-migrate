class MigrationError(Exception):
    pass

class ChecksumMismatch(MigrationError):
    pass

class MigrationLocked(MigrationError):
    pass
