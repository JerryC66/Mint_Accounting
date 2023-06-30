import sys
import sqlite3

from PyQt6 import QtWidgets, QtGui,QtCore
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

from showHistory import ShowHistory
from analysisGrapy import AnalysisGraph
from PyQt6.QtCharts import QChartView, QPieSeries, QChart
from PyQt6.QtGui import QPen




""" 登录注册类 """
class EnterWindow(QDialog):
    # dw：换成了QDialog作为父类，entrance.ui也一起改了，主要是方便设置为模态窗口
    def __init__(self):  
    # dw：改了这个初始化函数以及下面初始化父类的语句，登录对话框不需要父窗口
        super().__init__()

        # 登录界面的初始化代码
        from entrance_ui import Ui_loginDlg
        self.ui = Ui_loginDlg()
        self.ui.setupUi(self)

        # dw：设置一个登录窗口的状态码，根据这个状态码决定后续操作如何：
        # 0：登录成功，-1：登录失败，-2：注册失败 ……
        self.login_code = -1
        self.login_user_id = None

        self.ui.Quit.clicked.connect(QApplication.quit)
        self.ui.Login.clicked.connect(self.handle_login)
        self.ui.Register.clicked.connect(self.handle_register)

    def handle_login(self):
        """登录操作"""
        username = self.ui.Inputusername.text()
        password = self.ui.Inputpassword.text()

        # 用户信息已经储存到database里面，所以只用验证
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        # 查询数据库中是否存在匹配的用户名和密码
        rows = cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = rows.fetchone()  # 获取查询结果的第一行
        conn.close()

        if result:
            # 用户名和密码匹配成功，进入主界面
            QMessageBox.information(self, "登录成功", "用户名和密码验证通过")

            # dw：这里只修改登录状态码，不打开主窗口
            # self.open_main_window()
            self.login_code = 0
            # 从rows里把id拿出来保存
            self.login_user_id = result[0]
            self.close()  # dw：关闭登录窗口，结束阻塞，让程序能接着main()里面的w.exec()之后继续往下走
        else:
            # 用户名和密码不匹配，显示错误提示
            QMessageBox.warning(self, "登录失败", "用户名或密码错误")

    def handle_register(self):
        username = self.ui.Inputusername.text()
        password = self.ui.Inputpassword.text()
        # 显示提示信息
        QMessageBox.information(self, "登录确认", f"用户名：{username}\n密码:{password}")

        # 注册，需要将用户名密码写入database
        buildDatabase()
        # 进入数据库
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        # 获取行数
        cur.execute(""" SELECT COUNT(*) FROM users; """)
        row_count = int(cur.fetchone()[0])
        # 存入列表
        userinfo = [row_count + 10001, username, password]
        # 插入数据库
        cur.execute(
            "INSERT INTO users(user_id,username,password) VALUES (?,?,?);",
            userinfo,
        )

        # 拼接账目表的表名
        new_table = "table_" + str(userinfo[0])
        sql = (
            "CREATE TABLE IF NOT EXISTS %s(id INT NOT NULL, type TEXT NOT NULL, money FLOAT NOT NULL,category TEXT NOT NULL, comment TEXT NOT NULL,mood TEXT NOT NULL,date TEXT NOT NULL,PRIMARY KEY (id));"
            % new_table
        )
        cur.execute(sql)

        # 设置目标额度
        limit_table = "limit_table_" + str(userinfo[0])
        sql2 = (
            "CREATE TABLE IF NOT EXISTS %s(id INT NOT NULL, day_limit TEXT NOT NULL, month_limit TEXT NOT NULL,year_limit TEXT NOT NULL,PRIMARY KEY (id));"
            % limit_table
        )
        cur.execute(sql2)

        conn.commit()  # 事务
        conn.close()

        # 注册成功提示
        QMessageBox.information(self, "注册成功", "用户注册成功")

    # def open_main_window(self):
    #     # 创建主界面窗口并显示
    #     main_window = MainWindow()
    #     main_window.show()
    #     self.close()  # 关闭登录窗口
    # dw：不在登录窗口的方法里打开主窗口
    # 原因：首先现在的main_window是局部对象，离开这个函数后这个对象就没有了，无法一直存留
    # 其次，主窗口作为一个登录完就关闭的窗口的一个属性，不太合适

