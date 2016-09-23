from PyQt5.QtWidgets import QGraphicsView


class EasyScaleView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

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
        scale = self.width()/item.pixmap().width()*self.currentScale
        item.setScale(scale)
        rect = item.boundingRect()
        rect.setSize(rect.size() * scale)
        self.setSceneRect(rect)
