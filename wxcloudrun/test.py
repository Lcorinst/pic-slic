import requests
import json
import io
from django.http import JsonResponse

from wxcloudrun.uti.cosBuck import CosBuck



def cos_test(request,_):
    cos = CosBuck()
    auth = cos.get_Auth()
    print('请求授权参数：', auth)
    ##初始化
    client = cos.cos_Init(auth)
    respon = client.list_buckets()

    print(respon)

    return JsonResponse({'code': 0, 'data': '方法：cos_test'},
                        json_dumps_params={'ensure_ascii': False})