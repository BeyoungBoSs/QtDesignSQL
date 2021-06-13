
import multiprocessing
import random
import hashlib
import sys
import threading
import time
from PySide2.QtGui import QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLineEdit, QMessageBox

from main.contacts import flag

sys.path.append('../')
from src.Manifest import Manifest, showMessage
from src.SqlCorporate import SqlCorporate


def loginButton():

    u=login.lineEdit.text()
    pwd=login.lineEdit_2.text()
    if u=="" or pwd=="":
        showMessage(login, '注意', "用户名或密码不能为空", QMessageBox.Yes)
        return
    re=SqlCorporate.execute("select upassword,uid from users where uname = '"+u+"'")
    try:

        passWord=re[0][0]
        uid = re[0][1]
        m = hashlib.md5()
        m.update((str(len(pwd))+pwd).encode('utf-8'))
        pwd=m.hexdigest()
        if pwd==passWord:
            login.close()
            # app = QApplication(sys.argv)

            manifest = Manifest(uid)
            # 显示
            manifest.ui.show()
            # 监听
            app.aboutToQuit.connect(manifest.closeEvent)
            # sys.exit(app.exec_())
        else:
            login.lineEdit_2.setText("")
            QMessageBox.critical(login, '警告', "用户名或密码错误", QMessageBox.Yes)
    except:
        login.lineEdit_2.setText("")
        print("error")
        QMessageBox.critical(login, '警告', "用户名或密码错误", QMessageBox.Yes)


def forgetP(self):
    # register.setGeometry(100,100,400,400)
    register.show()
    register.pushButton.setDisabled(False)
    register.pushButton_2.clicked.connect(close_1)
    register.lineEdit.setClearButtonEnabled(1)
    register.lineEdit_2.setClearButtonEnabled(1)
    register.lineEdit_3.setClearButtonEnabled(1)
    register.lineEdit_4.setClearButtonEnabled(1)
    register.lineEdit_2.setEchoMode(QLineEdit.Password)
    register.lineEdit_3.setEchoMode(QLineEdit.Password)
    register.pushButton.clicked.connect(re)

def close_1(self):
    contact.flag1=0
    register.close()

#注册界面的确定按钮
def re(self):
    s_uname = register.lineEdit.text()
    s_pwd = register.lineEdit_2.text()
    s_secondPwd = register.lineEdit_3.text()
    s_remeber = register.lineEdit_4.text()
    s_emo = ['━━(￣ー￣*|||━━', 'Hi~ o(*￣▽￣*)', 'ヾ(￣▽￣)Bye~Bye~', '︿(￣︶￣)︿', 'Hi~ o(*￣▽￣*)ブ', '┗( T﹏T )┛']
    if s_remeber=="" or s_pwd=="" or s_secondPwd=="" or s_secondPwd =="":
        register.tip.setText(s_emo[random.randint(0, len(s_emo) - 1)] + "注册项不能为空" + s_emo[random.randint(0, len(s_emo) - 1)])
    else :
        if s_pwd!=s_secondPwd:
            register.tip.setText(s_emo[random.randint(0, len(s_emo) - 1)] + "密码不一致" + s_emo[random.randint(0, len(s_emo) - 1)])
        else:
            try:
                re = SqlCorporate.execute("select uid from users where uname = '" + s_uname + "'")
                time.sleep(0.1)
                print(re)
                s=re[0][0]
                if contact.flag1==0:
                    register.tip.setText(s_emo[random.randint(0, len(s_emo) - 1)] + "用户名已存在" + s_emo[random.randint(0, len(s_emo) - 1)])
            except:
                m = hashlib.md5()
                m.update((str(len(s_pwd)) + s_pwd).encode('utf-8'))
                s_pwd = m.hexdigest()
                sql = "INSERT INTO users(uname,upassword,certify) VALUES ('%s','%s','%s')" % (s_uname,s_pwd,s_remeber)
                print(sql)
                SqlCorporate.insert(sql)
                register.tip.setText(
                    s_emo[random.randint(0, len(s_emo) - 1)] + "注册成功" + s_emo[random.randint(0, len(s_emo) - 1)])
                contact.flag1=1
                register.pushButton.setDisabled(True)

