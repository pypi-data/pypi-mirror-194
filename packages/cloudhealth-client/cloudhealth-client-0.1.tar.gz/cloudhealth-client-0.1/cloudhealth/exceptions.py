
# All exceptions should subclass from Boto3Error in this module.

class CloudHealthError(Exception):
    """Base class for all CloudHealth errors."""
    pass

