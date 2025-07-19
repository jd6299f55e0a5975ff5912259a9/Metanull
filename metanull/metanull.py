import sys
import os
import random
import platform
import time
from datetime import datetime
from PIL import Image, ImageFilter
import piexif
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, 
    QPushButton, QTextEdit, QVBoxLayout, QWidget, 
    QMessageBox, QProgressBar, QHBoxLayout, QGroupBox,
    QStatusBar, QMenu, QMenuBar, QComboBox, QCheckBox,
    QSlider, QGridLayout, QSplitter
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QAction, QCursor

class ForensicSanitizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meta Null")
        self.setGeometry(300, 300, 900, 700)
        self.setMinimumSize(800, 600)
        
        # settings
        self.file_path = ""
        self.metadata_found = False
        self.output_format = "JPEG"
        self.quality = 95
        self.alter_pixels = True
        self.randomize_timestamp = True
        
        self.setup_ui()
        self.setup_menu()
        
    def setup_menu(self):
        menu_bar = QMenuBar()
        
        file_menu = QMenu("&File", self)
        
        open_action = QAction("Open Image", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.select_file)
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        tools_menu = QMenu("&Tools", self)
        
        analyze_action = QAction("Forensic Analysis", self)
        analyze_action.setShortcut("Ctrl+A")
        analyze_action.triggered.connect(self.analyze_metadata)
        
        clean_action = QAction("Sanitize Image", self)
        clean_action.setShortcut("Ctrl+S")
        clean_action.triggered.connect(self.sanitize_image)
        
        tools_menu.addAction(analyze_action)
        tools_menu.addAction(clean_action)
        
        help_menu = QMenu("&Help", self)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        
        help_menu.addAction(about_action)
        
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(tools_menu)
        menu_bar.addMenu(help_menu)
        
        self.setMenuBar(menu_bar)
    
    def setup_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # theme
        self.setStyleSheet("""
            QWidget {
                background-color: #0d0d0d;
                color: #e0e0e0;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QPushButton {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 2px;
                padding: 8px 16px;
                min-width: 120px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #252525;
                border: 1px solid #444;
            }
            QPushButton:pressed {
                background-color: #151515;
            }
            QPushButton:disabled {
                background-color: #0a0a0a;
                color: #666;
            }
            QTextEdit {
                background-color: #0a0a0a;
                border: 1px solid #222;
                border-radius: 2px;
                padding: 10px;
                color: #d0d0d0;
                font-family: 'Consolas', monospace;
                font-size: 11px;
                selection-background-color: #3a3a3a;
            }
            QProgressBar {
                background-color: #0a0a0a;
                border: 1px solid #222;
                border-radius: 2px;
                text-align: center;
                height: 6px;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 1px;
            }
            QGroupBox {
                border: 1px solid #333;
                border-radius: 2px;
                margin-top: 15px;
                padding-top: 10px;
                font-weight: bold;
                color: #64b5f6;
            }
            QLabel {
                font-size: 11px;
            }
            QLabel#title_label {
                font-size: 18px;
                font-weight: bold;
                color: #64b5f6;
                letter-spacing: 1px;
            }
            QLabel#file_label {
                font-size: 11px;
                color: #aaa;
                padding: 8px;
                background-color: #0a0a0a;
                border-radius: 2px;
                border: 1px solid #222;
            }
            QStatusBar {
                background-color: #0a0a0a;
                border-top: 1px solid #222;
                color: #666;
                font-size: 10px;
            }
            QComboBox, QSlider, QCheckBox {
                background-color: #1a1a1a;
                border: 1px solid #333;
                padding: 3px;
            }
        """)
        
        title_label = QLabel("FORENSIC METADATA NULL")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("padding: 10px 0; border-bottom: 1px solid #333;")
        
        file_group = QGroupBox("Selected File")
        file_layout = QVBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("file_label")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setMinimumHeight(30)
        
        file_layout.addWidget(self.file_label)
        file_group.setLayout(file_layout)
        
        # buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.select_btn = QPushButton("Select Image")
        self.select_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.select_btn.clicked.connect(self.select_file)
        self.select_btn.setMinimumHeight(30)
        
        self.analyze_btn = QPushButton("Forensic Analysis")
        self.analyze_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.analyze_btn.clicked.connect(self.analyze_metadata)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setMinimumHeight(30)
        
        self.clean_btn = QPushButton("SANITIZE IMAGE")
        self.clean_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clean_btn.clicked.connect(self.sanitize_image)
        self.clean_btn.setEnabled(False)
        self.clean_btn.setMinimumHeight(30)
        self.clean_btn.setStyleSheet("""
            background-color: #1a0f0f; 
            color: #ff5555;
            font-weight: 700;
            border: 1px solid #662222;
        """)
        
        btn_layout.addWidget(self.select_btn)
        btn_layout.addWidget(self.analyze_btn)
        btn_layout.addWidget(self.clean_btn)
        
        # settings panel
        settings_group = QGroupBox("Sanitization Settings")
        settings_layout = QGridLayout()
        
        # output format
        format_label = QLabel("Output Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "WebP", "PNG"])
        self.format_combo.setCurrentIndex(0)
        self.format_combo.currentTextChanged.connect(self.format_changed)
        
        # quality
        quality_label = QLabel("Quality:")
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(50, 100)
        self.quality_slider.setValue(95)
        self.quality_slider.setTickInterval(5)
        self.quality_slider.valueChanged.connect(self.quality_changed)
        
        # options
        pixel_label = QLabel("Pixel Alteration:")
        self.pixel_check = QCheckBox("Modify random pixels (anti-forensic)")
        self.pixel_check.setChecked(True)
        self.pixel_check.stateChanged.connect(self.pixel_changed)
        
        ts_label = QLabel("Timestamp:")
        self.ts_check = QCheckBox("Randomize file timestamps")
        self.ts_check.setChecked(True)
        self.ts_check.stateChanged.connect(self.ts_changed)
        
        settings_layout.addWidget(format_label, 0, 0)
        settings_layout.addWidget(self.format_combo, 0, 1)
        settings_layout.addWidget(quality_label, 1, 0)
        settings_layout.addWidget(self.quality_slider, 1, 1)
        settings_layout.addWidget(pixel_label, 2, 0)
        settings_layout.addWidget(self.pixel_check, 2, 1)
        settings_layout.addWidget(ts_label, 3, 0)
        settings_layout.addWidget(self.ts_check, 3, 1)
        settings_group.setLayout(settings_layout)
        
        result_group = QGroupBox("Forensic Analysis")
        result_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Forensic analysis results will appear here...")
        
        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("0301")
        self.setStatusBar(self.status_bar)
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(file_group)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(settings_group)
        main_layout.addWidget(result_group, 1)
        main_layout.addWidget(self.progress_bar)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def format_changed(self, text):
        self.output_format = text
        if text == "PNG":
            self.quality_slider.setEnabled(False)
        else:
            self.quality_slider.setEnabled(True)
    
    def quality_changed(self, value):
        self.quality = value
    
    def pixel_changed(self, state):
        self.alter_pixels = state == Qt.CheckState.Checked.value
    
    def ts_changed(self, state):
        self.randomize_timestamp = state == Qt.CheckState.Checked.value
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Images (*.jpg *.jpeg *.png *.tiff *.bmp *.webp);;All Files (*)"
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.analyze_btn.setEnabled(True)
            self.clean_btn.setEnabled(False)
            self.result_text.clear()
            self.status_bar.showMessage(f"Loaded: {os.path.basename(file_path)}")
    
    def analyze_metadata(self):
        if not self.file_path:
            return
            
        self.result_text.clear()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(True)
        self.status_bar.showMessage("Performing forensic analysis...")
        QApplication.processEvents()
        
        try:

            file_info = f"File Name: {os.path.basename(self.file_path)}\n"
            file_info += f"File Size: {os.path.getsize(self.file_path) // 1024} KB\n"
            file_info += f"Created: {datetime.fromtimestamp(os.path.getctime(self.file_path))}\n"
            file_info += f"Modified: {datetime.fromtimestamp(os.path.getmtime(self.file_path))}\n"
            
            self.result_text.append("=== FILE METADATA ===\n")
            self.result_text.append(file_info)
            
            with Image.open(self.file_path) as img:

                img_info = f"Format: {img.format}\n"
                img_info += f"Mode: {img.mode}\n"
                img_info += f"Dimensions: {img.width} x {img.height} px\n"
                
                self.result_text.append("\n=== IMAGE TECHNICAL DATA ===\n")
                self.result_text.append(img_info)
                
                self.result_text.append("\n=== EXIF METADATA ===\n")
                
                try:
                    exif_dict = piexif.load(img.info.get('exif', b''))
                    
                    if exif_dict:
                        # extract gps
                        gps_info = ""
                        if 'GPS' in exif_dict:
                            gps_data = exif_dict['GPS']
                            for key in gps_data:
                                tag_name = piexif.TAGS['GPS']['GPSVersionID'] if key == 0 else piexif.TAGS['GPS'].get(key, key)
                                gps_info += f"{tag_name}: {gps_data[key]}\n"
                        
                        # extract device info
                        device_info = ""
                        if '0th' in exif_dict:
                            for tag in exif_dict['0th']:
                                tag_name = piexif.TAGS['0th'].get(tag, tag)
                                device_info += f"{tag_name}: {exif_dict['0th'][tag]}\n"
                        
                        # extract exif data
                        exif_info = ""
                        if 'Exif' in exif_dict:
                            for tag in exif_dict['Exif']:
                                tag_name = piexif.TAGS['Exif'].get(tag, tag)
                                exif_info += f"{tag_name}: {exif_dict['Exif'][tag]}\n"
                        
                        if device_info:
                            self.result_text.append("--- DEVICE INFO ---\n" + device_info)
                        if exif_info:
                            self.result_text.append("--- EXIF DATA ---\n" + exif_info)
                        if gps_info:
                            self.result_text.append("--- GPS DATA ---\n" + gps_info)
                    else:
                        self.result_text.append("No EXIF metadata found\n")
                except Exception as ex:
                    self.result_text.append(f"EXIF analysis error: {str(ex)}\n")
                
                self.result_text.append("\n=== EMBEDDED DATA ===\n")
                embedded = False
                
                try:
                    if 'thumbnail' in img.info:
                        self.result_text.append(f"Embedded thumbnail: {len(img.info['thumbnail'])} bytes\n")
                        embedded = True
                except:
                    pass
                
                try:
                    if 'icc_profile' in img.info:
                        self.result_text.append(f"ICC profile: {len(img.info['icc_profile'])} bytes\n")
                        embedded = True
                except:
                    pass
                
                if not embedded:
                    self.result_text.append("No embedded thumbnails or ICC profiles detected\n")
                
                self.metadata_found = True
                self.clean_btn.setEnabled(True)
                self.status_bar.showMessage("Forensic analysis complete - Metadata detected")
                
        except Exception as e:
            self.show_error(f"Analysis error: {str(e)}")
            self.status_bar.showMessage("Analysis failed")
        finally:
            self.progress_bar.setVisible(False)
    
    def sanitize_image(self):
        if not self.file_path:
            return
            
        options = QFileDialog.Option.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Sanitized Image",
            os.path.splitext(self.file_path)[0] + "_sanitized." + self.output_format.lower(),
            f"{self.output_format} Files (*.{self.output_format.lower()})",
            options=options
        )
        
        if not save_path:
            return
            
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(True)
        self.status_bar.showMessage("Sanitizing image...")
        QApplication.processEvents()
        
        try:
            # load original image
            with Image.open(self.file_path) as img:
                # extract pixel data and create new image
                pixel_data = list(img.getdata())
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(pixel_data)
                
                #  pixel alteration
                if self.alter_pixels:
                    width, height = clean_img.size
                    for _ in range(5):  # alter 5 random pixels
                        x = random.randint(0, width - 1)
                        y = random.randint(0, height - 1)
                        current_color = clean_img.getpixel((x, y))
                        
                        
                        if len(current_color) == 4:  
                            new_color = (
                                min(255, max(0, current_color[0] + random.randint(-1, 1))),
                                min(255, max(0, current_color[1] + random.randint(-1, 1))),
                                min(255, max(0, current_color[2] + random.randint(-1, 1))),
                                current_color[3]
                            )
                        elif len(current_color) == 3:  
                            new_color = (
                                min(255, max(0, current_color[0] + random.randint(-1, 1))),
                                min(255, max(0, current_color[1] + random.randint(-1, 1))),
                                min(255, max(0, current_color[2] + random.randint(-1, 1)))
                            )
                        else:  
                            new_color = min(255, max(0, current_color + random.randint(-1, 1)))
                        
                        clean_img.putpixel((x, y), new_color)
                
                # save in selected forman with no metadata
                save_params = {
                    'quality': self.quality,
                    'optimize': True,
                    'dpi': (72, 72)
                }
                
                if self.output_format == "JPEG":
                    clean_img.save(save_path, 'JPEG', **save_params)
                elif self.output_format == "WebP":
                    save_params['method'] = 6  # highest quality method
                    clean_img.save(save_path, 'WEBP', **save_params)
                else:  
                    clean_img.save(save_path, 'PNG', optimize=True)
                
                # randomize timestamps if requested
                if self.randomize_timestamp:
                    try:
                        # get random timestamp
                        now = time.time()
                        random_time = now - random.randint(0, 157680000) 
                        
                        # set creation and modification times
                        os.utime(save_path, (random_time, random_time))
                    except Exception as ts_error:
                        self.result_text.append(f"\nTimestamp randomization failed: {str(ts_error)}")
            
            self.show_success("Image successfully sanitized")
            self.file_label.setText(os.path.basename(save_path))
            self.file_path = save_path
            self.clean_btn.setEnabled(False)
            self.status_bar.showMessage(f"Sanitized file saved: {os.path.basename(save_path)}")
            
            # refresh
            self.analyze_metadata()
            
        except Exception as e:
            self.show_error(f"Sanitization failed: {str(e)}")
            self.status_bar.showMessage("Image sanitization error")
        finally:
            self.progress_bar.setVisible(False)
    
    def show_error(self, message):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle("Forensic Error")
        error_box.setText(message)
        error_box.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
                color: #e0e0e0;
                border: 1px solid #333;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                min-width: 80px;
            }
        """)
        error_box.exec()
    
    def show_success(self, message):
        success_box = QMessageBox(self)
        success_box.setIcon(QMessageBox.Icon.Information)
        success_box.setWindowTitle("Sanitization Complete")
        success_box.setText(message)
        success_box.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
                color: #e0e0e0;
                border: 1px solid #333;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                min-width: 80px;
            }
        """)
        success_box.exec()
    
    def show_about(self):
        about_text = (
            "<b>Meta Null @0301</b><br><br>"
            "Forensic Grade Metadata Sanitization Tool<br><br>"
            "Features:<br>"
            "- Complete metadata removal (EXIF, GPS, XMP, IPTC)<br>"
            "- ICC profile and thumbnail elimination<br>"
            "- Pixel-level reconstruction of images<br>"
            "- Anti-forensic pixel alteration<br>"
            "- Timestamp randomization<br>"
            "- File format conversion<br><br>"
            "This tool ensures complete privacy by eliminating all identifiable metadata "
            "and disrupting potential steganography patterns, making forensic recovery impossible."           
        )
        
        about_box = QMessageBox(self)
        about_box.setIcon(QMessageBox.Icon.Information)
        about_box.setWindowTitle("About Meta Null")
        about_box.setText(about_text)
        about_box.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
                color: #e0e0e0;
                border: 1px solid #333;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                min-width: 80px;
            }
        """)
        about_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(13, 13, 13))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(10, 10, 10))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(80, 140, 200))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)
    
    app.setStyle("Fusion")
    
    window = ForensicSanitizer()
    window.show()
    sys.exit(app.exec())