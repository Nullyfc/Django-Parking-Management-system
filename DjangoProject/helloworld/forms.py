from django import forms
from django.forms import ModelForm, Form

from helloworld.models import StudentInfo, BookTypeInfo, BookInfo


class StudentForm(ModelForm):
    class Meta: #配置中心
        model = StudentInfo
        fields = ['name','age']

        widgets = {
            'name':forms.TextInput(attrs={'id':'name','class':'inputClass'}),
        }
        labels = {  #指定标签名称
            "name":"姓名",
            "age":"年龄"
        }

class BookInfoModelForm(ModelForm):
    class Meta: #配置中心
        model = BookInfo
        fields='__all__'

        widgets = {
            'bookName':forms.TextInput(attrs={'id':'bookName','class':'inputClass','placeholder':'请输入图书名称'}),
        }
        labels = {  #指定标签名称
            "bookName":"图书名称",
            "price":"价格",
            "publishDate":"出版日期",
            "bookType":"图书类型",

        }
        help_texts = {
            "bookName":"请输入图书名称"
        }


class BookInfoForm(Form):
    """
    图书表单
    """
    bookName = forms.CharField(
        max_length=20,
        label="图书名称",
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'请输入图书名称','class':'inputClass'}),
    )
    price= forms.FloatField(label="图书价格")
    publishDate= forms.DateField(label="出版日期")
    #获取图书类别列表
    bookTypeList=BookTypeInfo.objects.values()
    print(bookTypeList)
    choices=[(v['id'],v['bookTypeName']) for v , v in enumerate(bookTypeList)]
    bookType_id  = forms.ChoiceField(choices=choices,label="图书类别")


