import yagmail#在网上找的发送邮件的模块，按照格式进行设置就可以进行发送邮件
import time
def email():
    yag = yagmail.SMTP(user='$user',password='$password',host='smtp.qq.com')
    #绑定邮箱账号跟校验码，host设置qq邮箱的smtp服务器域名
    contents=['邮件发送成功！！']#邮件内容设置
    yag.send('$target','邮件头',contents)#绑定发送对象以及邮件主题

n=int(input("请输入发送次数:"))#设置发邮件次数，使用for循环进行控制
t=int(input("请输入时间间隔:"))#设置发送间隔，以秒为单位
for _ in range(n):
    email()
    time.sleep(3)
    print("success!")#发送成功则反馈success
