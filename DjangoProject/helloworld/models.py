from django.db import models

# Create your models here.
class StudentInfo(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    age=models.IntegerField()

    class Meta:
        db_table = "t_student"

class BookTypeInfo(models.Model):
    id=models.AutoField(primary_key=True)
    bookTypeName=models.CharField(max_length=20)
    class Meta:
        db_table = "t_bookType"
        verbose_name = "图书类别信息"

    def __str__(self):
        return self.bookTypeName

class BookInfo(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='编号')
    bookName=models.CharField(max_length=20,verbose_name='图书名称')
    price=models.FloatField(verbose_name='价格')
    publishDate=models.DateField(verbose_name='出版日期')
    bookType =models.ForeignKey(BookTypeInfo,on_delete=models.Prefetch,verbose_name='')
    class Meta:
        db_table = "t_book"
        verbose_name = "图书信息"



class AccountInfo(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    account=models.FloatField()
    class Meta:
        db_table = "t_account"
        verbose_name = "用户账号信息"

