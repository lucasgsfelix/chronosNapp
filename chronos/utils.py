"""Utility features for all backends"""
from datetime import datetime

def now():
    return datetime.utcnow().isoformat()

def validate_timestamp(start, end):
    """Method use for validate the time stamp.

    Avoiding that end be smaller than start.
    """
    
    if start > end:
        raise Exception("Invalid Data Range: {}, {}".format(start, end)
