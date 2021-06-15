import hashlib


flag=0
flag1=0
flag2=0

class flag:

    #注册时防止竞争条件注入
    flag1=0

    #联系人列表刷新
    flag2=0

    def en(self):
        # print(hashlib.md5(hash("111")).hexdigest())
        m=hashlib.md5()

        m.update('41234'.encode('utf-8'))

        print(m.hexdigest())
