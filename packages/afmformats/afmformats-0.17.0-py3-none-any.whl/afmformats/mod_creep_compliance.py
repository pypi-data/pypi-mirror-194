from .afm_data import AFMData
from .afm_segment import AFMSegment


__all__ = ["AFMCreepCompliance"]


class AFMCreepCompliance(AFMData):
    """Base class for AFM creep-compliance data

    A creep-compliance dataset consists of an approach,
    an intermediate (with constant Force), and a retract curve.
    """
    def __init__(self, *args, **kwargs):
        super(AFMCreepCompliance, self).__init__(*args, **kwargs)
        #: Dictionary-like interface to the approach segment
        self.appr = AFMSegment(self._raw_data, self._data, segment=0)
        #: Dictionary-like interface to the intermediate segment
        self.intr = AFMSegment(self._raw_data, self._data, segment=1)
        #: Dictionary-like interface to the retract segment
        self.retr = AFMSegment(self._raw_data, self._data, segment=2)

    def __setitem__(self, key, value):
        super(AFMCreepCompliance, self).__setitem__(key, value)
        if key == "segment":
            # The user changed the segment, which means we have to clear
            # the segment cache.
            self.appr.clear_cache()
            self.intr.clear_cache()
            self.retr.clear_cache()

    @property
    def modality(self):
        """Imaging modality"""
        return "creep-compliance"
