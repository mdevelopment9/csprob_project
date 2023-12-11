"""
Module for the RT60Toolbar class
"""
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class RT60Toolbar(NavigationToolbar2Tk):
    """
    View class for a custom toolbar for the RT60 graphs
    """
    def __init__(self, canvas_, parent_):
        self.prev_rt60 = parent_.prev_rt60
        self.next_rt60 = parent_.next_rt60
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None), #these are separators in matplotlib
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            (None, None, None, None),
            ('Previous plot', 'Previous RT60 plot', 'back', 'prev_rt60'),
            ('Next plot', 'Next RT60 plot', 'forward', 'next_rt60')
        )
        super().__init__(canvas_, parent_)