class InsertItem:
    #  初始化
    def __init__(self, parent, ui):
        # 这里的parent就是MainWindow类，ui是主窗口的ui
        self.parent = parent
        self.ui = ui

    def addItem(self):
        type = ""
        money = -1.0
        category = ""
        comment = ""
        mood = ""
        date = ""
        # 建立信号和槽
        # # 返回当前选择项的索引的对应文本
        type = self.ui.RevenueAndExpenditureBox.itemText(
            self.ui.RevenueAndExpenditureBox.currentIndex())
        # 返回金额，类别，备注
        money = self.ui.MoneyBox.text()
        category = self.ui.ClassificationBox.itemText(
            self.ui.ClassificationBox.currentIndex())
        comment = self.ui.NotesBox.text()
        mood = self.parent.selectedOption
        print(mood)
        # 获取时间
        date = self.ui.DateBox.text()
        # 数据录入
        try:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            # 获取行数
            table_name = "table_%d" % self.parent.current_user_id
            c.execute("SELECT COUNT(*) FROM %s;" % table_name)
            row_count = int(c.fetchone()[0])
            # 存入列表
            userinfo = [row_count + 10001, type, money, category, comment, mood, date]
            c.execute(
                "INSERT INTO %s(id,type,money,category,comment,mood,date) VALUES (?,?,?,?,?,?,?)" % table_name, userinfo,)

            conn.commit()
            c.close()
            conn.close()
            QMessageBox.information(
                QMessageBox(),
                "Successful",
                "Item is added successfully to the database.",
            )
        except Exception:
            QMessageBox.warning(
                QMessageBox(), "Error", "Fail to add item to the database."
            )




""" 搜索账单类 """

""" 设定额度类 """
class limitSetting:
    def __init__(self, parent, ui):
        # 这里的parent就是MainWindow类，ui是主窗口的ui
        self.parent = parent
        self.ui = ui

    def setting(self):
        day_limit = self.ui.new_day_target_line.text()
        month_limit = self.ui.new_month_target_line.text()
        year_limit = self.ui.new_year_target_line.text()
        print('已获取输入信息')

        try:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            table_name = "limit_table_%d" % self.parent.current_user_id
            c.execute("SELECT COUNT(*) FROM %s;" % table_name)
            row_count = int(c.fetchone()[0])
            userinfo = [row_count, day_limit, month_limit, year_limit]
            c.execute(
                "INSERT INTO %s(id, day_limit, month_limit, year_limit) VALUES (?,?,?,?)"
                % table_name,
                userinfo,
            )

            conn.commit()
            c.close()
            conn.close()
            QMessageBox.information(
                QMessageBox(),
                "成功",
                "额度设置成功。",
            )
            print('额度设置成功')
        except Exception:
            QMessageBox.warning(QMessageBox(), "错误", "无法设置额度。")

    def showSetting(self):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        table_name = "limit_table_%d" % self.parent.current_user_id
        c.execute("SELECT * FROM %s ORDER BY id DESC LIMIT 1" % table_name)
        latest_row = c.fetchone()
        print('获取到最后一行数据')

        if latest_row:
            # 处理最新一行数据，分别显示到三个label里面
           self.ui.DayTarget.setText(latest_row[1])
           self.ui.MonthTarget.setText(latest_row[2])
           self.ui.YearTarget.setText(latest_row[3])
        else:
            print("数据库中没有数据")
    
