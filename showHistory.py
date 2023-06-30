import sys
import sqlite3

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QDialog,
    QButtonGroup,
    QRadioButton,
)

from PyQt6 import uic
from matplotlib import category
from sqlite_project.buildDatabase import buildDatabase
import matplotlib.pyplot as plt


class ShowHistory:
    #  初始化
    def __init__(self, parent, ui):
        self.parent = parent
        self.ui = ui

    def showinTable(self):
        # print(1234)
        rank = self.ui.query_type_combox.currentText() 

        if rank == '金额':
            rank2 = 'money'

        if rank == "时间":
            rank2 = 'date'

        if rank == "分类":
            rank2 = "category"

        if rank == "不包含查询条条件":
            rank2 = "money"

        #把时间标准化的函数
        def split_date(date_string):
            parts = date_string.split('/')
            print(parts[0])
            len_mon = len(parts[1])
            len_day = len(parts[2])
            print(len_mon,len_day)
            if len_mon == 1:
                parts[1] = '0'+parts[1]
            print(parts[1]) 
            if len_day == 6 or len_day == 1:
                parts[2] = '0'+parts[2]
            print(parts[2])
            parts = parts[0]+parts[1]+parts[2]
            parts = parts[:8]
            print(parts)
            return parts
        

        max_money = self.ui.max_account_line.text() 
        min_money = self.ui.min_account_line.text()
        start_time = self.ui.start_time.text()
        end_time = self.ui.end_time.text()

        start_time = split_date(start_time)
        end_time = split_date(end_time)


        category1 = self.ui.type_combox.currentText()
        print(max_money,min_money,start_time,end_time,rank,category1)
        
        # 获取当前用户的id
        current_user_id = self.parent.current_user_id

        # 构建当前用户的表名
        table_name = "table_" + str(current_user_id)

        # 连接数据库
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

# 查询当前用户的历史账单信息
        if rank == '金额':

            rows = cur.execute(f"SELECT * FROM {table_name} WHERE  money BETWEEN '{min_money}'AND '{max_money}'ORDER BY {rank2}").fetchall()
        
        if rank == '时间':
            
            rows_all = cur.execute(f"SELECT * FROM {table_name}  ORDER BY {rank2}").fetchall()
            print(rows_all)
            rows = []
            for each in rows_all:
                cur_date = each[6]
                cur_date = split_date(cur_date)
                print(cur_date,start_time,end_time)
                if int(cur_date) >= int(start_time) and int(cur_date) <= int(end_time):
                    rows.append(each) 
                
                
        if rank == '分类':

            rows = cur.execute(f"SELECT * FROM {table_name} WHERE  category LIKE '{category1}' ORDER BY money").fetchall()

        if rank == "不包含查询条条件":

            rows = cur.execute(f"SELECT * FROM {table_name} ORDER BY {rank2}").fetchall()

        # 设置表格的行数和列数
        rowCount = len(rows)
        self.ui.HistoryTable.setRowCount(rowCount)
        print(rowCount)

    #如果无符合条件的记录，则弹出Qmessagebox提示用户重新输入正确的查询范围
        if rowCount <= 0:
            
            # 创建QMessageBox实例
            message_box = QMessageBox()
            message_box.setWindowTitle("提示")
            message_box.setText("无符合条件的记录,请重新输入正确的查询范围")
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            # 显示消息框并获取结果
            result = message_box.exec()

            # 根据结果进行处理
            if result == QMessageBox.StandardButton.Ok:
                print("用户点击了确定按钮")

            return 
        

    #当查询结果不为空，则将查询结果返回用户界面

        self.ui.HistoryTable.setColumnCount(len(rows[0]))  # 假设每行的列数相同

        # 遍历查询结果，将数据填充到表格中
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                # 将数据设置到相应的单元格中
                self.ui.HistoryTable.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(value))
                )
        # 关闭数据库连接
        cur.close()
        conn.close()
