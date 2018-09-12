from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from CMDB import models
import json
import hashlib
def CMDBIndex(request):
    return HttpResponse('<h2>The CMDB Index!</h2>')

def login(request):
    error_msg = ""  #默认错误提示信息为空
    if request.method == 'POST': #当用户以POST方式提交数据时进行指定操作
        user_name = request.POST.get('user_name', None)
        #获取用户输入的数据，根据name属性的值，可以用索引的方式获取，但最好用get方法获取，并将默认值设置为None，避免找不到该索引而报错
        password = request.POST.get('password', None)
        if user_name == 'downtiser' and password == '123123': #判断用户输入是否正确
            return redirect('/host_manager')
            #redirect会将用户界面重定向到指定url,要先导入redirct:
        else:
            error_msg = "用户名或密码错误!"
            #如果验证失败，则将错误提示信息赋值
    return render(request,'login.html', {'Error_msg':error_msg})
    # 第三个参数就是用于替换指定模板中的{{ xxx }}的，将模板中的{{ Error_msg }}替换为指定错误信息error_msg
# user_list = [{'user_name': 'downtiser', 'gender': 'male', 'email': '123@163.com'},]
# def background(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('user_name', None)
#         gender = request.POST.get('gender', None)
#         email = request.POST.get('email', None)
#         new_dict = {'user_name': user_name, 'gender': gender, 'email': email}
#         user_list.append(new_dict)
#
#     return render(request, 'background.html', {'user_list': user_list})

def host_manager(request):
    respond = {
        'statue': True,
        'error_msg': None
    }
    try:
        if request.method == 'POST':
            region = request.POST.get('region', None)
            host_name = request.POST.get('host_name', None)
            host_ip = request.POST.get('host_ip', None)
            host_port = request.POST.get('host_port', None)
            statue = request.POST.get('statue', None)
            os = request.POST.get('os', None)
            user_name = request.POST.get('user_name', None)
            password = request.POST.get('password', None)
            if not host_name or len(host_name) < 5:
                respond['statue'] = False
                respond['error_msg'] = 'Invalid input'
                return HttpResponse(json.dumps(respond))
            models.UserInfo.objects.create(user_name=user_name, password=password)
            user_obj = models.UserInfo.objects.filter(user_name=user_name).first()
            user_id = user_obj.uid
            models.HostInfo.objects.create(region=region,
                                           host_name=host_name,
                                           host_ip=host_ip,
                                           host_port=host_port,
                                           statue=statue,
                                           os=os,
                                           user_info_id=user_id
                                           )

            return HttpResponse(json.dumps(respond))
    except Exception:
        respond['statue'] = False
        respond['error_msg'] = 'server abnormal'
        return HttpResponse(json.dumps(respond))
    host_info_list = []
    host_list = models.HostInfo.objects.all()
    for host in host_list:
        nid = host.nid
        region = host.region
        host_name = host.host_name
        host_ip = host.host_ip
        host_port = host.host_port
        host_dict = {
            'nid': nid,
            'region': region,
            'host_name': host_name,
            'host_ip': host_ip,
            'host_port': host_port
        }
        host_info_list.append(host_dict)
    print(host_info_list)
    return render(request, 'hostManager.html', {'host_list':host_info_list})


def del_host(request):
    nid = int(request.POST.get('nid'))
    del_host = models.HostInfo.objects.filter(nid=nid).first()
    user_name = del_host.user_info.user_name
    models.HostInfo.objects.filter(nid=nid).delete()
    models.UserInfo.objects.filter(user_name=user_name).delete()
    return redirect('/host_manager')

def detail(request):
    respond = {
        'statue': True,
        'error_msg': None
    }
    try:
        if request.method == 'POST':
            nid = request.POST.get('nid', None)
            region = request.POST.get('region', None)
            host_name = request.POST.get('host_name', None)
            host_ip = request.POST.get('host_ip', None)
            host_port = request.POST.get('host_port', None)
            statue = request.POST.get('statue', None)
            os = request.POST.get('os', None)
            if not host_name or len(host_name) < 5:
                respond['statue'] = False
                respond['error_msg'] = 'Invalid input'
                return HttpResponse(json.dumps(respond))
            models.HostInfo.objects.filter(nid=nid).update(
                region=region,
                host_name=host_name,
                host_ip=host_ip,
                host_port=host_port,
                statue=statue,
                os=os
            )
            return HttpResponse(json.dumps(respond))
    except Exception:
        respond['statue'] = False
        respond['error_msg'] = 'server abnormal'
        return HttpResponse(json.dumps(respond))
    nid = request.GET.get('nid', None)
    host = models.HostInfo.objects.filter(nid=nid).first()
    host_name = host.host_name
    region = host.region
    host_ip = host.host_ip
    host_port = host.host_port
    statue = host.statue
    os = host.os
    user_name = host.user_info.user_name
    password = host.user_info.password
    encrypt = hashlib.md5()
    encrypt.update(password.encode())
    password = encrypt.hexdigest()
    host_dict = {
        'nid': nid,
        'host_name': host_name,
        'region': region,
        'host_ip': host_ip,
        'host_port': host_port,
        'statue': statue,
        'os': os,
        'user_name': user_name,
        'password': password
    }
    return render(request, 'detail.html', {'host_dict': host_dict})

def applications(request):
    if request.method == 'POST':
        app_caption = request.POST.get('app_caption')
        host_id_list = request.POST.getlist('host_select')
        added_app = models.Applications.objects.create(caption=app_caption)
        added_app.host.add(*host_id_list)
        return redirect('/applications')
    elif request.method == 'GET':
        application_list = models.Applications.objects.all()
        host_list = models.HostInfo.objects.all()
        return render(request, 'applications.html', {'app_list': application_list, 'host_list': host_list})

def delete_app(request):
    response = {
        'statue': True,
        'error_msg': None
    }
    try:
        aid = request.POST.get('app_id')
        app = models.Applications.objects.get(aid=aid)
        app.host.clear()
        app.delete()
        return HttpResponse(json.dumps(response))
    except Exception:
        response['statue'] = False
        response['error_msg'] = 'server abnormal!'
        return HttpResponse(json.dumps(response))

def edit_app(request):
    response = {
        'statue': True,
        'error_msg': None
    }
    try:
        aid = request.POST.get('aid')
        caption = request.POST.get('caption')
        select_host = json.loads(request.POST.get('select_host'))
        app = models.Applications.objects.get(aid=aid)
        app.caption = caption
        app.host.set(select_host)
        app.save()
        return HttpResponse(json.dumps(response))
    except Exception:
        response['statue'] = False
        response['error_msg'] = 'server abnormal!'
        return HttpResponse(json.dumps(response))