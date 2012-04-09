import numpy as N
from traits.api import HasTraits, Bool, Float, Array, Instance, Property
from traitsui.api import View, VGroup, Item
from pyface.timer.api import do_after
from CameraImage import *

class DeltaDetector(HasTraits):

    active = Bool(False)
    threshold = Range(low=0.0, high=10000.0, value=20.0)
    frame = Array(dtype=float)
    screen = Instance(CameraImage)
    average = Property(depends_on='frame')

    view = View(
        VGroup(
            Item('active'),
            Item('threshold'),
            label='Delta Detector',
            show_border=True))

    def __init__(self, **traits):
        self._previous_frame = None
        self._timed_out = False
        HasTraits.__init__(self, **traits)
    
    def _frame_changed(self, old, new):
        self._previous_frame = old
        
        if self._timed_out or not self.active or self._previous_frame is None:
            return
        if(self._previous_frame.shape != self.frame.shape):
            self._previous_frame = None
            return
        
        maximum_delta = N.max(N.abs(self.frame - self._previous_frame))
        if maximum_delta > self.threshold:
            print 'BEEP'  # FIXME
            
            # Don't beep more than once per second
            self._timed_out = True
            do_after(1000, self._switch_on_timeout)

        #self.screen.hud('delta',
        #    'Current average delta: {:.3f}\n'.format(self.average)
        #    + 'Current maximum delta: {:.3f}'.format(maximum_delta))

    def _switch_on_timeout(self):
        self._timed_out = False

    #def _active_changed(self, value):
    #    if not value:
    #        self.screen.hud('delta', None)

    def _get_average(self):
        if self.frame is None or self._previous_frame is None:
            return 0.0
        return N.mean(self.frame - self._previous_frame)
