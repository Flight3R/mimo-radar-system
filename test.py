from PyQt6.QtGui import QDrag, QMouseEvent, QPainter, QTransform, QPixmap, QColor, QColorConstants
from PyQt6.QtCore import QByteArray, QDataStream, QIODevice, QPoint, QPointF, Qt, QMimeData, QRectF
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget, \
    QGraphicsSceneMouseEvent


class MyItem(QGraphicsItem):
    def __init__(self, rect, parent=None):
        super().__init__(parent)
        self.rect = rect

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.fillRect(self.rect, QColorConstants.Blue)

    def mimeData(self):
        mimeData = QMimeData()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << self.rect
        mimeData.setData('application/myitem', data)
        return mimeData


class MyScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.scenePos(), QTransform())
            if item is not None:
                data = item.mimeData()
                drag = QDrag(event.widget())
                drag.setMimeData(data)
                drag.setPixmap(QPixmap(item.boundingRect().size().toSize()))
                drag.setHotSpot(event.pos().toPoint() - item.boundingRect().topLeft().toPoint())
                drag.exec()


class MyView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def dragEnterEvent(self, event: QMouseEvent):
        event.acceptProposedAction()

    def dragMoveEvent(self, event: QMouseEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QMouseEvent):
        item = event.mimeData().data('application/myitem')
        if item is not None:
            data = QByteArray(item)
            stream = QDataStream(data, QIODevice.ReadOnly)
            rect = QRectF()
            stream >> rect
            myItem = MyItem(rect)
            self.scene().addItem(myItem)
            myItem.setPos(event.scenePos())
            event.acceptProposedAction()


if __name__ == '__main__':
    app = QApplication([])
    scene = MyScene()
    view = MyView(scene)
    scene.addItem(MyItem(QRectF(0, 0, 50, 50)))
    scene.addItem(MyItem(QRectF(50, 50, 50, 50)))
    view.resize(640, 480)
    view.show()
    app.exec()