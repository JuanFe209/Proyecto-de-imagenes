import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Editor Simple')
lb_image = QLabel('Imagen')
lb_image.setStyleSheet("background-color: #eee; border: 1px solid #ccc")
lb_image.setScaledContents(True)
btn_dir = QPushButton('Carpeta')
lw_files = QListWidget()

btn_left = QPushButton('Izquierda')
btn_right = QPushButton('Derecha')
btn_flip = QPushButton('Reflejo')
btn_bw = QPushButton('B/N')
btn_sharp = QPushButton("Nitidez")

row = QHBoxLayout()
win.setLayout(row)
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.show()

workdir = ' '

def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.lower().endswith(ext):
               result.append(filename)
   return result

def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
   extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        full_path = os.path.join(workdir, filename)
        pixmap = QPixmap(full_path)
        if not pixmap.isNull():
            lb_image.setPixmap(pixmap.scaled(
                lb_image.width(), lb_image.height(), aspectRatioMode=1
            ))
        else:
            lb_image.setText("No se pudo cargar la imagen")

class ImageProcesor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modificado/'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRadio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = (os.path,join(workdir, self.save_dir, self.filename))

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

    def do_right(self):
        self.image = self.image.pygame.transpose(Image.ROTATE_270)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

    def do_flip(self):
        self.image = self.image.transpouse(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

    def do_sharp(self):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(2.0)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

workimage = ImageProcesor()

btn_dir.clicked.connect(showFilenamesList)
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharp)


app.exec()