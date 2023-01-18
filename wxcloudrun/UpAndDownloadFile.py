import requests
import json
import io
from django.http import JsonResponse
from PIL import Image, ImageDraw
from requests_toolbelt import MultipartEncoder
# from wxcloudrun import cosBuck
from wxcloudrun.uti.cosBuck import CosBuck

def print_func( par ):
   print("Hello : ", par)
   return

def DownLoad(request):
    data = json.loads(request.body)
    UserUpfile = data['UserUpfile']
    Downurls = reSend(UserUpfile)
    img_B = []
    for url in Downurls:
        r = requests.get(url=url)
        img_B.append(r.content)
#返回多张图片的二进制表示列表
    return img_B


def reSend(UserUpfile):
    print('1`')
    print(UserUpfile)
    list1 = []
    urls = []
    for urlDown in UserUpfile:
        one = {"fileid": urlDown,"max_age": 2400}
        list1.append(one)
    print(list1)
    params = {
                "env": "prod-1gozglh32abdf0a5",
                "file_list": list1
            }
    res = requests.post('http://api.weixin.qq.com/tcb/batchdownloadfile',json=params)
    print(type(res))
    if(res.status_code == 200):   
        data = res.json()
        # print(type(data))
        # print(data)
        for Downdfile in data['file_list']:
            urls.append(Downdfile['download_url'])
        print(urls)
        return urls
    
def UpLoad(UpFileObject,userid):
    path = 'UserDownLoadImgs/'+ userid +'.png'
    print('路径：',path)
    param={
        "env": "prod-1gozglh32abdf0a5",
        "path": path
    }
    res = requests.post('http://api.weixin.qq.com/tcb/uploadfile',json=param)
    reData = res.json()
    print(reData)
    print(type(UpFileObject))
    # print(len(UpFileObject))
    m = MultipartEncoder(
    fields={'key': path, 
            # 'Signature1': reData['authorization'],
            # 'x-cos-security-token': reData['token'],
            'x-cos-meta-fileid': reData['cos_file_id'],
            # 'file':UpFileObject
            'file': ('1.jpg', UpFileObject, 'image/png')
            # 'file':  ('1.png', open(UpFileObject, 'rb'), 'image/png')
        }
    )
    headers = {
        'Content-Type': m.content_type,
        'authorization': reData['authorization'],
        'host': 'cos.ap-shanghai.myqcloud.com',
        'x-cos-security-token': reData['token']
    }
    # print(m)
    url = reData['url']
    print(url)
    print(type(m),m.content_type)
    r = requests.post('https://cos.ap-shanghai.myqcloud.com/7072-prod-1gozglh32abdf0a5-1316357380/UserDownLoadImgs/userid.png' ,data = m,headers=headers)
    # r = requests.post(url = url ,data = m)
    if r == None:
        print('ok')
    else:
        print(r.text)