#找回密码
def findBack(self):
    find.show()
    find.confim.setDisabled(False)
    find.cancel.clicked.connect(find.close)
    find.name1.setClearButtonEnabled(1)
    find.pwd.setClearButtonEnabled(1)
    find.pwd_new.setClearButtonEnabled(1)
    find.confim.clicked.connect(findFunction)


#找回密码
def findFunction(self):
    s_pwd=find.pwd_new.text()
    s_remeber=find.pwd.text()
    s_u=find.name1.text()
    # try:
    #     re = SqlCorporate.execute("select certify from users where uname = '"+s_u+"'")
    #     s=re[0][0]
    #     if s==s_remeber:
    #         m = hashlib.md5()
    #         m.update((str(len(s_pwd)) + s_pwd).encode('utf-8'))
    #         s_pwd = m.hexdigest()
    #         sql = "UPDATE users SET upassword="+s_pwd+" WHERE uname='"+s_u+"';"
    #         SqlCorporate.insert(sql)
    #         showMessage(find, '注意', "修改密码成功", QMessageBox.Yes)
    #         find.close()
    #     else:
    #         showMessage(find, '警告', "助记符不正确", QMessageBox.Yes)
    # except:
    #     showMessage(find, '警告', "用户不存在", QMessageBox.Yes)
    # find.close()
    s_emo=['━━(￣ー￣*|||━━','Hi~ o(*￣▽￣*)','ヾ(￣▽￣)Bye~Bye~','︿(￣︶￣)︿','Hi~ o(*￣▽￣*)ブ','┗( T﹏T )┛']
    re = SqlCorporate.execute("select certify from users where uname = '"+s_u+"'")
    try:
        s=re[0][0]
    except:
        find.tip.setText(s_emo[random.randint(0,len(s_emo)-1 )]+"用户名不存在"+s_emo[random.randint(0,len(s_emo)-1 )])
        return
    if s==s_remeber:
        m = hashlib.md5()
        m.update((str(len(s_pwd)) + s_pwd).encode('utf-8'))
        s_pwd = m.hexdigest()
        print(s_pwd)
        sql = "UPDATE users SET upassword='"+s_pwd+"' WHERE uname='"+s_u+"';"
        SqlCorporate.insert(sql)
        find.tip.setText(s_emo[random.randint(0,len(s_emo)-1 )]+"密码修改成功"+s_emo[random.randint(0,len(s_emo)-1 )])
        find.confim.setDisabled(True)
        # showMessage(find, '注意', "修改密码成功", QMessageBox.Yes)
    else:
        find.tip.setText(s_emo[random.randint(0,len(s_emo)-1 )]+"助记符不正确"+s_emo[random.randint(0,len(s_emo)-1 )])
    print('test')

#时间线程
def time_run():
    while 1:
        pix = QPixmap('UI/login' + str(random.randint(1, 20)) + '.png')
        login.pic.setPixmap(pix.scaled(541,239))
        time.sleep(3)

if __name__ == '__main__':
    # #优化多线程
    multiprocessing.freeze_support()
    # #主框架运行
    app = QApplication(sys.argv)
    #初始化登录界面
    login = QUiLoader().load('UI' + '\\' + 'Login.ui')
    #初始化注册界面等待调用
    register = QUiLoader().load('UI' + '\\' + 'register.ui')
    #初始化找回密码界面等待调用
    find = QUiLoader().load('UI' + '\\' + 'find.ui')
    #后台图片刷新线程
    t2 = threading.Thread(target=time_run, args=(), daemon=True)
    t2.start()
    #绑定按钮-登录
    login.login.clicked.connect(loginButton)
    contact=flag()
    login.lineEdit.setClearButtonEnabled(1)
    login.lineEdit_2.setClearButtonEnabled(1)
    login.lineEdit_2.setEchoMode(QLineEdit.Password)
    #绑定按钮-忘记密码
    login.regeist.clicked.connect(forgetP)
    #绑定按钮-找回密码
    login.forget.clicked.connect(findBack)
    # 显示
    login.show()
    sys.exit(app.exec_())