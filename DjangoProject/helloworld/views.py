import datetime
import os

from django.core.paginator import Paginator
from django.db import connection, transaction
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.utils.translation.trans_real import translation
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from helloworld.models import StudentInfo, BookInfo, BookTypeInfo, AccountInfo
from helloworld.forms import StudentForm, BookInfoForm, BookInfoModelForm


# Create your views here.
def index(request):
    date = datetime.date.today()
    content_value={"date":date}
    return render(request, 'index2.html',content_value)

def blog(request,id):
    if id==0:
        return redirect("/static/error.html")
    else:
        return HttpResponse("id是"+str(id)+"博客页面")

def blog2(request,year,month,day):
    return HttpResponse(f"{year}年{month}月{day}日")


filepath=r"D:\yfc\Downloads\陈一发儿 - 童话镇.flac"
filepath2=r"D:\yfc\Downloads\1.jpeg"
def download_file1(request):
    file=open(filepath,"rb")
    response = HttpResponse(file, content_type="application/octet-stream")
    response["Content-Disposition"]="attachment;filename=file.flac"
    return response

def download_file2(request):
    file=open(filepath,"rb")
    response = StreamingHttpResponse(file, content_type="application/octet-stream")
    response["Content-Disposition"]="attachment;filename=file.flac"
    return response

def download_file3(request):
    file=open(filepath2,"rb")
    response = FileResponse(file, content_type="application/octet-stream")
    response["Content-Disposition"]="attachment;filename=1.jpeg"
    return response

def to_login(request):
    """
    跳转登录页面
    :param request:
    :return:
    """
    return render(request, 'login.html')

def login(request):
    """
    登录处理
    :param request:
    :return:
    """
    user_name=request.POST.get("user_name")
    user_pwd =request.POST.get("user_pwd")
    if user_name=="yfc" and user_pwd=="666":
        request.session["Currentuser_name"]=user_name
        print("session获取",request.session.get("Currentuser_name"))
        response = render(request,"main.html")
        response.set_cookie("remember_me",True)
        return response
    else:
        context_value = {"error_info":"用户名或者密码错误"}
        return render(request, 'login.html',context=context_value)


def to_upload(request):
    """
    跳转上传文件页面
    :return:
    """
    return render(request, 'upload.html')

def upload_file(request):
    """
    文件上传处理
    :param request:
    :return:
    """
    myFile = request.FILES.get("myfile",None)
    if myFile:
       f = open(os.path.join("D:\\myFile",myFile.name),"wb+")
       #分块写入
       for chunk in myFile.chunks():
           f.write(chunk)
       f.close()
       return HttpResponse("文件上传成功")
    else:
        return HttpResponse("未发现文件")

class List(ListView):
    #设置模板文件
    template_name = "student/list.html"
    #设置模型外数据
    extra_context = {'title':'学生信息列表'}
    #查询结果集
    queryset=StudentInfo.objects.all()
    #每页展示5跳条数据
    paginate_by=5
    #设置上下文对象名称
    context_object_name="student_list"

class Detail(DetailView):
    # 设置模板文件
    template_name = "student/detail.html"
    # 设置模型外数据
    extra_context = {'title': '学生信息详情'}
    #设置查询模型
    model = StudentInfo
    context_object_name = "student"
    pk_url_kwarg = "id"

class Create(CreateView):
    # 设置模板文件
    template_name = "student/create.html"
    # 设置模型外数据
    extra_context = {'title': '学生信息新增'}
    #指定form表单
    form_class = StudentForm
    #执行成功后跳转页面
    success_url = "/student/list"

class Update(UpdateView):
    # 设置模板文件
    template_name = "student/update.html"
    # 设置模型外数据
    extra_context = {'title': '学生信息修改'}
    #设置查询模型
    model = StudentInfo

    form_class = StudentForm

    pk_url_kwarg = "id"

    success_url = "/student/list"

class Delete(DeleteView):
    # 设置模板文件
    template_name = "student/delete.html"
    # 设置模型外数据
    extra_context = {'title': '学生信息删除'}
    # 设置查询模型
    model = StudentInfo

    context_object_name = "student"
    success_url = "/student/list"

    pk_url_kwarg = "id"


def to_course(request):
    """
    跳转课程页面
    :return:
    """
    return render(request, 'course.html')

