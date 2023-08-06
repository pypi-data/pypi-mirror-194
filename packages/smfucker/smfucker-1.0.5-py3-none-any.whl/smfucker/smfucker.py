from smfucker import smms as sm
import argparse
import getpass
import configparser
from prettytable import PrettyTable
import os
import re

smms=sm.SMMS()
inifilename = "config.ini"

def HistoryTablePrint(data):
    field_names = ["id","filename", "url", "hash", "created_at"]
    x = PrettyTable(field_names)
    x.title = 'SM.MS History'
    num=0
    for row in data:
        x.add_row([num,row['filename'],row['url'],row['hash'],row['created_at']])
        num+=1
    print(x)

def UploadTablePrint(data):
    field_names = ["id","name", "url", "state"]
    x = PrettyTable(field_names)
    x.title = 'SM.MS Upload'
    num = 0
    for row in data:
        x.add_row([num,row['name'],row['url'],row['state']])
        num += 1
    print(x)

def getallpic():
    all_data=[]
    pages=smms.get_TotalPages()
    for i in range(0,pages+1):
        data_boby=smms.view_upload_history(i)
        all_data+=data_boby
    final_data = sorted(all_data, key=lambda k: k.get('created_at'), reverse=True)
    #all_data.sort(key=lambda k: k.get('created_at'), reverse=True)  # 此处使用sort以复习和sorted的区别
    return final_data

def namesearch(data,name):
    resluit=list(filter(lambda item: item['filename'][0:len(name)] == name, data))
    HistoryTablePrint(resluit)

def datesearch(data,date):
    resluit=list(filter(lambda item: item['created_at'][0:10] == date, data))
    HistoryTablePrint(resluit)

def uploadOnepic(path):
    upload_pic_msg = []
    url=None
    if os.path.exists(path):
        url=smms.upload_image(path)
    else:
        print("no such file")
    one_pic_msg = {'name': None, 'url': None, 'state': None}
    pic_name=None
    if '\\' in path:  # 获取插入图片时 md 中图片的名
        pic_name = path.split('\\')[-1]
    elif '\\\\' in path:
        pic_name = path.split('\\\\')[-1]
    elif '/' in path:
        pic_name = path.split('/')[-1]
    elif '//' in path:
        pic_name = path.split('//')[-1]
    if url!=None:
        state='Success'
    else:
        state = 'False'
    one_pic_msg['name'] = pic_name
    one_pic_msg['url'] = url
    one_pic_msg['state'] = state
    upload_pic_msg.append(one_pic_msg)
    UploadTablePrint(upload_pic_msg)
def deleteOnepic(hash):
    res=smms.delete_image(hash)
    print(res)

def mduploadpic(mdpath):
    sm_link=''
    upload_pic_msg=[]
    with open(mdpath, 'r', encoding='utf-8') as md:
        text=md.read()
        all_pic=re.findall(r'\!\[.*?\)',text)
        for i in range(len((all_pic))):
            one_pic_msg={'name':None,'url':None ,'state':None}
            state='False'
            sm_link=None
            pic_origin_md_url = re.findall(r'\((.*?)\)', all_pic[i])[0]   #取得括号中的绝对地址或者相对地址
            if '\\' in pic_origin_md_url:   # 获取插入图片时 md 中图片的名
                pic_name = pic_origin_md_url.split('\\')[-1]
            elif '\\\\' in pic_origin_md_url:
                pic_name = pic_origin_md_url.split('\\\\')[-1]
            elif '/' in pic_origin_md_url:
                pic_name = pic_origin_md_url.split('/')[-1]
            elif '//' in pic_origin_md_url:
                pic_name = pic_origin_md_url.split('//')[-1]
            if os.path.exists(pic_origin_md_url):
                sm_link=smms.upload_image(pic_origin_md_url)
                state='Success'
            else:
                state='False'
            new_link='![{0}]({1})'.format(pic_name,sm_link)
            text=text.replace(all_pic[i],new_link)
            one_pic_msg['name']=pic_name
            one_pic_msg['url']=sm_link
            one_pic_msg['state'] = state
            upload_pic_msg.append(one_pic_msg)
    pwd=os.getcwd()
    new_filepath=pwd+r'\new.md'
    with open(new_filepath, 'w', encoding='utf-8') as md:
        md.write(text)
        print("job done")
    UploadTablePrint(upload_pic_msg)

def getprofile():
    res=smms.get_user_profile()
    if res["success"]==True:
        data=res['data']
        field_names = ["id", "project", "value"]
        x = PrettyTable(field_names)
        x.title = 'SM.MS User Profile'
        x.add_row([0,"username",data["username"]])
        x.add_row([1, "role", data["role"]])
        x.add_row([2, "email", data["email"]])
        x.add_row([3, "disk_usage", data["disk_usage"]])
        x.add_row([4, "disk_limit", data["disk_limit"]])
        print(x)
    else:
        print(res['message'])

def login():
    name=input("please input your user name:")
    password= getpass.getpass("please input your password:")

    smms.get_api_token(name,password)
    #print(smms.token)

    if smms.token!=None:
        config = configparser.ConfigParser()
        config.read(inifilename)
        if config.has_section("login")==False:
            config.add_section("login")
        config.set('login', 'username', name)
        #config.set('login', 'password', password)
        config.set('login', 'token', smms.token)
        config.write(open(inifilename, 'w'))

def checkToken():
    config = configparser.ConfigParser()
    config.read(inifilename)

    if config.has_section("login")==True:
        try:
            token=config.get('login','token')
            smms.token=token
            smms.headers = {'Authorization': token}
        except configparser.NoOptionError:
            print("no available token,please login")
            login()
    else:
        login()


def test():
    a=1
    # if filename!=None:
    #     mduploadpic(filename)

    #HistoryTablePrint(getallpic())
    #search(getallpic(),'2022-08-10',None)
    #mduploadpic(r'D:\learning record\学术报告\SMMS\examples\test.md')



    #smms.view_upload_history(0)
    #uploadOnepic(r"D:\learning record\学术报告\SMMS\examples\pic\Snipaste_2023-02-14_10-21-40.png")

# 按间距中的绿色按钮以运行脚本。
def exe_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',  help='Point to a md file')
    parser.add_argument('--history', help='look all history', action="store_true")
    parser.add_argument('-d', '--date', help='search by date')
    parser.add_argument('-n', '--name', help='search by name')
    parser.add_argument('--upload', help='upload by file path')
    parser.add_argument('--delete', help='delete by hash')
    parser.add_argument('-l', '--login', help='login',action="store_true")
    parser.add_argument('--user', help='get user profile', action="store_true")
    parser.add_argument('-v','--version',action="store_true")
    args = parser.parse_args()

    if args.login:
        login()
    if args.file!=None:
        checkToken()
        mduploadpic(args.file)
    if args.date!=None and args.history:
        checkToken()
        datesearch(getallpic(),args.date)
    if args.name != None and args.history:
        checkToken()
        namesearch(getallpic(),args.name)
    if args.history and args.date==None and args.name==None:
        checkToken()
        HistoryTablePrint(getallpic())
    if args.upload:
        checkToken()
        uploadOnepic(args.upload)
    if args.delete:
        checkToken()
        deleteOnepic(args.delete)
    if args.user:
        checkToken()
        getprofile()
    if args.version:
        print("smfucker version 1.0.0")

if __name__ == '__main__':
    exe_main()