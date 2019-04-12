from lxml import html
import requests
import re
import bisect
import time
from bs4 import BeautifulSoup
#禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#function：这个是分割字符串的函数
#allstring: 输入的整条字符串
#start： 输入的开始截取部分的字符串
#end： 输入的结束截取部分的字符串
#return： 返回截取到在中间字符串，如果找不到就返回空字符串
def getMidString(allstring, start, end):
    start_pos = allstring.find(start)
    form_string = ""
    if (start_pos < 0):
        return ""
    form_string = allstring[start_pos + len(start):]
    end_pos = form_string.find(end)
    end_string = ""
    if (end_pos < 0):
        return ""
    result = form_string[0:end_pos]
    return result

#登录获取cookies数据
r1 = requests.get('https://git.colibri.com.cn/users/sign_in',verify = False)
soup = BeautifulSoup(r1.text, features='lxml')  # 生成soup 对象
s1 = soup.find(name='input', attrs={'name': 'authenticity_token'}).get('value')
r1_cookies = r1.cookies.get_dict()  # 下次提交用户名时用的cookie
print(r1_cookies)
print(s1)

# token = s1.find(name='input', attrs={'name': 'authenticity_token'}).get('value')
#登陆用户，注意每种网站登陆，发送的数据格式基本不一样
r2 = requests.post(
    'https://git.colibri.com.cn/users/sign_in',
    data={
        'commit':'Sign in',
        'utf8':'✓',
        'authenticity_token':s1,
        'login':'jdyeSpiderTest',
        'password':'jdyetest123456789'
    },
    cookies=r1.cookies.get_dict(),  # 这里需要第一次的cookie
    verify =False
)
print(r2.cookies.get_dict())  # 这个是成功以后的cookie

projectsNames = []
sshPaths = []

#获取html数据并保存
pagePath = "/jdyeSpiderTest/test"
page = requests.get(
    'https://github.com'+pagePath,  # 查看个人的详情页
    cookies=r2.cookies.get_dict(),
    verify = False
)

element = page.text
print(element)

print("\n####################")
projectName = getMidString(element, "<title>GitHub - ", "</title>")
projectsNames.append(projectName)
print("Project: ", projectName)
ssh_str = getMidString(element, "<div class=\"input-group-button\">\n    <clipboard-copy value=\"", "\" aria-label=")
sshPaths.append(ssh_str)
print("ssh: ", ssh_str)

print("####################\n")

csvFileDate = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())
csvFile = open("GitInfo"+csvFileDate+".csv",'a+')
csvFile.writelines(["Name,","ssh path\n"])

for i in range(0,len(projectsNames)):
    csvFile.write(projectsNames[i]+",")
    csvFile.write(sshPaths[i]+"\n")

csvFile.close()
print("\n******************* Finish ********************\n")

