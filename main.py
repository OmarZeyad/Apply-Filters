import os
import sys
import cv2

from filters import filters
from gui     import Ui_MainWindow

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore    as qtc
from PyQt5 import QtGui     as qtg


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setupUi(self)

        self.default_brightness, self.default_contrast = 0, 1.0
        self.IMG_LBL_WIDTH, self.IMG_LBL_HEIGHT = 310, 220
        
        self.setup_slots()
        
        self.show()

    def setup_slots(self):
        self.load_img_btn.clicked.connect(self.load_img)
        self.default_conv_rbtn.clicked.connect(self.default_conv)
        self.gray_conv_rbtn.clicked.connect(self.gray_conv)
        self.sp_noise_rbtn.clicked.connect(self.sp_noise)
        self.gaussian_noise_rbtn.clicked.connect(self.gaussian_noise)
        self.poisson_noise_rbtn.clicked.connect(self.poisson_noise)
        self.brightness_adj_btn.clicked.connect(self.brightness_adj)
        self.contrast_adj_btn.clicked.connect(self.contrast_adj)
        self.histogram_btn.clicked.connect(self.histogram)
        self.histogram_equalizer_btn.clicked.connect(self.histogram_equalizer)
        self.lpf_btn.clicked.connect(self.lpf)
        self.hpf_btn.clicked.connect(self.hpf)
        self.medf_btn.clicked.connect(self.medf)
        self.avgf_btn.clicked.connect(self.avgf)
        self.laplacian_edf_rbtn.clicked.connect(self.laplacian_edf)
        self.gaussian_edf_rbtn.clicked.connect(self.gaussian_edf)
        self.vertsobel_edf_rbtn.clicked.connect(self.vertsobel_edf)
        self.horizsobel_edf_rbtn.clicked.connect(self.horizsobel_edf)
        self.vertprewitt_edf_rbtn.clicked.connect(self.vertprewitt_edf)
        self.horizprewitt_edf_rbtn.clicked.connect(self.horizprewitt_edf)
        self.prewitt_edf_rbtn.clicked.connect(self.prewitt_edf)
        self.log_edf_rbtn.clicked.connect(self.log_edf)
        self.canny_edf_rbtn.clicked.connect(self.canny_edf)
        self.zerocross_edf_rbtn.clicked.connect(self.zerocross_edf)
        self.skeleton_edf_rbtn.clicked.connect(self.skeleton_edf)
        self.sobel_edf_rbtn.clicked.connect(self.sobel_edf)
        self.linedetect_btn.clicked.connect(self.linedetect)
        self.circledetect_btn.clicked.connect(self.circledetect)
        self.dilation_morph_btn.clicked.connect(self.dilation_morph)
        self.erosion_morph_btn.clicked.connect(self.erosion_morph)
        self.close_morph_btn.clicked.connect(self.close_morph)
        self.open_morph_btn.clicked.connect(self.open_morph)
        self.save_img_btn.clicked.connect(self.save_img)
        self.exit_prog_btn.clicked.connect(self.exit_prog)

    def display_result(self, cvImg):
        def convert_cv2img_to_qimg():
            height, width, channel = cvImg.shape
            bytesPerLine = 3 * width
            self.qImg = qtg.QImage(cvImg.data, width, height, bytesPerLine, qtg.QImage.Format_RGB888).rgbSwapped()
            self.res_img_lbl.setPixmap(qtg.QPixmap.fromImage(self.qImg).scaled(self.IMG_LBL_WIDTH, self.IMG_LBL_HEIGHT))

        if cvImg.ndim == 2:
            cvImg = cv2.cvtColor(cvImg, cv2.COLOR_GRAY2BGR)
            convert_cv2img_to_qimg()
        elif cvImg.ndim == 3:
            convert_cv2img_to_qimg()

    def load_img(self):
        img_path, _ = qtw.QFileDialog.getOpenFileName(self, 'Open file', os.path.dirname(__file__), "JPEG(*.jpg *.jpeg);;PNG(*.png);;All Files(*.*)")
        self.orig_img_lbl.setPixmap(qtg.QPixmap(img_path).scaled(self.IMG_LBL_WIDTH, self.IMG_LBL_HEIGHT))
        self.filters = filters(cv2.imread(img_path))

    def default_conv(self):
        self.display_result(self.filters.in_image)
    
    def gray_conv(self):
        self.display_result(self.filters.gray)
    
    def sp_noise(self):
        self.display_result(self.filters.add_noise("s&p"))
    
    def gaussian_noise(self):
        self.display_result(self.filters.add_noise("gauss"))
    
    def poisson_noise(self):
        self.display_result(self.filters.add_noise("poisson"))
    
    def brightness_adj(self):
        self.default_brightness += 50
        self.display_result(self.filters.bc_adj(beta=self.default_brightness))
    
    def contrast_adj(self):
        self.default_contrast += 0.2
        self.display_result(self.filters.bc_adj(alpha=self.default_contrast))
    
    def histogram(self):
        cvImg = self.filters.histogram()
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        self.qImg = qtg.QImage(cvImg.data, width, height, bytesPerLine, qtg.QImage.Format_RGB888).rgbSwapped()
        self.res_img_lbl.setPixmap(qtg.QPixmap.fromImage(self.qImg).scaled(self.IMG_LBL_WIDTH, self.IMG_LBL_HEIGHT))
        #self.display_result(self.filters.show_histogram())
    
    def histogram_equalizer(self):
        self.display_result(self.filters.hist_equal())
        
    def lpf(self):
        self.display_result(self.filters.low_pass_filter())
    
    def hpf(self):
        self.display_result(self.filters.high_pass_filter())
    
    def medf(self):
        self.display_result(self.filters.median())
    
    def avgf(self):
        self.display_result(self.filters.avg())

    def laplacian_edf(self):
        self.display_result(self.filters.laplace())

    def gaussian_edf(self):
        self.display_result(self.filters.gauss())
    
    def log_edf(self):
        self.display_result(self.filters.log())

    def vertsobel_edf(self):
        self.display_result(self.filters.sobel_v())

    def horizsobel_edf(self):
        self.display_result(self.filters.sobel_h())

    def sobel_edf(self):
        self.display_result(self.filters.sobel())

    def vertprewitt_edf(self):
        self.display_result(self.filters.prewitt_v())

    def horizprewitt_edf(self):
        self.display_result(self.filters.prewitt_h())

    def prewitt_edf(self):
        self.display_result(self.filters.prewitt())

    def canny_edf(self):
        self.display_result(self.filters.canny())

    def zerocross_edf(self):
        self.display_result(self.filters.zero_crossing())

    def skeleton_edf(self):
        self.display_result(self.filters.skeleton())

    def linedetect(self):
        self.display_result(self.filters.line_detect())
    
    def circledetect(self):
        self.display_result(self.filters.circle_detect())
    
    def dilation_morph(self):
        self.display_result(self.filters.dilatation())
    
    def erosion_morph(self):
        self.display_result(self.filters.erosion())
    
    def close_morph(self):
        self.display_result(self.filters.closing())
    
    def open_morph(self):
        self.display_result(self.filters.opening())

    def save_img(self):
        filePath, _ = qtw.QFileDialog.getSaveFileName(self, "Save Image", os.path.dirname(__file__), "JPEG(*.jpg *.jpeg);;PNG(*.png);;All Files(*.*)")
        self.qImg.save(filePath)

    def exit_prog(self):
        self.close()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.move(50, 50)
    sys.exit(app.exec_())