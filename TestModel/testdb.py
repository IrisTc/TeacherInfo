from TestModel.models import Connect
import json
import requests
import urllib
from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render

def get_id(record_name): 
    base_api = r'https://cloud.minapp.com/oserve/v1/table/%s/record/' % Connect.table_id
    headers = {
        'Authorization': 'Bearer %s' % Connect.token,
    }
    where_ = {
            'name': {'$eq': record_name},
        }
    query_ = urllib.parse.urlencode({
            'where': json.dumps(where_),
            'order_by': '-created_at',
            'limit': 1,
            'offset': 0,
        })
    api = '?'.join((base_api, query_))

    resp_ = requests.get(api, headers=headers)
    resp_object = json.loads(resp_.content)
    objects = resp_object["objects"][0]
    global _college, _name, _title
    _college = objects['college']
    _name = objects['name']
    _title = objects['title']
    return objects['id']

def deleteTeacher(request):
    record_name  =  request.GET['name']  
    try:
        record_id = get_id(record_name)
        base_api = 'https://cloud.minapp.com/oserve/v1/table/{0}/record/{1}/'.format(Connect.table_id, record_id)
        headers = {
            'Authorization': 'Bearer %s' % Connect.token,
            'Content-Type': 'application/json',
            'charset' : 'utf-8'
        }
    except  IndexError:
        back = '查无此人！'
        return HttpResponse(back)
    else:
        response = requests.delete(url=base_api, headers=headers)
        back = '删除成功!<br> 姓名：{0}<br> 学校：{1}<br> 职称：{2}'.format(_name, _college, _title)
        return HttpResponse(back)

def getSomeTeacher(request):
    record_college = request.GET['college']
    record_title = request.GET['title']
    base_api = r'https://cloud.minapp.com/oserve/v1/table/%s/record/' % Connect.table_id
    headers = {
        'Authorization': 'Bearer %s' % Connect.token,
    }
    where_ = {
            'college': {'$eq': record_college},
            'title': {'$eq': record_title},
        }
    query_ = urllib.parse.urlencode({
            'where': json.dumps(where_),
            'order_by': '-created_at',
            'offset': 0,
        })
    api = '?'.join((base_api, query_))
    resp_ = requests.get(api, headers=headers)
    
    content = json.loads(resp_.content)
    num = len(content['objects'])
    if(num==0):
        evaluation = '无该学院或无该职称'
    elif(num>5):
        evaluation = 'A'
    elif(num>3):
        evaluation = 'B'
    else:
        evaluation = 'C'
    context = {'content': content['objects'], 'evaluation': evaluation}
    return render(request,'view.html', context)