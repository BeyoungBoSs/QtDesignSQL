sql=input("请输入sql语句:")
print(sql)
#sql为用户输入
dirty_stuff = ['union']
tag=0
while(1): #循环判断，防止双写绕过
    for stuff in dirty_stuff:
        # if(sql.lower().find(stuff)): #防止大小写绕过
        re=sql.replace(stuff," ")
        if re != sql :
            tag=tag=1
        sql=re
    if(tag==0):
        break
    tag=0
print("处理后的sql语句："+sql)