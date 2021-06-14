import datetime
import sys
import PySide2.QtXml

from main.contacts import flag

sys.path.append('../')
import PySide2
from PyQt5.QtCore import Qt
from PySide2 import QtWidgets
from PySide2.QtGui import QPalette, QPixmap
from PySide2.QtWidgets import QMessageBox, QInputDialog
from PySide2.QtUiTools import QUiLoader
import time
import threading

from src.SqlCorporate import SqlCorporate

showMessage = QMessageBox.question


class Manifest(QtWidgets.QMainWindow):
    gUid = 0
    targetUid = -1
    urelate = {}
    list = []


    # 初始化
    def __init__(self, uid):
        super().__init__()
        self.setUid(uid)
        # 获得ui文件
        self.ui = QUiLoader().load('UI' + '\\' + 'QtDesignSQL.ui')
        # 定时器
        t = threading.Thread(target=self.time_run, args=(), daemon=True)
        t.start()
        #获取消息线程
        t1 = threading.Thread(target=self.refreshMessage, args=(), daemon=True)
        t1.start()
        # 联系人按钮
        self.ui.contacts.clicked.connect(self.contacts)
        pix = QPixmap('UI' + '\\' + '1.png')
        self.ui.pic.setPixmap(pix.scaled(90,90))
        # 发送按钮
        self.ui.send.clicked.connect(self.send)
        # 发送文件按钮
        self.ui.send_files.clicked.connect(self.send_files)
        self.ui.contacts_list.itemClicked.connect(self.beClicked)
        # 初始化用户名和在线状态
        self.initUsername()
        # 初始化列表和（uid，uname）的字典
        self.initContactList()
        # self.ui.SQL.setWindowOpacity(0.2)
        self.contactList = QUiLoader().load('UI' + '\\' + 'contacts.ui')
        self.flag_b=flag()
        self.search = QUiLoader().load('UI' + '\\' + 'search.ui')



    #联系人被选中，修改targetID
    def beClicked(self):
        try:
            self.ui.messages.setText("")
            Manifest.list.clear()
            item = self.ui.contacts_list.selectedItems()[0]
            s=item.text()
            new_dict = {v: k for k, v in Manifest.urelate.items()}
            Manifest.targetUid=new_dict[s]
            time.sleep(1)

        except:
            print('error')



    def closeEvent(self):
        return
        # reply = showMessage(self, '警告', "系统将退出,您的帐号即将离线", QMessageBox.Yes)
        # if reply == QMessageBox.Yes:
        #     """
        #     离线操作
        #     """
        #     sys.exit(0)


    # 设置uid
    def setUid(self, uid):
        Manifest.gUid = uid
        print(Manifest.gUid)

    # 初始化用户名和在线状态
    def initUsername(self):
        re = SqlCorporate.execute('select uname from users where uid = ' + str(Manifest.gUid))
        self.ui.username.setText(str(re[0][0]))
        Manifest.urelate[Manifest.gUid]=str(re[0][0])
        # self.ui.online.setText()
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.green)  # 设置字体颜色
        # self.ui.online.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件
        # pe.setColor(QPalette.Window, Qt.blue)  # 设置背景颜色
        # pe.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样
        self.ui.online.setPalette(pe)

    # 初始化联系人列表
    def initContactList(self):
        row_num=self.ui.contacts_list.count()
        print(row_num)
        # self.ui.contacts_list.clear()
        re = SqlCorporate.execute(
            "select uid1,uid2 from contact where flag = 1 and ( uid1 = " + str(Manifest.gUid) + " or uid2 = " + str(
                Manifest.gUid) + " )")
        s = set()
        for i in re:
            for j in i:
                if j != Manifest.gUid:
                    s.add(j)
        #优化的联系人加载
        print(len(s))
        if row_num!=len(s):
            self.ui.contacts_list.clear()
            print(111)
            re2 = SqlCorporate.execute("select uid,uname from users")
            for i in s:
                for j in re2:
                    if j[0]==i:
                        self.ui.contacts_list.addItem(j[1])
                        Manifest.urelate[i] = j[1]
        # for i in s:
        #     re2 = SqlCorporate.execute("select uname from users where uid = " + str(i))
        #     self.ui.contacts_list.addItem(re2[0][0])
        #     Manifest.urelate[i] = re2[0][0]

    # 时钟模块
    def time_run(self):
        while 1:
            self.ui.hours.display(time.strftime("%H"))
            self.ui.minutes.display(time.strftime("%M"))
            time.sleep(10)
            # if self.flag_b.flag2==1:
            #     self.initContactList()
            #     self.flag_b.flag2=0
            self.initContactList()

    #消息模块
    def refreshMessage(self):
        try:
            while 1:
                self.ui.messages.ensureCursorVisible()  # 游标可用
                cursor = self.ui.messages.textCursor()  # 设置游标
                pos = len(self.ui.messages.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.ui.messages.setTextCursor(cursor)  # 滚动到游标位置
                time.sleep(1)
                if Manifest.targetUid !=-1:
                    sql="select id,message,time,uidSend from message where ( uidSend = '"+str(Manifest.gUid)+"' and uidRecipient = '"+str(Manifest.targetUid)+"' ) or ( uidSend = '"+str(Manifest.targetUid)+"' and uidRecipient = '"+str(Manifest.gUid) +"' )"
                    print(sql)

                    re = SqlCorporate.execute(sql)

                    print(re)
                if Manifest.targetUid != -1:
                    ii = 0
                    for i in  re:
                        print(len(re))

                        print(ii)
                        ii=ii+1
                        if i[0] not in Manifest.list:
                            s_l='<p><font color="'
                            if i[3]==Manifest.gUid:
                                s_c='red'
                            else:
                                s_c='green'
                            s_r='">'
                            ss=s_l+s_c+s_r
                            s_last='</font></p>'
                            Manifest.list.append(i[0])
                            print(ss+str(i[2])+s_last+ss+i[1]+s_last)
                            print("]")
                            time.sleep(0.05)
                            self.ui.messages.append(ss+str(i[2])+s_last+ss+i[1]+s_last+'<p><font color="black">-------------------------------</font></p>')
                            print("!")
                            # self.ui.messages.append('<p><font color="red">---</font></p>')





        except:
            print("消息模块出错")

    # 新增联系人
    def contacts(self):
        #self.con……不是self.ui.con……
        self.contactList.setWindowFlags(PySide2.QtCore.Qt.WindowStaysOnTopHint)
        self.contactList.out.clicked.connect(self.contact_op)
        self.contactList.list.clear()
        re = SqlCorporate.execute(
            "select uid1,uid2 from contact where ( uid1 = " + str(Manifest.gUid) + " or uid2 = " + str(
                Manifest.gUid) + " )")
        s = set()
        for i in re:
            for j in i:
                if j != Manifest.gUid:
                    s.add(j)
        re2 = SqlCorporate.execute("select uid,uname from users ")
        sql = 'select flag,uid1,uid2 from contact '
        re3 = SqlCorporate.execute(sql)
        #优化速度
        list = set()
        for uid in s:
            for j in re2:
                if j[0]==uid:
                    uname=j[1]
                    break

            # for i in range(self.contactList.list.count()):
            #     list.add(self.contactList.list.item(i).text().replace("[待确认]", ""))
            for flag in re3:
                if uname not in list:
                    if flag[0]==1 and ( ( flag[1]==Manifest.gUid and flag[2]==uid ) or ( flag[2]==Manifest.gUid and flag[1]==uid ) ) :
                        self.contactList.list.addItem(uname)
                        list.add(uname)
                    elif flag[0]==0 and  flag[2]==Manifest.gUid and flag[1]==uid :
                        self.contactList.list.addItem(uname+'[待确认]')
                        list.add(uname)
                    Manifest.urelate[uid] = uname

            #未优化速度
        # for i in s:
        #     re2 = SqlCorporate.execute("select uname from users where uid = " + str(i))
        #     sql='select flag,uid1 from contact where ( uid1 = "'+str(Manifest.gUid)+'"and uid2 = "'+str(i)+'" ) or ( uid2 = "'+str(Manifest.gUid)+'"and uid1 = "'+str(i)+'")'
        #     print(sql)
        #     re3=SqlCorporate.execute(sql)
        #     if re3[0][0]==1:
        #         self.contactList.list.addItem(re2[0][0])
        #     elif re3[0][0]==0 and re3[0][1]!=Manifest.gUid:
        #         self.contactList.list.addItem(re2[0][0]+'[待确认]')
        #     Manifest.urelate[i] = re2[0][0]
        self.contactList.list.addItem("+++添加联系人")
        self.contactList.list.itemDoubleClicked.connect(self.addContact)
        self.contactList.show()

    def addContact(self):
        item = self.contactList.list.selectedItems()[0]
        s=item.text()
        if s=="":
            print("blank")
        elif s=='+++添加联系人':
            print("new")
            back=QInputDialog.getText(self.contactList.list, "添加联系人", "请输入uid或者用户名", text="")
            if back[1]==True:
                sql='select uid from users where uid = "'+back[0]+'" or uname="'+back[0]+'"'
                re =SqlCorporate.execute(sql)
                print(re)
                try:
                    t=re[0][0]
                    if t!=Manifest.gUid:
                        print(t)
                        sql = "INSERT INTO contact(uid1,uid2,flag) VALUES ('%d','%d','%d')" % (Manifest.gUid,t,0)
                        print(sql)
                        SqlCorporate.insert(sql)
                        self.flag_b.flag2=1
                        self.refresh()
                    else:
                        showMessage(self.contactList.list, "注意", '不能添加自己！', QMessageBox.Yes)
                except:
                    showMessage(self.contactList.list, "警告", '用户不存在', QMessageBox.Yes )
            self.refresh()
        else:
            s1 = s.replace("[待确认]", "")
            #s1==s表示没替换
            if s1!=s:
                re=showMessage(self.contactList,"注意",'是否确认与" '+s1+' "成为好友?',QMessageBox.Yes|QMessageBox.No)
                print(Manifest.urelate)
                new_dict = {v: k for k, v in Manifest.urelate.items()}
                i = new_dict[s1]
                if re==QMessageBox.Yes:
                    sql='update contact set flag=1 where ( uid1 = "' + str(Manifest.gUid) + '" and uid2 = "' + str(i) + '" ) or ( uid1 = "' + str(i) + '" and uid2 = "' + str(Manifest.gUid) + '" ) '
                    SqlCorporate.insert(sql)
                else:
                    re1 = showMessage(self.contactList, "注意", '不成为好友，是否删除好友请求" ' + s1 + ' "?', QMessageBox.Yes | QMessageBox.No)
                    if re1 == QMessageBox.Yes:
                        sql = 'DELETE FROM contact WHERE ( uid1 = "' + str(Manifest.gUid) + '" and uid2 = "' + str(i) + '" ) or ( uid1 = "' + str(i) + '" and uid2 = "' + str(Manifest.gUid) + '" ) '
                        SqlCorporate.insert(sql)
                self.refresh()
            else:
                re=showMessage(self.contactList,"注意",'是否删除" '+s+' "?',QMessageBox.Yes|QMessageBox.No)
                if re==QMessageBox.Yes:
                    print('Yes')
                    new_dict = {v: k for k, v in Manifest.urelate.items()}
                    i = new_dict[s]
                    print(i,type(Manifest.gUid),type(i))
                    sql='DELETE FROM contact WHERE ( uid1 = "'+ str(Manifest.gUid) +'" and uid2 = "'+str(i)+ '" ) or ( uid1 = "'+str(i) +'" and uid2 = "'+str(Manifest.gUid)+'" ) '
                    SqlCorporate.insert(sql)
                    self.ui.messages.clear()
                self.refresh()

    #刷新
    def refresh(self):
        self.contactList.close()
        self.contacts()


    #联系人列表推出按钮作用
    def contact_op(self):
        self.contactList.close()
        #清空列表

        #初始化列表
        self.initContactList()




    # 发送信息
    def send(self):
        strings = self.ui.test_edit.toPlainText()
        print(strings)
        self.ui.test_edit.clear()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if strings=="":
            showMessage(self, '注意', "输入为空", QMessageBox.Yes)
            return
        sql="INSERT INTO message(uidSend, uidRecipient, message, time) VALUES ('%d', '%d',  '%s',  '%s')" %(Manifest.gUid, Manifest.targetUid, strings, dt)
        SqlCorporate.insert(sql)

    # 发送文件名
    def send_files(self):
        self.search.setWindowFlags(PySide2.QtCore.Qt.WindowStaysOnTopHint)
        self.search.show()
        self.search.cancel.clicked.connect(self.close1)
        list=['id或用户名','信息内容','开始时间']
        self.search.comboBox.clear()
        self.search.comboBox.addItems(list)
        self.history_display(0,"")
        self.search.button.clicked.connect(self.display)

    def close1(self):
        self.search.close()


    def display(self):
        self.search.text.clear()
        SqlCorporate.insert('CREATE VIEW mess AS SELECT users.uname,message.message FROM message,users WHERE message.uidSend = '+str(Manifest.gUid)+' and users.uid=message.uidSend')
        s=self.search.comboBox.currentText()
        ss=self.search.lineEdit.text()
        if s=='id或用户名':
            if ss.isdigit()==False:
                new_dict = {v: k for k, v in Manifest.urelate.items()}
                ss = new_dict[ss]
            self.history_display(1,ss)
        elif s=='信息内容':
            self.history_display(2,ss)

        else:
            self.history_display(3,ss)
        print(s)

    def history_display(self,flag,s):
        self.search.text.clear()
        # sql="select id,message,time,uidSend from message where ( uidSend = '"+str(Manifest.gUid)+"' and uidRecipient = '"+str(Manifest.targetUid)+"' ) or ( uidSend = '"+str(Manifest.targetUid)+"' and uidRecipient = '"+str(Manifest.gUid) +"' )"
        if flag==1:
            sql="select id,message,time,uidSend,uidRecipient from message where ( uidSend = '"+str(Manifest.gUid)+"' and uidRecipient = '"+str(s)+"' ) or ( uidSend = '"+str(s)+"' and uidRecipient = '"+str(Manifest.gUid) +"' )"
        elif flag==2:
            print(2)
            sql='select id,message,time,uidSend,uidRecipient from message where message like "%'+s+'%"'
        elif flag==3:
            print(3)
            sql = 'select id,message,time,uidSend,uidRecipient from message where time >= "' + s + '"'
        else:
            sql = "select id,message,time,uidSend,uidRecipient from message where  uidSend = '" + str(Manifest.gUid) + "' or  uidRecipient = '" + str(Manifest.gUid) + "' "
        print(sql)
        re = SqlCorporate.execute(sql)
        print(re)
        for i in  re:
            s_l='<p><font color="'

            if i[3]==Manifest.gUid:
                s_c='red'
            else:
                s_c='green'
            s_r='">'
            ss=s_l+s_c+s_r
            s_last='</font></p>'
            print(i)
            print(Manifest.urelate[i[3]],i[4],Manifest.urelate[i[4]])

            u2u=Manifest.urelate[i[3]]+' 发送给 '+Manifest.urelate[i[4]]+"  时间:"
            print(ss+u2u+str(i[2])+s_last+ss+i[1]+s_last)
            # time.sleep(0.1)
            print(222)
            self.search.text.append(ss+u2u+str(i[2])+s_last+ss+i[1]+s_last+'<p><font color="black">-------------------------------</font></p>')
        self.search.text.ensureCursorVisible()  # 游标可用
        cursor = self.search.text.textCursor()  # 设置游标
        pos = len(self.search.text.toPlainText())  # 获取文本尾部的位置
        cursor.setPosition(pos)  # 游标位置设置为尾部
        self.search.text.setTextCursor(cursor)  # 滚动到游标位置


