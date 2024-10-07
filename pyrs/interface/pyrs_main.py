from qtpy.QtWidgets import QMainWindow  # type:ignore
from pyrs.utilities import load_ui  # type: ignore
from pyrs.core import pyrscore
from pyrs.interface.peak_fitting import fitpeakswindow
from pyrs.interface.manual_reduction import manualreductionwindow

try:
    import vtk.qt
    # https://stackoverflow.com/questions/51357630/vtk-rendering-not-working-as-expected-inside-pyqt
    vtk.qt.QVTKRWIBase = "QGLWidget"  # noqa: E402
except ImportError:
    # if vtk is not aviable we will disable the 3D viewer
    pass
from pyrs.interface.strainstressviewer.strain_stress_view import StrainStressViewer  # noqa: E402
from pyrs.interface.strainstressviewer.model import Model  # noqa: E402
from pyrs.interface.strainstressviewer.controller import Controller  # noqa: E402

from pyrs.interface.texture_fitting.texture_fitting_viewer import TextureFittingViewer  # noqa: E402
from pyrs.interface.texture_fitting.texture_fitting_model import TextureFittingModel  # noqa: E402
from pyrs.interface.texture_fitting.texture_fitting_crtl import TextureFittingCrtl  # noqa: E402

from pyrs.interface.detector_calibration.detector_calibration_viewer import DetectorCalibrationViewer  # noqa: E402
from pyrs.interface.detector_calibration.detector_calibration_model import DetectorCalibrationModel  # noqa: E402
from pyrs.interface.detector_calibration.detector_calibration_crtl import DetectorCalibrationCrtl  # noqa: E402

from pyrs.interface.combine_runs.combine_runs_viewer import CombineRunsViewer  # noqa: E402
from pyrs.interface.combine_runs.combine_runs_model import CombineRunsModel  # noqa: E402
from pyrs.interface.combine_runs.combine_runs_crtl import CombineRunsCrtl  # noqa: E402


class PyRSLauncher(QMainWindow):
    """
    The main window launched for PyRS
    """

    def __init__(self):
        """
        initialization
        """
        super(PyRSLauncher, self).__init__(None)

        # set up UI
        self.ui = load_ui('pyrsmain.ui', baseinstance=self)

        # define
        self.ui.pushButton_manualReduction.clicked.connect(self.do_launch_manual_reduction)
        self.ui.pushButton_fitPeaks.clicked.connect(self.do_launch_fit_peak_window)
        self.ui.pushButton_fitTexture.clicked.connect(self.do_launch_fit_texture_window)
        self.ui.pushButton_launchStrainStressCalculation.clicked.connect(self.do_launch_strain_stress_window)

        self.ui.actionQuit.triggered.connect(self.do_quit)
        self.ui.actionCalibration.triggered.connect(self.do_launch_calibration_window)
        self.ui.actionCombine_Runs.triggered.connect(self.do_launch_combeineruns)

        # child windows
        self.peak_fit_window = None
        self.manual_reduction_window = None
        self.strain_stress_window = None
        self.texture_fit_window = None
        self.combine_run_window = None

    def do_launch_fit_texture_window(self):
        """
        launch peak fit window
        :return:
        """
        if self.texture_fit_window is not None:
            self.texture_fit_window.close()

        self.texture_fitting_model = TextureFittingModel(pyrscore.PyRsCore())
        self.texture_fitting_ctrl = TextureFittingCrtl(self.texture_fitting_model)
        self.texture_fit_window = TextureFittingViewer(self.texture_fitting_model, self.texture_fitting_ctrl)

        # launch
        self.texture_fit_window.show()

    def do_launch_combeineruns(self):
        if self.combine_run_window is not None:
            self.combine_run_window.close()

        self.combine_runs_model = CombineRunsModel()
        self.combine_runs_ctrl = CombineRunsCrtl(self.combine_runs_model)
        self.combine_run_window = CombineRunsViewer(self.combine_runs_model, self.combine_runs_ctrl)

        # launch
        self.combine_run_window.show()

    def do_launch_calibration_window(self):
        """
        launch peak fit window
        :return:
        """
        if self.texture_fit_window is not None:
            self.texture_fit_window.close()

        self.calibration_model = DetectorCalibrationModel(pyrscore.PyRsCore())
        self.calibration_ctrl = DetectorCalibrationCrtl(self.calibration_model)
        self.calibration_window = DetectorCalibrationViewer(self.calibration_model, self.calibration_ctrl)

        # launch
        self.calibration_window.show()

    def do_launch_fit_peak_window(self):
        """
        launch peak fit window
        :return:
        """
        # core
        fit_peak_core = pyrscore.PyRsCore()

        # set up interface object
        # if self.peak_fit_window is None:
        self.peak_fit_window = fitpeakswindow.FitPeaksWindow(self, fit_peak_core=fit_peak_core)
        self.peak_fit_window.show()

    def do_launch_manual_reduction(self):
        """
        launch manual data reduction window
        :return:
        """
        if self.manual_reduction_window is None:
            self.manual_reduction_window = manualreductionwindow.ManualReductionWindow(self)

        # show
        self.manual_reduction_window.show()

    def do_launch_strain_stress_window(self):
        """
        launch the strain/stress calculation and visualization window
        """

        if self.strain_stress_window is not None:
            self.strain_stress_window.close()

        self.strain_stress_model = Model()
        self.strain_stress_ctrl = Controller(self.strain_stress_model)
        self.strain_stress_window = StrainStressViewer(self.strain_stress_model, self.strain_stress_ctrl)

        # launch
        self.strain_stress_window.show()

    def do_quit(self):
        """
        close window
        :return:
        """
        # close all 5 child windows
        if self.peak_fit_window is not None:
            self.peak_fit_window.close()

        if self.manual_reduction_window is not None:
            self.manual_reduction_window.close()

        if self.strain_stress_window is not None:
            self.strain_stress_window.close()

        self.close()
