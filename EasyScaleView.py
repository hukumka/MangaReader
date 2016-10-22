from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPixmap


class EasyScaleView(QGraphicsView):
    def __init__(self, parent=None):
        self.__scene = QGraphicsScene(parent)
        super().__init__(self.__scene)
        self.currentScale = 1.0

    def zoom(self, mul):
        self.currentScale *= mul
        self.update_scale()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # if self.__item is not None:
        self.update_scale()

    def update_scale(self):
        for i in self.items():
            self.update_item_scale(i)

    def update_item_scale(self, item):
        scale = self.width()/(item.pixmap().width()+1)*self.currentScale
        item.setScale(scale)
        rect = item.boundingRect()
        rect.setSize(rect.size() * scale)
        self.setSceneRect(rect)

    def scroll(self, offset):
        scroll = self.verticalScrollBar()
        scroll.setValue(scroll.value() + offset)


    def display_image(self, image_path):
        print(image_path)
        self.__scene.clear()
        item = QGraphicsPixmapItem(QPixmap(image_path))
        self.__scene.addItem(item)
        self.verticalScrollBar().setValue(0)
        self.update_scale()