""" 主窗口类 """
class MainWindow(QMainWindow):
    showHistory = None
    def __init__(self, userid ,parent=None):
        QMainWindow.__init__(self, parent)
        
        from main_ui import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_user_id = userid 

    
        #  连接心情单选框的信号和槽
        # 创建一个按钮组并添加单选框
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.ui.happy)
        self.buttonGroup.addButton(self.ui.sad)
        self.buttonGroup.addButton(self.ui.angry)
        self.buttonGroup.addButton(self.ui.calm)
        self.buttonGroup.addButton(self.ui.grief)
        self.buttonGroup.addButton(self.ui.excited)
        self.buttonGroup.buttonClicked.connect(self.handleRadioButtonClicked)

        # 建立确认按钮信号和槽的连接
        self.ui.ensureInsert.clicked.connect(self.addingItem)

        # 建立历史记录表信号和槽的连接
        self.ui.HistoryTable.clicked.connect(self.showData)

        # 建立扇形表信号和槽的连


        # 创建饼图数据
        self.pieseries = QPieSeries()  # 定义PieSeries

        # 计算category各值的比例
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        table_name = "table_" + str(self.current_user_id)
        cur.execute("SELECT * FROM %s" % table_name)
        results = cur.fetchall()
        label_counts = {}
        if len(results) == 0:
            print("表中没有数据或表不存在。")
        else:
            for row in results:
                if len(row) >= 5:  # 确保结果行中至少有 5 个元素（包括 category 列）
                    category = row[3]  # 将索引 3 更改为 category 列所在的整数索引
                    if category in label_counts:
                        label_counts[category] += 1
                    else:
                        label_counts[category] = 1
        total_records = len(results)
        label_proportions = {}
        for label, count in label_counts.items():
            proportion = count / total_records
            label_proportions[label] = proportion
            # 将每个标签和对应的比例添加到 pieseries 中
            self.pieseries.append(label, proportion)
        # 得到饼图的某一个元素切片，在这取得为第一个
        self.slice = self.pieseries.slices()[0]  
        self.slice.setExploded()  # 设置为exploded
        self.slice.setLabelVisible()  # 设置Lable
        self.slice.setPen(QPen(Qt.GlobalColor.darkGreen, 1))  # 设置边框画笔类型
        self.slice.setBrush(Qt.GlobalColor.green)  # 设置笔刷

        # 第二个切片
        self.slice = self.pieseries.slices()[1] 
        self.slice.setExploded()  
        self.slice.setLabelVisible() 
        self.slice.setPen(QPen(Qt.GlobalColor.darkBlue, 1))
        self.slice.setBrush(Qt.GlobalColor.blue) 

        # 第三个切片
        self.slice = self.pieseries.slices()[2] 
        self.slice.setExploded()  
        self.slice.setLabelVisible() 
        self.slice.setPen(QPen(Qt.GlobalColor.darkRed, 1))
        self.slice.setBrush(Qt.GlobalColor.red)

        # 第四个切片
        self.slice = self.pieseries.slices()[3] 
        self.slice.setExploded()  
        self.slice.setLabelVisible() 
        self.slice.setPen(QPen(Qt.GlobalColor.darkYellow, 1))
        self.slice.setBrush(Qt.GlobalColor.yellow)   

        # 第五个切片
        self.slice = self.pieseries.slices()[4] 
        self.slice.setExploded()  
        self.slice.setLabelVisible() 
        self.slice.setPen(QPen(Qt.GlobalColor.darkCyan, 1))
        self.slice.setBrush(Qt.GlobalColor.cyan)   

        # 第六个切片
        self.slice = self.pieseries.slices()[5] 
        self.slice.setExploded()  
        self.slice.setLabelVisible() 
        self.slice.setPen(QPen(Qt.GlobalColor.darkMagenta, 1))
        self.slice.setBrush(Qt.GlobalColor.magenta)   
   

        self.chart = QChart()  # 定义QChart
        self.chart.addSeries(self.pieseries)  # 将 pieseries添加到chart里
        self.chart.setTitle("Simple piechart example")  # 设置char的标题
        # self.chart.legend().hide()  # 将char的legend设置为隐藏

        self.ui.pie.setChart(self.chart)  # 拿到ui中的GraphicsView控件对象gview，将创建的chart关联到控件中
        self.ui.pie.show()  # 将ChartView显示出来
        
        # self.pieseries.append("购物", label_proportions[label])
        # self.pieseries.append("日用", label_proportions[label])
        # self.pieseries.append("交通", label_proportions[label])
        # self.pieseries.append("娱乐", label_proportions[label])
        # self.pieseries.append("学习", label_proportions[label]) 
        self.selectedOption = ""  

        # 查询按钮建立信号和槽
        self.showHistory = ShowHistory(self, self.ui)
        query_button: QPushButton = self.ui.query_button
        query_button.clicked.connect(self.showHistory.showinTable)

        # 设置额度文本建立信号和槽
        self.ui.reset_target_button.clicked.connect(self.showSetting)

        # 始终存在的文本内容
        limit = limitSetting(self,self.ui)
        limit.showSetting()

    """ 把新的记账条目写入数据库"""
    def addingItem(self):
        insert_tool = InsertItem(self, self.ui)
        # 把MainWindow这个类和这个类的ui都传入InsertItem类，将InsertItem类的一个实例对象赋值给insert_tool变量，InsertItem类里面也可以有current_user_id
        insert_tool.addItem()  # 对insert_tool进行添加操作，即对主窗口这个实例的self进行了添加操作

    """获取心情"""
    def handleRadioButtonClicked(self, radioButton: QRadioButton):
        self.selectedOption = radioButton.objectName()
        print(self.selectedOption)
        QMessageBox.information(self, "123", self.selectedOption)

    """ 展示历史数据 """
    def showData(self):
        show_table = ShowHistory(self, self.ui)
        show_table.showinTable()

    """ 展示额度设置 """
    def showSetting(self):
        setting_tool = limitSetting(self,self.ui)
        setting_tool.setting()
        setting_tool.showSetting()

    """ 退出×键设置 """
    def closeEvent(self, event):
        reply = QMessageBox.question(
        self,
        "确认",
        "您确定要退出吗？",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

from main_ui import Ui_MainWindow

""" 主函数 """
def main():
    app = QApplication(sys.argv)
    w = EnterWindow()
    # dw：QDialog类的exce()方法，是将对话框以模态的方式显示出来，程序会在这里阻塞
    # 关闭登录对话框之后会结束阻塞，继续往下走
    w.exec()
    # dw：根据登录状态码决定后续怎么做
    if w.login_code == 0:
        main_window = MainWindow(w.login_user_id)
        # main_window.current_user_id = w.login_user_id
        main_window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()




# def main():
#     app = QApplication(sys.argv)
#     w = EnterWindow()

#     # dw：QDialog类的exce()方法，是将对话框以模态的方式显示出来，程序会在这里阻塞
#     # 关闭登录对话框之后会结束阻塞，继续往下走
#     w.exec()

#     # dw：根据登录状态码决定后续怎么做
#     if w.login_code == 0:
#         # main_window = MainWindow()
        
#         main_window = QMainWindow()
#         ui = Ui_MainWindow()
#         ui.setupUi(main_window)
#         ui.happyImage.setPixmap(QtGui.QPixmap(r'.\images\开心.jpg'))  
#         ui.angryImage.setPixmap(QtGui.QPixmap(r'.\images\生气.jpg'))
#         ui.sadImage.setPixmap(QtGui.QPixmap(r'.\images\难过.jpg'))
#         ui.griefImage.setPixmap(QtGui.QPixmap(r'.\images\委屈.jpg'))
#         ui.calmImage.setPixmap(QtGui.QPixmap(r'.\images\平静.png'))
#         ui.excitedImage.setPixmap(QtGui.QPixmap(r'.\images\兴奋.jpg'))
#         img1 = QtGui.QImage(r'.\images\Me.jpg')
#         pixmap1= QtGui.QPixmap.fromImage(img1)
#         fitPixmap1 = pixmap1.scaled(50, 49)    
#         icon1 = QtGui.QIcon(fitPixmap1)
#         ui.Me.setIcon(icon1)
#         ui.Me.setIconSize(QtCore.QSize(48, 48))
#         img2= QtGui.QImage(r'.\images\refresh.jpg')
#         pixmap2 = QtGui.QPixmap.fromImage(img2)
#         fitPixmap2 = pixmap2.scaled(50, 49)    
#         icon2 = QtGui.QIcon(fitPixmap2)
#         ui.Refresh.setIcon(icon2)
#         ui.Refresh.setIconSize(QtCore.QSize(48, 48))
#         main_window.show()
        
#         # 获得当前用户的id
#         main_window.current_user_id = w.login_user_id
#         sys.exit(app.exec())


# if __name__ == "__main__":
#     main()