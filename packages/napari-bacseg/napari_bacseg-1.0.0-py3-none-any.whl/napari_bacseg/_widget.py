"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""

import mahotas
from qtpy.QtWidgets import (QWidget,QVBoxLayout,QTabWidget,QCheckBox,QLabel,QLineEdit,QFileDialog,
                            QComboBox,QPushButton,QProgressBar,QTextEdit,QSlider, QRadioButton, QFormLayout)
from qtpy.QtCore import (QObject,QRunnable,QThreadPool)
from PyQt5.QtCore import pyqtSignal,pyqtSlot
import sys
from functools import partial,wraps, update_wrapper
import os
import traceback
import napari
import numpy as np
import time
import cv2
import pandas as p
from glob2 import glob
import napari_bacseg._utils
from napari_bacseg._utils import unstack_images, align_image_channels
import tempfile
import shutil
from napari.utils.notifications import show_info

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

    def result(self):

        return self.fn(*self.args, **self.kwargs)






class BacSeg(QWidget):
    """Widget allows selection of two labels layers and returns a new layer
      highlighing pixels whose values differ between the two layers."""

    def __init__(self, viewer: napari.Viewer):
        """Initialize widget with two layer combo boxes and a run button

        """

        super().__init__()

        # import functions
        from napari_bacseg._utils_database import (populate_upload_combos, _populateUSERMETA, update_database_metadata,
                                                   _create_bacseg_database, _load_bacseg_database, _show_database_controls)
        from napari_bacseg._utils import stack_images, _manualImport
        from napari_bacseg._utils_tiler import unfold_images, fold_images, update_image_folds
        from napari_bacseg._utils_statistics import _compute_simple_cell_stats
        from napari_bacseg.bacseg_ui import Ui_tab_widget
        from napari_bacseg._utils_oufti import midline_edit_toggle,centre_oufti_midlines,generate_midlines, update_midlines, _update_active_midlines
        from napari_bacseg._utils_cellpose import train_cellpose_model, _initialise_cellpose_model, _select_custom_cellpose_model, _select_cellpose_save_directory,_select_cellpose_save_path
        from napari_bacseg._utils_interface_events import (_modifyMode, _viewerControls, _copymasktoall,
                                                          _deleteallmasks, _imageControls, _segmentationEvents,
                                                          _delete_active_image, _doubeClickEvents)


        self.populate_upload_combos = partial(populate_upload_combos, self)
        self.update_database_metadata = partial(update_database_metadata, self)
        self.stack_image = partial(stack_images, self)
        self._modifyMode = partial(_modifyMode, self)
        self._viewerControls = partial(_viewerControls, self)
        self._copymasktoall = partial(_copymasktoall, self)
        self._deleteallmasks = partial(_deleteallmasks, self)
        self._delete_active_image = partial(_delete_active_image,self)
        self._populateUSERMETA = partial(_populateUSERMETA, self)
        self._imageControls = partial(_imageControls, self)
        self._segmentationEvents = partial(_segmentationEvents, self)
        self._manualImport = partial(_manualImport, self)
        self.train_cellpose_model = partial(train_cellpose_model, self)
        self._initialise_cellpose_model = partial(_initialise_cellpose_model, self)
        self._select_custom_cellpose_model = partial(_select_custom_cellpose_model, self)
        self._select_cellpose_save_directory = partial(_select_cellpose_save_directory, self)
        self._select_cellpose_save_path = partial(_select_cellpose_save_path, self)
        self.unfold_images = partial(unfold_images, self)
        self.fold_images = partial(fold_images, self)
        self.update_image_folds = partial(update_image_folds, self)
        self.midline_edit_toggle = partial(midline_edit_toggle, self)
        self.centre_oufti_midlines = partial(centre_oufti_midlines, self)
        self.generate_midlines = partial(generate_midlines, self)
        self.update_midlines = partial(update_midlines, self)
        self._update_active_midlines = partial(_update_active_midlines, self)
        self._create_bacseg_database = partial(_create_bacseg_database, self)
        self._load_bacseg_database = partial(_load_bacseg_database, self)
        self._show_database_controls = partial(_show_database_controls, self)
        self._doubeClickEvents = partial(_doubeClickEvents, self)
        self._compute_simple_cell_stats = partial(_compute_simple_cell_stats, self)


        application_path = os.path.dirname(sys.executable)
        self.viewer = viewer
        self.setLayout(QVBoxLayout())

        # ui_path = os.path.abspath(r"C:\napari-bacseg\src\napari_bacseg\bacseg_ui.ui")
        # self.bacseg_ui = uic.loadUi(ui_path)
        #command to refresh ui file: pyuic5 bacseg_ui.ui -o bacseg_ui.py

        self.form = Ui_tab_widget()
        self.bacseg_ui = QTabWidget()
        self.form.setupUi(self.bacseg_ui)

        # add widget_gui layout to main layout
        self.layout().addWidget(self.bacseg_ui)

        # general references from Qt Desinger References
        self.tab_widget = self.findChild(QTabWidget, "tab_widget")

        # import controls from Qt Desinger References
        self.path_list = []
        self.active_import_mode = ""
        self.import_mode = self.findChild(QComboBox, "import_mode")
        self.import_filemode = self.findChild(QComboBox, "import_filemode")
        self.import_precision = self.findChild(QComboBox, "import_precision")
        self.import_import = self.findChild(QPushButton, "import_import")
        self.import_limit = self.findChild(QComboBox, "import_limit")
        self.import_limit_label = self.findChild(QLabel, "import_limit_label")
        self.clear_previous = self.findChild(QCheckBox, "import_clear_previous")
        self.autocontrast = self.findChild(QCheckBox, "import_auto_contrast")
        self.import_multiframe_mode = self.findChild(QComboBox, "import_multiframe_mode")
        self.import_crop_mode = self.findChild(QComboBox, "import_crop_mode")
        self.channel_mode = self.findChild(QComboBox, "nim_channel_mode")
        self.import_progressbar = self.findChild(QProgressBar, "import_progressbar")
        self.import_align = self.findChild(QCheckBox, "import_align")
        self.label_modality = self.findChild(QComboBox, "label_modality")
        self.label_stain = self.findChild(QComboBox, "label_stain")
        self.label_stain_target = self.findChild(QComboBox, "label_stain_target")
        self.label_overwrite = self.findChild(QPushButton, "label_overwrite")
        self.label_light_source = self.findChild(QComboBox, "label_light_source")

        #view tab controls + variables from Qt Desinger References
        self.unfold_tile_size = self.findChild(QComboBox,"unfold_tile_size")
        self.unfold_tile_overlap = self.findChild(QComboBox, "unfold_tile_overlap")
        self.unfold_mode = self.findChild(QComboBox, "unfold_mode")
        self.fold = self.findChild(QPushButton,"fold")
        self.unfold = self.findChild(QPushButton,"unfold")
        self.unfold_progressbar = self.findChild(QPushButton,"unfold_progressbar")

        # cellpose controls + variables from Qt Desinger References
        self.cellpose_segmentation = False
        self.cellpose_model = None
        self.cellpose_custom_model_path = ""
        self.cellpose_train_model_path = ""
        self.cellpose_log_file = None
        self.cellpose_select_custom_model = self.findChild(QPushButton, "cellpose_select_custom_model")
        self.cellpose_segmodel = self.findChild(QComboBox, "cellpose_segmodel")
        self.cellpose_trainmodel = self.findChild(QComboBox, "cellpose_trainmodel")
        self.cellpose_segchannel = self.findChild(QComboBox, "cellpose_segchannel")
        self.cellpose_flowthresh = self.findChild(QSlider, "cellpose_flowthresh")
        self.cellpose_flowthresh_label = self.findChild(QLabel, "cellpose_flowthresh_label")
        self.cellpose_maskthresh = self.findChild(QSlider, "cellpose_maskthresh")
        self.cellpose_maskthresh_label = self.findChild(QLabel, "cellpose_maskthresh_label")
        self.cellpose_minsize = self.findChild(QSlider, "cellpose_minsize")
        self.cellpose_minsize_label = self.findChild(QLabel, "cellpose_minsize_label")
        self.cellpose_diameter = self.findChild(QSlider, "cellpose_diameter")
        self.cellpose_diameter_label = self.findChild(QLabel, "cellpose_diameter_label")
        self.cellpose_segment_active = self.findChild(QPushButton, "cellpose_segment_active")
        self.cellpose_segment_all = self.findChild(QPushButton, "cellpose_segment_all")
        self.cellpose_clear_previous = self.findChild(QCheckBox, "cellpose_clear_previous")
        self.cellpose_usegpu = self.findChild(QCheckBox, "cellpose_usegpu")
        self.cellpose_resetimage = self.findChild(QCheckBox, "cellpose_resetimage")
        self.cellpose_progressbar = self.findChild(QProgressBar, "cellpose_progressbar")
        self.cellpose_train_model = self.findChild(QPushButton, "cellpose_train_model")
        self.cellpose_save_dir = self.findChild(QPushButton, "cellpose_save_dir")
        self.cellpose_trainchannel = self.findChild(QComboBox, "cellpose_trainchannel")
        self.cellpose_nepochs = self.findChild(QComboBox, "cellpose_nepochs")
        self.cellpose_batchsize = self.findChild(QComboBox, "cellpose_batchsize")

        # modify tab controls + variables from Qt Desinger References
        self.interface_mode = "panzoom"
        self.segmentation_mode = "add"
        self.class_mode = "single"
        self.class_colour = 1
        self.modify_panzoom = self.findChild(QPushButton, "modify_panzoom")
        self.modify_segment = self.findChild(QPushButton, "modify_segment")
        self.modify_classify = self.findChild(QPushButton, "modify_classify")
        self.modify_refine = self.findChild(QPushButton, "modify_refine")
        self.refine_channel = self.findChild(QComboBox, "refine_channel")
        self.refine_all = self.findChild(QPushButton, "refine_all")
        self.modify_copymasktoall = self.findChild(QPushButton, "modify_copymasktoall")
        self.modify_deleteallmasks = self.findChild(QPushButton, "modify_deleteallmasks")
        self.modify_deleteactivemasks = self.findChild(QPushButton, "modify_deleteactivemasks")
        self.modify_deleteactiveimage = self.findChild(QPushButton, "modify_deleteactiveimage")
        self.modify_deleteotherimages = self.findChild(QPushButton, "modify_deleteotherimages")
        self.modify_progressbar = self.findChild(QProgressBar, "modify_progressbar")

        self.modify_auto_panzoom = self.findChild(QCheckBox, "modify_auto_panzoom")
        self.modify_add = self.findChild(QPushButton, "modify_add")
        self.modify_extend = self.findChild(QPushButton, "modify_extend")
        self.modify_split = self.findChild(QPushButton, "modify_split")
        self.modify_join = self.findChild(QPushButton, "modify_join")
        self.modify_delete = self.findChild(QPushButton, "modify_delete")
        self.classify_single = self.findChild(QPushButton, "classify_single")
        self.classify_dividing = self.findChild(QPushButton, "classify_dividing")
        self.classify_divided = self.findChild(QPushButton, "classify_divided")
        self.classify_vertical = self.findChild(QPushButton, "classify_vertical")
        self.classify_broken = self.findChild(QPushButton, "classify_broken")
        self.classify_edge = self.findChild(QPushButton, "classify_edge")
        self.modify_viewmasks = self.findChild(QCheckBox, "modify_viewmasks")
        self.modify_viewlabels = self.findChild(QCheckBox, "modify_viewlabels")
        self.find_next = self.findChild(QPushButton, 'find_next')
        self.find_previous = self.findChild(QPushButton, 'find_previous')
        self.find_criterion = self.findChild(QComboBox, "find_criterion")
        self.find_mode = self.findChild(QComboBox, "find_mode")

        self.modify_panzoom.setEnabled(False)
        self.modify_add.setEnabled(False)
        self.modify_extend.setEnabled(False)
        self.modify_join.setEnabled(False)
        self.modify_split.setEnabled(False)
        self.modify_delete.setEnabled(False)
        self.modify_refine.setEnabled(False)
        self.classify_single.setEnabled(False)
        self.classify_dividing.setEnabled(False)
        self.classify_divided.setEnabled(False)
        self.classify_vertical.setEnabled(False)
        self.classify_broken.setEnabled(False)
        self.classify_edge.setEnabled(False)

        # upload tab controls from Qt Desinger References
        self.database_path = ""
        self.metadata_columns = ["date_uploaded","date_created","date_modified","file_name","channel","file_list",
                                 "channel_list","segmentation_file","segmentation_channel","akseg_hash","user_initial",
                                 "content","microscope","modality","source","stain","stain_target","antibiotic",
                                 "treatment time (mins)","antibiotic concentration","mounting method","protocol",
                                 "user_meta1","user_meta2","user_meta3","folder","parent_folder","num_segmentations",
                                 "segmented","labelled","segmentation_curated","label_curated","posX","posY","posZ",
                                 "image_load_path","image_save_path","mask_load_path","mask_save_path",
                                 "label_load_path","label_save_path"]

        self.upload_initial = self.findChild(QComboBox, "upload_initial")
        self.upload_content = self.findChild(QComboBox, "upload_content")
        self.upload_microscope = self.findChild(QComboBox, "upload_microscope")
        self.upload_antibiotic = self.findChild(QComboBox, "upload_antibiotic")
        self.upload_abxconcentration = self.findChild(QComboBox, "upload_abxconcentration")
        self.upload_treatmenttime = self.findChild(QComboBox, "upload_treatmenttime")
        self.upload_mount = self.findChild(QComboBox, "upload_mount")
        self.upload_protocol = self.findChild(QComboBox, "upload_protocol")
        self.upload_usermeta1 = self.findChild(QComboBox, "upload_usermeta1")
        self.upload_usermeta2 = self.findChild(QComboBox, "upload_usermeta2")
        self.upload_usermeta3 = self.findChild(QComboBox, "upload_usermeta3")
        self.upload_overwrite_images = self.findChild(QCheckBox, "upload_overwrite_images")
        self.upload_overwrite_masks = self.findChild(QCheckBox, "upload_overwrite_masks")
        self.overwrite_selected_metadata = self.findChild(QCheckBox, "overwrite_selected_metadata")
        self.overwrite_all_metadata = self.findChild(QCheckBox, "overwrite_all_metadata")
        self.upload_all = self.findChild(QPushButton, "upload_all")
        self.upload_active = self.findChild(QPushButton, "upload_active")
        self.database_download = self.findChild(QPushButton, "database_download")
        self.database_download_limit = self.findChild(QComboBox, "database_download_limit")
        self.create_database = self.findChild(QPushButton, "create_database")
        self.load_database = self.findChild(QPushButton, "load_database")
        self.display_database_path = self.findChild(QLineEdit, "display_database_path")
        self.upload_progressbar = self.findChild(QProgressBar, "upload_progressbar")
        self.upload_tab = self.findChild(QWidget,"upload_tab")
        self.upload_segmentation_combo = self.findChild(QComboBox, "upload_segmentation_combo")
        self.upload_label_combo = self.findChild(QComboBox, "upload_label_combo")
        self.download_sort_order = self.findChild(QComboBox, "download_sort_order")
        self.update_metadata = self.findChild(QPushButton, "update_metadata")

        self.image_metadata_controls = self.findChild(QFormLayout, "image_metadata_controls")

        self._show_database_controls(False)

        #oufti tab controls
        self.oufti_generate_all_midlines = self.findChild(QPushButton, "oufti_generate_all_midlines")
        self.oufti_generate_active_midlines = self.findChild(QPushButton, "oufti_generate_active_midlines")
        self.oufti_panzoom_mode = self.findChild(QRadioButton, "oufti_panzoom_mode")
        self.oufti_edit_mode = self.findChild(QRadioButton, "oufti_edit_mode")
        self.oufti_midline_vertexes = self.findChild(QComboBox, "oufti_midline_vertexes")
        self.oufti_centre_all_midlines = self.findChild(QPushButton, "oufti_centre_all_midlines")
        self.oufti_centre_active_midlines = self.findChild(QPushButton, "oufti_centre_active_midlines")
        self.oufti_mesh_length = self.findChild(QComboBox, "oufti_mesh_length")
        self.oufti_mesh_dilation = self.findChild(QComboBox, "oufti_mesh_dilation")

        # export tab controls from Qt Desinger References
        self.export_channel = self.findChild(QComboBox, "export_channel")
        self.export_mode = self.findChild(QComboBox, "export_mode")
        self.export_location = self.findChild(QComboBox, "export_location")
        self.export_modifier = self.findChild(QLineEdit, "export_modifier")
        self.export_single = self.findChild(QCheckBox, "export_single")
        self.export_dividing = self.findChild(QCheckBox, "export_dividing")
        self.export_divided = self.findChild(QCheckBox, "export_divided")
        self.export_vertical = self.findChild(QCheckBox, "export_vertical")
        self.export_broken = self.findChild(QCheckBox, "export_broken")
        self.export_edge = self.findChild(QCheckBox, "export_edge")
        self.export_statistics_multithreaded = self.findChild(QCheckBox, "export_statistics_multithreaded")
        self.export_active = self.findChild(QPushButton, "export_active")
        self.export_all = self.findChild(QPushButton, "export_all")
        self.export_normalise = self.findChild(QCheckBox, "export_normalise")
        self.export_invert = self.findChild(QCheckBox, "export_invert")
        self.export_autocontrast = self.findChild(QCheckBox, "export_autocontrast")
        self.export_statistics_pixelsize = self.findChild(QLineEdit, 'export_statistics_pixelsize')
        self.export_statistics_active = self.findChild(QPushButton, "export_statistics_active")
        self.export_statistics_all = self.findChild(QPushButton, "export_statistics_all")
        self.export_colicoords_mode = self.findChild(QComboBox, "export_colicoords_mode")
        self.export_progressbar = self.findChild(QProgressBar, "export_progressbar")
        self.export_image_setting = self.findChild(QCheckBox, "export_image_setting")
        self.export_overwrite_setting = self.findChild(QCheckBox, "export_overwrite_setting")
        self.export_directory = ""

        # import events
        self.autocontrast.stateChanged.connect(self._autoContrast)
        self.import_import.clicked.connect(self._importDialog)
        self.label_overwrite.clicked.connect(self.overwrite_channel_info)

        #view events
        self.fold.clicked.connect(self.fold_images)
        self.unfold.clicked.connect(self.unfold_images)
        self.tiler_object = None
        self.tile_dict = {"Segmentations": [],"Classes": []}
        self.unfolded = False


        # cellpose events
        self.cellpose_flowthresh.valueChanged.connect(lambda: self._updateSliderLabel("cellpose_flowthresh",
                                                                                      "cellpose_flowthresh_label"))
        self.cellpose_maskthresh.valueChanged.connect(lambda: self._updateSliderLabel("cellpose_maskthresh"
                                                                                      , "cellpose_maskthresh_label"))
        self.cellpose_minsize.valueChanged.connect(lambda: self._updateSliderLabel("cellpose_minsize",
                                                                                   "cellpose_minsize_label"))
        self.cellpose_diameter.valueChanged.connect(lambda: self._updateSliderLabel("cellpose_diameter",
                                                                                    "cellpose_diameter_label"))

        self.cellpose_select_custom_model.clicked.connect(self._select_custom_cellpose_model)
        self.cellpose_save_dir.clicked.connect(self._select_cellpose_save_directory)
        self.cellpose_segment_all.clicked.connect(self._segmentAll)
        self.cellpose_segment_active.clicked.connect(self._segmentActive)
        self.cellpose_train_model.clicked.connect(self._trainCellpose)
        self.cellpose_segchannel.currentTextChanged.connect(self._updateSegChannels)


        # modify tab events
        self.modify_panzoom.clicked.connect(partial(self._modifyMode, "panzoom"))
        self.modify_segment.clicked.connect(partial(self._modifyMode, "segment"))
        self.modify_classify.clicked.connect(partial(self._modifyMode, "classify"))
        self.modify_refine.clicked.connect(partial(self._modifyMode, "refine"))
        self.modify_add.clicked.connect(partial(self._modifyMode, "add"))
        self.modify_extend.clicked.connect(partial(self._modifyMode, "extend"))
        self.modify_join.clicked.connect(partial(self._modifyMode, "join"))
        self.modify_split.clicked.connect(partial(self._modifyMode, "split"))
        self.modify_delete.clicked.connect(partial(self._modifyMode, "delete"))
        self.classify_single.clicked.connect(partial(self._modifyMode, "single"))
        self.classify_dividing.clicked.connect(partial(self._modifyMode, "dividing"))
        self.classify_divided.clicked.connect(partial(self._modifyMode, "divided"))
        self.classify_vertical.clicked.connect(partial(self._modifyMode, "vertical"))
        self.classify_broken.clicked.connect(partial(self._modifyMode, "broken"))
        self.classify_edge.clicked.connect(partial(self._modifyMode, "edge"))
        self.modify_viewmasks.stateChanged.connect(partial(self._viewerControls, "viewmasks"))
        self.modify_viewlabels.stateChanged.connect(partial(self._viewerControls, "viewlabels"))
        self.refine_all.clicked.connect(self._refine_bacseg)
        self.modify_copymasktoall.clicked.connect(self._copymasktoall)
        self.modify_deleteallmasks.clicked.connect(partial(self._deleteallmasks, mode = "all"))
        self.modify_deleteactivemasks.clicked.connect(partial(self._deleteallmasks, mode="active"))
        self.modify_deleteactiveimage.clicked.connect(partial(self._delete_active_image, mode="active"))
        self.modify_deleteotherimages.clicked.connect(partial(self._delete_active_image, mode="other"))
        self.find_next.clicked.connect(partial(self._sort_cells, "next"))
        self.find_previous.clicked.connect(partial(self._sort_cells, "previous"))

        # export events
        self.export_active.clicked.connect(partial(self._export, "active"))
        self.export_all.clicked.connect(partial(self._export, "all"))
        self.export_statistics_active.clicked.connect(partial(self._export_statistics, "active"))
        self.export_statistics_all.clicked.connect(partial(self._export_statistics, "all"))

        #oufti events
        self.oufti_generate_all_midlines.clicked.connect(partial(self.generate_midlines, mode = "all"))
        self.oufti_generate_active_midlines.clicked.connect(partial(self.generate_midlines, mode="active"))
        self.viewer.bind_key(key="m", func=self.midline_edit_toggle, overwrite=True)
        self.oufti_edit_mode.clicked.connect(self.midline_edit_toggle)
        self.oufti_panzoom_mode.clicked.connect(self.midline_edit_toggle)
        self.oufti_centre_all_midlines.clicked.connect(partial(self.centre_oufti_midlines, mode = "all"))
        self.oufti_centre_active_midlines.clicked.connect(partial(self.centre_oufti_midlines, mode="active"))

        # upload tab events
        self.upload_all.clicked.connect(partial(self._uploadDatabase, mode="all"))
        self.upload_active.clicked.connect(partial(self._uploadDatabase, mode="active"))
        self.database_download.clicked.connect(self._downloadDatabase)
        self.create_database.clicked.connect(self._create_bacseg_database)
        self.load_database.clicked.connect(self._load_bacseg_database)
        self.upload_initial.currentTextChanged.connect(self._populateUSERMETA)

        self.update_metadata.clicked.connect(self.update_database_metadata)

        # viewer event that call updateFileName when the slider is modified
        self.contours = []
        self.viewer.dims.events.current_step.connect(self._sliderEvent)

        # self.segImage = self.viewer.add_image(np.zeros((1,100,100),dtype=np.uint16),name="Image")
        self.class_colours = {1: (255 / 255, 255 / 255, 255 / 255, 1),
                              2: (0 / 255, 255 / 255, 0 / 255, 1),
                              3: (0 / 255, 170 / 255, 255 / 255, 1),
                              4: (170 / 255, 0 / 255, 255 / 255, 1),
                              5: (255 / 255, 170 / 255, 0 / 255, 1),
                              6: (255 / 255, 0 / 255, 0 / 255, 1), }

        self.classLayer = self.viewer.add_labels(np.zeros((1, 100, 100), dtype=np.uint16), opacity=0.25, name="Classes",
                                                 color=self.class_colours, metadata={0: {"image_name": ""}},
                                                 visible=False)
        self.segLayer = self.viewer.add_labels(np.zeros((1, 100, 100), dtype=np.uint16), opacity=1,
                                               name="Segmentations", metadata={0: {"image_name": ""}})

        self.segLayer.contour = 1

        # keyboard events, only triggered when viewer is not empty (an image is loaded/active)
        self.viewer.bind_key(key="t", func=partial(self._modifyMode, "toggle"), overwrite=True)
        self.viewer.bind_key(key="a", func=partial(self._modifyMode, "add"), overwrite=True)
        self.viewer.bind_key(key="e", func=partial(self._modifyMode, "extend"), overwrite=True)
        self.viewer.bind_key(key="j", func=partial(self._modifyMode, "join"), overwrite=True)
        self.viewer.bind_key(key="s", func=partial(self._modifyMode, "split"), overwrite=True)
        self.viewer.bind_key(key="d", func=partial(self._modifyMode, "delete"), overwrite=True)
        self.viewer.bind_key(key="r", func=partial(self._modifyMode, "refine"), overwrite=True)

        self.viewer.bind_key(key="Control-1", func=partial(self._modifyMode, "single"), overwrite=True)
        self.viewer.bind_key(key="Control-2", func=partial(self._modifyMode, "dividing"), overwrite=True)
        self.viewer.bind_key(key="Control-3", func=partial(self._modifyMode, "divided"), overwrite=True)
        self.viewer.bind_key(key="Control-4", func=partial(self._modifyMode, "vertical"), overwrite=True)
        self.viewer.bind_key(key="Control-5", func=partial(self._modifyMode, "broken"), overwrite=True)
        self.viewer.bind_key(key="Control-6", func=partial(self._modifyMode, "edge"), overwrite=True)
        self.viewer.bind_key(key="F1", func=partial(self._modifyMode, "panzoom"), overwrite=True)
        self.viewer.bind_key(key="F2", func=partial(self._modifyMode, "segment"), overwrite=True)
        self.viewer.bind_key(key="F3", func=partial(self._modifyMode, "classify"), overwrite=True)
        # self.viewer.bind_key(key="Control", func=partial(self._modifyMode, "segment"), overwrite=True)
        self.viewer.bind_key(key="h", func=partial(self._viewerControls, "h"), overwrite=True)
        self.viewer.bind_key(key="i", func=partial(self._viewerControls, "i"), overwrite=True)
        self.viewer.bind_key(key="o", func=partial(self._viewerControls, "o"), overwrite=True)
        self.viewer.bind_key(key="x", func=partial(self._viewerControls, "x"), overwrite=True)
        self.viewer.bind_key(key="z", func=partial(self._viewerControls, "z"), overwrite=True)
        self.viewer.bind_key(key="c", func=partial(self._viewerControls, "c"), overwrite=True)
        self.viewer.bind_key(key="Right", func=partial(self._imageControls, "Right"), overwrite=True)
        self.viewer.bind_key(key="Left", func=partial(self._imageControls, "Left"), overwrite=True)
        self.viewer.bind_key(key="u", func=partial(self._imageControls, "Upload"), overwrite=True)
        self.viewer.bind_key(key="Control-d", func=partial(self._deleteallmasks, mode="active"), overwrite=True)
        self.viewer.bind_key(key="Control-Shift-d", func=partial(self._deleteallmasks, mode="all"), overwrite=True)
        self.viewer.bind_key(key="Control-i", func=partial(self._delete_active_image, mode="active"), overwrite=True)
        self.viewer.bind_key(key="Control-Shift-i", func=partial(self._delete_active_image, mode="other"), overwrite=True)

        self.viewer.bind_key(key="Control-l", func=self._downloadDatabase(),overwrite=True)
        self.viewer.bind_key(key="Control-u", func=partial(self._uploadDatabase, mode="active"),overwrite=True)
        self.viewer.bind_key(key="Control-Shift-u", func=partial(self._uploadDatabase, mode="all"), overwrite=True)

        self.viewer.bind_key(key="Control-Left", func=partial(self._manual_align_channels, "left", mode="active"), overwrite=True)
        self.viewer.bind_key(key="Control-Right", func=partial(self._manual_align_channels, "right", mode="active"), overwrite=True)
        self.viewer.bind_key(key="Control-Up", func=partial(self._manual_align_channels, "up", mode="active"), overwrite=True)
        self.viewer.bind_key(key="Control-Down", func=partial(self._manual_align_channels, "down", mode="active"), overwrite=True)

        self.viewer.bind_key(key="Alt-Left", func=partial(self._manual_align_channels, "left", mode="all"), overwrite=True)
        self.viewer.bind_key(key="Alt-Right", func=partial(self._manual_align_channels, "right", mode="all"), overwrite=True)
        self.viewer.bind_key(key="Alt-Up", func=partial(self._manual_align_channels, "up", mode="all"), overwrite=True)
        self.viewer.bind_key(key="Alt-Down", func=partial(self._manual_align_channels, "down", mode="all"), overwrite=True)

        self.import_filemode.currentIndexChanged.connect(self.update_import_limit)
        self.update_import_limit()

        # mouse events
        self.segLayer.mouse_drag_callbacks.append(self._segmentationEvents)
        self.segLayer.mouse_double_click_callbacks.append(self._doubeClickEvents)

        # viewer events
        self.viewer.layers.events.inserted.connect(self._manualImport)

        self.threadpool = QThreadPool()
        # self.load_dev_data()

    def overwrite_channel_info(self):

        all_layers = [layer.name for layer in self.viewer.layers]
        selected_layers = [layer.name for layer in self.viewer.layers.selection]

        if len(selected_layers) == 1:

            selected_layer = selected_layers[0]
            all_layers.pop(all_layers.index(selected_layer))

            if selected_layer not in ["Segmentations", "Classes","center_lines"]:

                metadata = self.viewer.layers[selected_layer].metadata.copy()

                label_modality = self.label_modality.currentText()
                label_light_source = self.label_light_source.currentText()
                label_stain = self.label_stain.currentText()
                label_stain_target = self.label_stain_target.currentText()

                if label_stain != "":
                    channel = label_stain
                else:
                    channel = label_modality

                if channel in ["",None]:
                    channel = selected_layer

                self.viewer.layers[selected_layer].name = channel

                for i in range(len(metadata)):

                    metadata[i]["channel"] = channel
                    metadata[i]["modality"] = label_modality
                    metadata[i]["light_source"] = label_light_source
                    metadata[i]["stain"] = label_stain
                    metadata[i]["stain_target"] = label_stain_target

                self.viewer.layers[channel].metadata = metadata

                self._updateFileName()
                self._updateSegmentationCombo()
                self._updateSegChannels()

    def _export_statistics(self, mode='active'):

        multithreaded = self.export_statistics_multithreaded.isChecked()

        if self.unfolded == True:
            self.fold_images()

        pixel_size = float(self.export_statistics_pixelsize.text())

        colicoords_channel = self.export_colicoords_mode.currentText()
        colicoords_channel = colicoords_channel.replace("Mask + ", "")

        if pixel_size <= 0:
            pixel_size = 1

        desktop = os.path.expanduser("~/Desktop")

        path = QFileDialog.getExistingDirectory(self, "Select Directory", desktop)

        colicoords_dir = os.path.join(tempfile.gettempdir(), "colicoords")

        if os.path.isdir(colicoords_dir) != True:
            os.mkdir(colicoords_dir)
        else:
            shutil.rmtree(colicoords_dir)
            os.mkdir(colicoords_dir)

        if os.path.isdir(path):

            path = os.path.abspath(path)

            from napari_bacseg._utils_statistics import get_cell_statistics, process_cell_statistics

            self.get_cell_statistics = partial(get_cell_statistics, self)
            self.process_cell_statistics = partial(process_cell_statistics, self)

            worker = Worker(self.get_cell_statistics, mode=mode, pixel_size=pixel_size, colicoords_dir=colicoords_dir)
            worker.signals.progress.connect(partial(self._Progresbar, progressbar="export"))
            worker.signals.result.connect(partial(self.process_cell_statistics, path=path))
            self.threadpool.start(worker)
            cell_data = worker.result()

            if self.export_colicoords_mode.currentIndex() != 0:
                from napari_bacseg._utils_colicoords import run_colicoords

                self.run_colicoords = partial(run_colicoords, self)

                worker = Worker(self.run_colicoords,
                                cell_data=cell_data,
                                colicoords_channel=colicoords_channel,
                                pixel_size=pixel_size,
                                statistics=True,
                                multithreaded=multithreaded)

                worker.signals.progress.connect(partial(self._Progresbar, progressbar="export"))
                worker.signals.result.connect(partial(self.process_cell_statistics, path=path))
                self.threadpool.start(worker)

    def update_import_limit(self):

        if self.import_filemode.currentIndex() == 0:

            self.import_limit.setEnabled(False)
            self.import_limit.setCurrentIndex(6)
            self.import_limit.hide()
            self.import_limit_label.hide()
        else:
            self.import_limit.setEnabled(True)
            self.import_limit.setCurrentIndex(0)
            self.import_limit.show()
            self.import_limit_label.show()



    def _sort_cells(self, order):

        if self.unfolded == True:
            self.fold_images()

        try:

            current_fov = self.viewer.dims.current_step[0]

            meta = self.segLayer.metadata[current_fov]

            self._compute_simple_cell_stats()

            find_criterion = self.find_criterion.currentText()
            find_mode = self.find_mode.currentText()

            cell_centre = meta["simple_cell_stats"]['cell_centre']
            cell_zoom = meta["simple_cell_stats"]['cell_zoom']

            if find_criterion == "Cell Area":
                criterion = meta["simple_cell_stats"]["cell_area"]
            if find_criterion == "Cell Solidity":
                criterion = meta["simple_cell_stats"]["cell_solidity"]
            if find_criterion == "Cell Aspect Ratio":
                criterion = meta["simple_cell_stats"]["cell_aspect_ratio"]

            if find_mode == "Ascending":
                criterion, cell_centre, cell_zoom= zip(*sorted(zip(criterion, cell_centre, cell_zoom), key=lambda x: x[0]))
            else:
                criterion, cell_centre, cell_zoom = zip(*sorted(zip(criterion, cell_centre, cell_zoom), key=lambda x: x[0], reverse=True))

            current_position = tuple(np.array(self.viewer.camera.center).round())

            if current_position not in cell_centre:

                self.viewer.camera.center = cell_centre[0]
                self.viewer.camera.zoom = cell_zoom[0]

            else:

                current_index = cell_centre.index(current_position)

                if order == 'next':

                    new_index = current_index + 1

                if order == 'previous':

                    new_index = current_index - 1

                new_index = max(current_fov, min(new_index, len(cell_centre) - 1))

                self.viewer.camera.center = cell_centre[new_index]
                self.viewer.camera.zoom = cell_zoom[new_index]

        except:
            pass


    def _manual_align_channels(self, key, viewer=None, mode ='active'):

        if self.unfolded == True:
            self.fold_images()

        from scipy.ndimage import shift
        current_fov = self.viewer.dims.current_step[0]
        active_layer = self.viewer.layers.selection.active

        if key == 'up':
            shift_vector = [-1.0, 0.0]
        elif key == 'down':
            shift_vector = [1.0, 0.0]
        elif key == 'left':
            shift_vector = [0.0, -1.0]
        elif key == 'right':
            shift_vector = [0.0, 1.0]
        else:
            shift_vector = [0.0, 0.0]

        shift_image = False
        if active_layer != None:
            if active_layer.name not in ["Segmentations","Classes"]:
                shift_image = True

        if shift_image is True:

            if mode == 'active':

                image_stack = active_layer.data.copy()
                image = image_stack[current_fov, :, :]
                image = shift(image, shift=shift_vector)
                image_stack[current_fov, :, :] = np.expand_dims(image,0)

                active_layer.data = image_stack

            else:

                image_stack = active_layer.data.copy()

                for i in range(len(image_stack)):

                    image = image_stack[i, :, :]
                    image = shift(image, shift=shift_vector)
                    image_stack[i, :, :] = np.expand_dims(image, 0)

                active_layer.data = image_stack
        else:

            mask_stack = self.segLayer.data.copy()
            label_stack = self.classLayer.data.copy()

            mask = mask_stack[current_fov, :, :]
            label = label_stack[current_fov, :, :]

            mask = shift(mask, shift=shift_vector)
            label = shift(label, shift=shift_vector)

            mask_stack[current_fov, :, :] = np.expand_dims(mask, 0)
            label_stack[current_fov, :, :] = np.expand_dims(label, 0)

            self.segLayer.data = mask_stack
            self.classLayer.data = label_stack







    def _refine_bacseg(self):

        if self.unfolded == True:
            self.fold_images()

        pixel_size = float(self.export_statistics_pixelsize.text())

        if pixel_size <= 0:
            pixel_size = 1

        current_fov = self.viewer.dims.current_step[0]

        channel = self.refine_channel.currentText()
        colicoords_channel = channel.replace("Mask + ", "")

        mask_stack = self.segLayer.data
        mask = mask_stack[current_fov, :, :].copy()

        from napari_bacseg._utils_statistics import get_cell_statistics
        from napari_bacseg._utils_colicoords import run_colicoords, process_colicoords

        self.get_cell_statistics = partial(get_cell_statistics,self)
        self.run_colicoords = partial(run_colicoords,self)
        self.process_colicoords = partial(process_colicoords,self)

        colicoords_dir = os.path.join(tempfile.gettempdir(), "colicoords")

        worker = Worker(self.get_cell_statistics,
                        mode='active',
                        pixel_size=pixel_size,
                        colicoords_dir=colicoords_dir)

        self.threadpool.start(worker)
        cell_data = worker.result()

        worker = Worker(self.run_colicoords,
                        cell_data=cell_data,
                        colicoords_channel=colicoords_channel,
                        pixel_size=pixel_size,
                        multithreaded=True)

        worker.signals.progress.connect(partial(self._Progresbar, progressbar="modify"))
        worker.signals.result.connect(self.process_colicoords)
        self.threadpool.start(worker)

    def _uploadDatabase(self, viewer = None, mode=""):

        try:

            if self.database_path != "" and os.path.exists(self.database_path) == True:

                if self.unfolded == True:
                    self.fold_images()

                from napari_bacseg._utils_database_IO import _upload_bacseg_database
                self._upload_bacseg_database = partial(_upload_bacseg_database, self)

                worker = Worker(self._upload_bacseg_database, mode=mode)
                worker.signals.progress.connect(partial(self._Progresbar, progressbar="database"))
                self.threadpool.start(worker)

        except:
            pass

    def _downloadDatabase(self, viewer=None):

        try:

            if self.database_path != "" and os.path.exists(self.database_path) == True:

                if self.unfolded == True:
                    self.fold_images()

                from napari_bacseg._utils_database_IO import read_bacseg_images, get_filtered_database_metadata

                self.get_filtered_database_metadata = partial(get_filtered_database_metadata,self)
                self.read_bacseg_images = partial(read_bacseg_images, self)

                self.active_import_mode = "BacSeg"

                measurements, file_paths, channels = self.get_filtered_database_metadata()

                if len(file_paths) == 0:

                    show_info("no matching database files found")

                else:

                    worker = Worker(self.read_bacseg_images, measurements=measurements, channels=channels)
                    worker.signals.result.connect(self._process_import)
                    worker.signals.progress.connect(partial(self._Progresbar, progressbar="database"))
                    self.threadpool.start(worker)

        except:
            pass

    def _updateSegChannels(self):

        layer_names = [layer.name for layer in self.viewer.layers if layer.name not in ["Segmentations", "Classes","center_lines"]]

        segChannel = self.cellpose_segchannel.currentText()

        self.export_channel.setCurrentText(segChannel)

    def _Progresbar(self, progress, progressbar):

        if progressbar == "import":
            self.import_progressbar.setValue(progress)
        if progressbar == "export":
            self.export_progressbar.setValue(progress)
        if progressbar == 'cellpose':
            self.cellpose_progressbar.setValue(progress)
        if progressbar == "database":
            self.upload_progressbar.setValue(progress)
        if progressbar == 'modify':
            self.modify_progressbar.setValue(progress)

        if progress == 100:
            time.sleep(1)
            self.import_progressbar.setValue(0)
            self.export_progressbar.setValue(0)
            self.cellpose_progressbar.setValue(0)
            self.upload_progressbar.setValue(0)
            self.modify_progressbar.setValue(0)

    def _importDialog(self):

        if self.unfolded == True:
            self.fold_images()

        import_mode = self.import_mode.currentText()
        import_filemode = self.import_filemode.currentText()

        file_extension = "*.tif"

        if import_mode == "Images":
            file_extension = "*.tif *.png *.jpeg *.fits"
        if import_mode == "Cellpose (.npy) Segmentation(s)":
            file_extension = "*.npy"
        if import_mode == "Oufti (.mat) Segmentation(s)":
            file_extension = "*.mat"
        if import_mode == "JSON (.txt) Segmentation(s)":
            file_extension = "*.txt"

        desktop = os.path.expanduser("~/Desktop")

        if import_filemode == "Import File(s)":
            paths, _ = QFileDialog.getOpenFileNames(self, "Open Files", desktop, f"Files ({file_extension})")

        if import_filemode == "Import Directory":
            path = QFileDialog.getExistingDirectory(self, "Select Directory", desktop)

            paths = [path]

        if "" in paths or paths == []:

            show_info("No file/folder selected")

        else:

            if import_mode == "Images":

                self.import_images = partial(napari_bacseg._utils.import_images, self)

                worker = Worker(self.import_images, file_paths=paths)
                worker.signals.result.connect(self._process_import)
                worker.signals.progress.connect(partial(self._Progresbar, progressbar="import"))
                self.threadpool.start(worker)

            if import_mode == "NanoImager Data":

                self.read_nim_directory = partial(napari_bacseg._utils.read_nim_directory, self)
                self.read_nim_images = partial(napari_bacseg._utils.read_nim_images, self)

                measurements, file_paths, channels = self.read_nim_directory(paths)

                worker = Worker(self.read_nim_images, measurements=measurements, channels=channels)
                worker.signals.result.connect(self._process_import)
                worker.signals.progress.connect(partial(self._Progresbar, progressbar="import"))
                self.threadpool.start(worker)

            if import_mode == "Mask (.tif) Segmentation(s)":

                self.import_masks = partial(napari_bacseg._utils.import_masks, self)
                self.import_masks(paths, file_extension = ".tif")
                self._autoClassify()

            if import_mode == "Cellpose (.npy) Segmentation(s)":

                self.import_masks = partial(napari_bacseg._utils.import_masks, self)
                self.import_masks(paths, file_extension=".npy")
                self._autoClassify()

            if import_mode == "Oufti (.mat) Segmentation(s)":

                self.import_masks = partial(napari_bacseg._utils.import_masks, self)
                self.import_masks(paths, file_extension=".mat")
                self._autoClassify()

            if import_mode == "JSON (.txt) Segmentation(s)":

                self.import_masks = partial(napari_bacseg._utils.import_masks, self)
                self.import_masks(paths, file_extension=".txt")
                self._autoClassify()

            if import_mode == "ImageJ files(s)":

                self.import_imagej = partial(napari_bacseg._utils.import_imagej, self)

                worker = Worker(self.import_imagej, paths=paths)
                worker.signals.result.connect(self._process_import)
                worker.signals.progress.connect(partial(self._Progresbar, progressbar="import"))
                self.threadpool.start(worker)

            if import_mode == "ScanR Data":

                from napari_bacseg._utils import read_scanr_directory, read_scanr_images

                self.read_scanr_images = partial(read_scanr_images, self)

                measurements, file_paths, channels = read_scanr_directory(self, paths)

                worker = Worker(self.read_scanr_images, measurements=measurements, channels=channels)
                worker.signals.result.connect(self._process_import)
                worker.signals.progress.connect(partial(self._Progresbar, progressbar="import"))
                self.threadpool.start(worker)

    def _export(self, mode):

        # if self.unfolded == True:
        #     self.fold_images()

        execute_export = True

        if self.export_location.currentIndex() == 1:

            desktop = os.path.expanduser("~/Desktop")
            self.export_directory = QFileDialog.getExistingDirectory(self, "Select Directory", desktop)

            if self.export_directory == "":

                execute_export = False

        if execute_export == True:

            self.export_files = partial(napari_bacseg._utils.export_files, self)

            worker = Worker(self.export_files, mode=mode)
            worker.signals.progress.connect(partial(self._Progresbar, progressbar="export"))
            self.threadpool.start(worker)

    def _trainCellpose(self):

        if self.unfolded == True:
            self.fold_images()

        from napari_bacseg._utils_cellpose import train_cellpose_model
        self.train_cellpose_model = partial(train_cellpose_model, self)

        worker = Worker(self.train_cellpose_model)
        worker.signals.progress.connect(partial(self._Progresbar, progressbar="cellpose_train"))
        self.threadpool.start(worker)


    def _segmentActive(self):

        if self.unfolded == True:
            self.fold_images()

        from napari_bacseg._utils_cellpose import _run_cellpose, _process_cellpose
        self._run_cellpose = partial(_run_cellpose, self)
        self._process_cellpose = partial(_process_cellpose, self)

        current_fov = self.viewer.dims.current_step[0]
        chanel = self.cellpose_segchannel.currentText()

        images = self.viewer.layers[chanel].data

        image = [images[current_fov, :, :]]

        worker = Worker(self._run_cellpose, images=image)
        worker.signals.result.connect(self._process_cellpose)
        worker.signals.progress.connect(partial(self._Progresbar, progressbar="cellpose"))
        self.threadpool.start(worker)

    def _segmentAll(self):

        if self.unfolded == True:
            self.fold_images()

        from napari_bacseg._utils_cellpose import _run_cellpose, _process_cellpose
        self._run_cellpose = partial(_run_cellpose, self)
        self._process_cellpose = partial(_process_cellpose, self)

        channel = self.cellpose_segchannel.currentText()

        images = self.viewer.layers[channel].data

        images = unstack_images(images)

        worker = Worker(self._run_cellpose, images=images)
        worker.signals.result.connect(self._process_cellpose)
        worker.signals.progress.connect(partial(self._Progresbar, progressbar="cellpose"))
        self.threadpool.start(worker)

    def _updateSliderLabel(self, slider_name, label_name):

        self.slider = self.findChild(QSlider, slider_name)
        self.label = self.findChild(QLabel, label_name)

        slider_value = self.slider.value()

        if slider_name == "cellpose_flowthresh" or slider_name == "cellpose_maskthresh":
            self.label.setText(str(slider_value / 100))
        else:
            self.label.setText(str(slider_value))

    def _updateSegmentationCombo(self):

        layer_names = [layer.name for layer in self.viewer.layers if layer.name not in ["Segmentations", "Classes","center_lines"]]

        self.cellpose_segchannel.clear()
        self.cellpose_segchannel.addItems(layer_names)

        self.cellpose_trainchannel.clear()
        self.cellpose_trainchannel.addItems(layer_names)

        self.cellpose_trainchannel.clear()
        self.cellpose_trainchannel.addItems(layer_names)

        self.export_channel.clear()
        export_layers = layer_names
        export_layers.extend(["All Channels (Stack)","First Three Channels (RGB)"])
        self.export_channel.addItems(export_layers)

        self.refine_channel.clear()
        refine_layers = ["Mask + " + layer for layer in layer_names]
        self.refine_channel.addItems(['Mask'] + refine_layers)

        self.export_colicoords_mode.clear()
        refine_layers = ["Mask + " + layer for layer in layer_names]
        self.export_colicoords_mode.addItems(['None (OpenCV Stats)', 'Mask'] + refine_layers)

        if "532" in layer_names:
            index532 = layer_names.index("532")
            self.cellpose_segchannel.setCurrentIndex(index532)

    def _sliderEvent(self, current_step):

        self._updateFileName()
        self._autoContrast()
        self._update_active_midlines()

    def _autoContrast(self):

        try:
            if self.autocontrast.isChecked():

                layer_names = [layer.name for layer in self.viewer.layers if
                               layer.name not in ["Segmentations", "Classes","center_lines"]]

                if len(layer_names) != 0:

                    active_layer = layer_names[-1]

                    image_dims = tuple(list(self.viewer.dims.current_step[:-2]) + [...])

                    image = self.viewer.layers[str(active_layer)].data[image_dims].copy()

                    crop = self.viewer.layers[str(active_layer)].corner_pixels[:, -2:]

                    [[y1, x1], [y2, x2]] = crop

                    image_crop = image[y1:y2, x1:x2]

                    contrast_limit = [np.min(image_crop), np.max(image_crop)]

                    if contrast_limit[1] > contrast_limit[0]:
                        self.viewer.layers[str(active_layer)].contrast_limits = contrast_limit

        except:
            pass

    def _updateFileName(self):

        try:

            current_fov = self.viewer.dims.current_step[0]
            active_layer = self.viewer.layers.selection.active

            metadata = self.viewer.layers[str(active_layer)].metadata[current_fov]

            file_name = metadata["image_name"]
            channel = metadata["channel"]


            if "stain" in metadata.keys():
                stain = metadata["stain"]
            else:
                stain = None

            if "stain_target" in metadata.keys():
                stain_target = metadata["stain_target"]
            else:
                stain_target = None

            if "modality" in metadata.keys():
                modality = metadata["modality"]
            else:
                modality = None

            if "light_source" in metadata.keys():
                light_source = metadata["light_source"]
            else:
                light_source = None


            viewer_text = f"File Name: {file_name}\nModality: {modality}\nLight Source: {light_source}\nStain: {stain}\nStain Target: {stain_target}"

            self.viewer.text_overlay.visible = True

            self.viewer.text_overlay.text = viewer_text

        except:
            pass


    def _process_import(self, imported_data, rearrange=True):

        layer_names = [layer.name for layer in self.viewer.layers if layer.name not in ["Segmentations", "Classes","center_lines"]]

        if self.clear_previous.isChecked() == True:
            # removes all layers (except segmentation layer)
            for layer_name in layer_names:
                self.viewer.layers.remove(self.viewer.layers[layer_name])
            # reset segmentation and class layers
            self.segLayer.data = np.zeros((1, 100, 100), dtype=np.uint16)
            self.classLayer.data = np.zeros((1, 100, 100), dtype=np.uint16)

        imported_images = imported_data["imported_images"]

        for layer_name, layer_data in imported_images.items():

            images = layer_data['images']
            masks = layer_data['masks']
            classes = layer_data['classes']
            metadata = layer_data['metadata']

            from napari_bacseg._utils import stack_images
            new_image_stack, new_metadata = stack_images(images, metadata)
            new_mask_stack, new_metadata = stack_images(masks, metadata)
            new_class_stack, new_metadata = stack_images(classes, metadata)

            if len(new_mask_stack) == 0:
                new_mask_stack = np.zeros(new_image_stack.shape, dtype=np.uint16)

            if len(new_class_stack) == 0:
                new_class_stack = np.zeros(new_image_stack.shape, dtype=np.uint16)

            colormap = 'gray'

            if layer_name == "405":
                colormap = "green"
            if layer_name == "532":
                colormap = "red"
            if layer_name == "Cy3":
                colormap = "red"
            if layer_name == "DAPI":
                colormap = "green"


            if self.clear_previous.isChecked() == False and layer_name in layer_names:

                current_image_stack = self.viewer.layers[layer_name].data
                current_metadata = self.viewer.layers[layer_name].metadata
                current_mask_stack = self.segLayer.data
                current_class_stack = self.classLayer.data

                if len(current_image_stack) == 0:

                    self.imageLayer = self.viewer.add_image(new_image_stack, name=layer_name, colormap=colormap,
                                                            gamma=0.8, metadata=new_metadata)
                    self.segLayer.data = new_mask_stack
                    self.classLayer.data = new_class_stack
                    self.segLayer.metadata = new_metadata

                else:

                    from napari_bacseg._utils import append_image_stacks
                    appended_image_stack, appended_metadata = append_image_stacks(current_metadata, new_metadata,
                                                                                  current_image_stack, new_image_stack)

                    appended_mask_stack, appended_metadata = append_image_stacks(current_metadata, new_metadata,
                                                                                 current_mask_stack, new_mask_stack)

                    appended_class_stack, appended_metadata = append_image_stacks(current_metadata, new_metadata,
                                                                                  current_class_stack, new_class_stack)

                    self.viewer.layers.remove(self.viewer.layers[layer_name])
                    self.viewer.add_image(appended_image_stack, name=layer_name, colormap=colormap, gamma=0.8,
                                          metadata=appended_metadata)
                    self.segLayer.data = appended_mask_stack
                    self.classLayer.data = appended_class_stack
                    self.segLayer.metadata = appended_metadata


            else:

                self.viewer.add_image(new_image_stack, name=layer_name, colormap=colormap, gamma=0.8,
                                      metadata=new_metadata)
                self.segLayer.data = new_mask_stack
                self.classLayer.data = new_class_stack
                self.segLayer.metadata = new_metadata

        layer_names = [layer.name for layer in self.viewer.layers if layer.name not in ["Segmentations", "Classes","center_lines"]]

        # ensures segmentation and classes is in correct order in the viewer
        for layer in layer_names:
            self.viewer.layers[layer].selected = False
            layer_index = self.viewer.layers.index(layer)
            self.viewer.layers.move(layer_index, 0)

        if "532" in layer_names and rearrange == True:
            layer_name = "532"
            num_layers = len(self.viewer.layers)
            layer_ref = self.viewer.layers[layer_name]
            layer_index = self.viewer.layers.index(layer_name)
            self.viewer.layers.selection.select_only(layer_ref)
            self.viewer.layers.move(layer_index, num_layers - 2)

        if "Cy3" in layer_names and rearrange == True:
            layer_name = "Cy3"
            num_layers = len(self.viewer.layers)
            layer_ref = self.viewer.layers[layer_name]
            layer_index = self.viewer.layers.index(layer_name)
            self.viewer.layers.selection.select_only(layer_ref)
            self.viewer.layers.move(layer_index, num_layers - 2)

        # sets labels such that only label contours are shown
        self.segLayer.contour = 1
        self.segLayer.opacity = 1

        self._updateFileName()
        self._updateSegmentationCombo()
        self._updateSegChannels()
        self.import_progressbar.reset()
        self.viewer.reset_view()
        self._autoClassify()
        align_image_channels(self)
        self._autoContrast()

    def _autoClassify(self, reset=False):

        mask_stack = self.segLayer.data.copy()
        label_stack = self.classLayer.data.copy()

        for i in range(len(mask_stack)):

            mask = mask_stack[i, :, :]
            label = label_stack[i, :, :]

            label_ids = np.unique(label)
            mask_ids = np.unique(mask)

            if len(label_ids) == 1 or reset == True:

                label = np.zeros(label.shape, dtype=np.uint16)

                for mask_id in mask_ids:

                    if mask_id != 0:

                        cnt_mask = np.zeros(label.shape, dtype=np.uint8)
                        cnt_mask[mask == mask_id] = 255

                        cnt, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                        x, y, w, h = cv2.boundingRect(cnt[0])
                        y1, y2, x1, x2 = y, (y + h), x, (x + w)

                        # appends contour to list if the bounding coordinates are along the edge of the image
                        if y1 > 0 and y2 < cnt_mask.shape[0] and x1 > 0 and x2 < cnt_mask.shape[1]:

                            label[mask == mask_id] = 1

                        else:

                            label[mask == mask_id] = 6

            label_stack[i, :, :] = label

        self.classLayer.data = label_stack

