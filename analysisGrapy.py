import sys
import sqlite3

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QImage, QPixmap

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QDialog,
    QButtonGroup,
    QRadioButton,
    QPushButton,
)

from PyQt6 import uic
from matplotlib import category
from sqlite_project.buildDatabase import buildDatabase
import matplotlib.pyplot as plt


class AnalysisGraph:
    #  初始化
    def __init__(self, parent, ui):
        self.parent = parent
        self.ui = ui

    def generate_pie_chart(self):
        print(123)
        # 获取当前用户的信息
        current_user_id = self.parent.current_user_id
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        table_name = "table_" + str(current_user_id)
        # 按category分类求money的SUM
        cur.execute(f"SELECT category, SUM(money) FROM {table_name} GROUP BY category")

        # 提取类别和总金额数据
        data = cur.fetchall()
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        # 计算百分比
        total_amount = sum(amounts)
        percentages = [amount / total_amount * 100 for amount in amounts]

        # 绘制饼状图
        fig, ax = plt.subplots()
        ax.pie(percentages, labels=categories, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # 保证饼状图是圆形
        ax.set_title("Category Percentages")

        # 转换图表为图像

        image = QImage(400, 300, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        canvas = QtGui.QPainter(image)
        fig.canvas.draw()

        # 创建 QGraphicsPixmapItem，并设置图像
        pixmap = QPixmap.fromImage(image)

        # 创建 QGraphicsScene，并设置场景大小与图像大小相同
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(pixmap.rect())

        # 将 QGraphicsPixmapItem 添加到 QGraphicsScene
        scene.addPixmap(pixmap)

        # 设置 QGraphicsView 的场景
        self.ui.pie.setScene(scene)

        # 关闭数据库连接
        cur.close()
        conn.close()
