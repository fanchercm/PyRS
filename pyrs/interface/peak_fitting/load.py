import os

from pyrs.interface.gui_helper import pop_message
from pyrs.interface.peak_fitting.gui_utilities import GuiUtilities
from pyrs.interface.peak_fitting.utilities import Utilities
from pyrs.projectfile import HidraProjectFile  # type: ignore


class Load:

    def __init__(self, parent=None):
        self.parent = parent

    def load(self, project_file=None):
        if project_file is None:
            return
        elif len(project_file) == 1:
            project_file = project_file[0]
            try:
                self.__set_up_project_name(project_file=project_file)
                ws = self.parent._core.load_hidra_project(project_file,
                                                          project_name=self.parent._project_name,
                                                          load_detector_counts=False,
                                                          load_diffraction=True)

                # Record data key and next
                self.parent._curr_file_name = project_file
                self.parent.hidra_workspace = ws
                self.parent.fit_result = None
                self.parent.create_plot_color_range()
            except (RuntimeError, TypeError) as run_err:
                pop_message(self, 'Unable to load {}'.format(project_file),
                            detailed_message=str(run_err),
                            message_type='error')
        else:
            self.parent._curr_file_name = project_file[0]
            self.parent.hidra_workspace = self.__load_multiple_file(project_file)
            self.parent.fit_result = None
            self.parent.create_plot_color_range()

        # Get and set the range of sub runs
        o_utility = Utilities(parent=self.parent)
        sub_run_list = o_utility.get_subruns_limit()

        o_gui = GuiUtilities(parent=self.parent)
        o_gui.initialize_fitting_slider(max=len(sub_run_list))

        o_gui.set_1D_2D_axis_comboboxes(with_clear=True, fill_raw=True)
        o_gui.enabled_1dplot_widgets(enabled=True)
        o_gui.initialize_combobox()

        self.parent.ui.graphicsView_plot2D.reset_viewer()

    def __load_multiple_file(self, project_files):
        _hidra_ws = self.parent._core.load_hidra_project(project_files[0],
                                                         project_name=self.parent._project_name,
                                                         load_detector_counts=False,
                                                         load_diffraction=True)

        for project in project_files[1:]:
            _project = HidraProjectFile(project)
            _hidra_ws.append_hidra_project(_project)
            _project.close()

        return _hidra_ws

    def __set_up_project_name(self, project_file=""):
        """Keep the basename and removed the nxs and h5 extenstions"""
        self.parent._project_name = os.path.basename(project_file).split('.')[0]
