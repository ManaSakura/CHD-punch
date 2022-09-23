import time
import logging
from datetime import datetime
import yagmail
from selenium import  webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

'''
需要更改的地方：
1. 38 行edge引擎绝对路径
2. 111 行 mail_user 发送打卡信息的邮箱
3. 111 行 mail_code 163邮箱第三方授权码
'''

mail_user = 'XingyouTang109@163.com'    # 发送打卡提示的163邮箱
mail_code = 'VUPGIYDRFPUKIBEK'   # SMTP第三方app授权码

username_lst = ['2021226069', '2021126118', '2021220005']     # 学号列表
password_lst = ['txy199906301152', '19980820hgjj', 'lxs140723']    # 密码列表
receiver_mail_lst = ['1804151045@qq.com', '1105323812@qq.com', '1223015240@qq.com'] # 接收打卡提示的邮箱列表

# username_lst = ['2021226069']     # 学号列表
# password_lst = ['txy199906301152']    # 密码列表
# receiver_mail_lst = ['1804151045@qq.com'] # 接收打卡提示的邮箱列表


def person_submit(username, password):
    '''
    信网处快速打卡（一个人）
    :param username:    学号
    :param password:    密码
    :return:
    '''
    # 1 信网处登录学号和密码
    # option = webdriver.EdgeOptions()
    # option.add_argument('headless')
    service = Service(r'C:\Users\tang xingyou\AppData\Local\Programs\Python\Python37\msedgedriver.exe')
    driver = webdriver.Edge(service=service)
    chd_edu_url = 'https://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fcdjk.chd.edu.cn%2FhealthPunch%2Findex%2Flogin'
    driver.get(chd_edu_url)
    print('浏览器加载中...')
    time.sleep(5)
    print('正在填写提交用户登录账号和密码...')
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    login_btn = driver.find_element(By.ID, 'login_submit')
    username_input.send_keys(username)
    time.sleep(2)
    password_input.send_keys(password)
    time.sleep(2)
    login_btn.click()
    time.sleep(2)
    # 2 登录成功后更新地址
    address_update_before_text = '点击获取详细地址'
    address_div = driver.find_element(By.ID, 'xxdz41')
    if address_div.get_attribute('innerHTML') == address_update_before_text:
        print('健康打卡界面加载成功')
        time.sleep(2)
        # 点击更新前信息
        updatebefore_address_div = driver.find_element(By.ID, 'xxdz41')
        updaetbefore_address_div_display = updatebefore_address_div.value_of_css_property('display')
        # print('定位更新前', updaetbefore_address_div_display)
        # 点击更新地址
        address_div.click()
        print('地址更新中......')
        time.sleep(10)
        update_address_div = driver.find_element(By.ID, 'xxdz41')
        update_address_div_display = update_address_div.value_of_css_property('display')
        # print('定位更新后', update_address_div_display)
        if update_address_div_display == 'none':
            print('定位更新成功')
            # 寻找textarea并填入信息
            update_address_textarea = update_address_div.find_element(By.XPATH,value="//*[@id='app']/div[2]/form/div[3]/div[2]/div/span/textarea")
            update_address_textarea.send_keys('长安大学雁塔校区')
            print('等待提交中......')
            time.sleep(3)
            # 3 提交信息
            submit_btn = driver.find_element(By.XPATH, value='//*[@id="app"]/div[2]/form/div[18]/div/div/span/button')
            submit_state = submit_btn.click()
            print('信息提交成功')
            time.sleep(3)
            recorde_box = driver.find_element(By.XPATH, value='//*[@id="app"]/div/div[2]/div[1]')
            if recorde_box.get_attribute('innerText').__contains__('您今日健康打卡已完成'):
                time.sleep(3)
                driver.close()
                return True
            else:
                print('打卡错误')
                time.sleep(3)
                driver.close()
                return False
        else:
            print('定位更新失败')
            time.sleep(3)
            driver.close()
            return False
    else:
        print('健康打卡界面加载不成功')
        time.sleep(3)
        driver.close()
        return False
# 利用yagmail发送邮件
def sendmail(receiver_mail, contents):
    '''

    :param receiver_mail: 接收者邮箱
    :param contents: 发送内容
    :return:
    '''
    yag = yagmail.SMTP(user=mail_user, password=mail_code, host='smtp.163.com')
    subject = '健康打卡提示'  #邮件主题
    receiver = receiver_mail
    yag.send(receiver, subject, contents)
    yag.close()
    print('发送成功')
def person_punch(username, password, receiver_mail):
    '''
    单人打卡并发送邮箱
    :param username: 接收者学号
    :param password: 接收者密码
    :param receiver_mail: 接收者邮箱
    :return:
    '''
    try:
        isSubmit = person_submit(username=username, password=password)
        if isSubmit:
            print('{}打卡成功'.format(username))
            print('正在发送{}打卡邮件'.format(username))
            sendmail(receiver_mail, contents = '今日健康打卡成功')
        else:
            print('正在发送{}打卡邮件'.format(username))
            sendmail(receiver_mail, contents = '今日健康打卡失败')
    except:
        print('正在发送{}打卡邮件'.format(username))
        sendmail(receiver_mail, contents='出现错误，打卡失败')

def main():
    # 多人打卡
    for username, password, receiver_mail in zip(username_lst, password_lst, receiver_mail_lst):
        print('{}打卡准备中...'.format(username))
        person_punch(username, password, receiver_mail)
        time.sleep(5)
    print('今日打卡人数:',len(username_lst))

main()