def bookList(request):
    """
    图书列表查询
    :param request: 
    :return: 
    """
    bookList = BookInfo.objects.all()

    #bookList=BookInfo.objects.extra(where=["price>%s"],params=[200])
    #bookList=BookInfo.objects.raw("select * from t_book where price>%s",params=[200])

    # cursor = connection.cursor()
    # print(type(cursor))
    # cursor.execute("select count(*) from t_book where price>200")
    # print(cursor.fetchone())

    # bookList = BookInfo.objects.all()[:2]
    # bookList=BookInfo.objects.values("bookName","price")
    # d = dict(price=100,id=1)
    # bookList = BookInfo.objects.get(**d)
    #bookList = BookInfo.objects.filter(Q(id=1)|Q(price=88))

    #bookList = BookInfo.objects.filter(~Q(id=1))
    # bookList = BookInfo.objects.exclude(Q(id=1))
    #bookList = BookInfo.objects.order_by('-id')
    #r= BookInfo.objects.values("bookType").annotate(Sum('price'))
    #分页
    # p = Paginator(bookList, 2)
    # bookListPage=p.page(2)
    # print("总记录数:",BookInfo.objects.count())
    #bookList=BookInfo.objects.filter(price__gt=66)
    context_value = {'title':'图书列表','bookList':bookList}
    return  render(request,"book/list.html",context_value)


def bookList2(request):
    """
    多表查询，正向查询和反向查询
    :param request:
    :return:
    """
    #正常查询
    book:BookInfo=BookInfo.objects.filter(id=2).first()
    print(book.bookName,book.bookType.bookTypeName)
    context_value = {'title': '图书列表'}
    return render(request, "book/list.html", context_value)

def preAdd(request):
    """
    预处理，添加操作
    :param request:
    :return:
    """
    bookTypeList = BookTypeInfo.objects.all()
    print(bookTypeList)
    context_value={"title":"图书添加","bookTypeList":bookTypeList}
    return render(request,"book/add.html",context_value)


def add(request):
    """
    图书添加
    :param request:
    :return:
    """
    print(request.POST.get("bookName"))
    print(request.POST.get("price"))
    print(request.POST.get("publishDate"))
    print(request.POST.get("bookType"))
    book=BookInfo()
    book.bookName=request.POST.get("bookName")
    book.price=request.POST.get("price")
    book.publishDate=request.POST.get("publishDate")
    book.bookType_id=request.POST.get("bookType")
    book.save()

    #添加数据后可以获取id
    print("bookId:",book.id)
    return bookList(request)

def preUpdate(request,id):
    """
    预处理，添加操作
    :param request:
    :return:
    """
    print("id:",id)
    book = BookInfo.objects.get(id=id)
    bookTypeList = BookTypeInfo.objects.all()
    print(book.bookName)
    context_value={"title":"图书修改","book":book,"bookTypeList":bookTypeList}
    return render(request,"book/edit.html",context_value)


def update(request):
    """
       图书修改
       :param request:
       :return:
       """
    # print(request.POST.get("bookName"))
    # print(request.POST.get("price"))
    # print(request.POST.get("publishDate"))
    # print(request.POST.get("bookType_id"))
    # print(request.POST.get("id"))
    book = BookInfo()

    print("requestid",request.POST.get("id"))
    book.id=request.POST.get("id")
    print("bookid:",book.id)
    book.bookName = request.POST.get("bookName")
    book.price = request.POST.get("price")
    book.publishDate = request.POST.get("publishDate")
    book.bookType_id = request.POST.get("bookType_id")
    book.save()
    return bookList(request)

def delete(request,id):
    BookInfo.objects.get(id=id).delete()
    return bookList(request)


@transaction.atomic
def transfer(request):
    """
    模拟转账
    :param request:
    :return:
    """
    #开启事务
    sid = transaction.savepoint()
    try:
        a1=AccountInfo.objects.filter(user='张三')
        a1.update(account=F("account")+100)
        a2 = AccountInfo.objects.filter(user='李四')
        a2.update(account=F("account") - 100)
        #提交事务
        transaction.savepoint_commit(sid)
    except Exception as e:
        print("异常信息：",e)
        #事务回滚
        transaction.savepoint_rollback(sid)

    return  HttpResponse("Ok")


def preAdd2(request):
    """
    预处理，添加操作
    :param request:
    :return:
    """
    form=BookInfoForm()
    context_value={"title":"图书添加","form":form}
    return render(request,"book/add2.html",context_value)

def preAdd3(request):
    """
    预处理，添加操作 使用ModelForm表单
    :param request:
    :return:
    """
    form=BookInfoModelForm()
    context_value={"title":"图书添加","form":form}
    return render(request,"book/add2.html",context_value)