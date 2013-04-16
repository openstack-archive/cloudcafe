
class _CommonStatuses(object):
    AVAILABLE = "available"
    DELETING = "deleting"


class VolumeStatuses(_CommonStatuses):
    ATTACHING = "attaching"


class SnapshotStatuses(_CommonStatuses):
    pass
