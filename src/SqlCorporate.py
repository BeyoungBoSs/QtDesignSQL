import pymysql


class SqlCorporate:

    #连接数据库
    def connect():
        return pymysql.connect(host='1.xcycloud.xyz',
                             port=54312,
                             user='testUser',
                             password='748956',
                             db='onlineContact',
                             charset='utf8')
    # def connect():
    #     return pymysql.connect(host='192.168。10.132',
    #                          port=3306,
    #                          user='testUser',
    #                          password='748956',
    #                          db='onlineContact',
    #                          charset='utf8')
    #关闭数据库
    def close(db):
        db.close()


    #返回sql查询的结果
    def execute(sql):
        # 打开数据库连接
        db = SqlCorporate.connect()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        try:
            # 执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()
            print("测试:"+str(result))

            # while result != None:
            #     print(result, cursor.rownumber)
            #     result = cursor.fetchone()
            #
            # result = cursor.fetchone()
            # print(result, cursor.rownumber)

        except:
            result = "Error: unable to fetch data"

        # 关闭数据库连接
        SqlCorporate.close(db)
        return result


    #sql插入的结果
    def insert(sql):
        db = SqlCorporate.connect()
        cursor = db.cursor()

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            print('success')
        except:
            # 发生错误时回滚
            db.rollback()
            print('failed')

        SqlCorporate.close(db)

#Test
# if __name__ == '__main__':
#     SqlCorporate.execute("SELECT * FROM message ");
