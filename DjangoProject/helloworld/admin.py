from django.contrib import admin

from helloworld.models import BookTypeInfo, BookInfo

# Register your models here.
#方法一：将模型直接注册到admin后台
admin.site.register(BookTypeInfo)
#方法二：自定义类,继承ModelAdmin,已BookInfo为例子
@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    #设置显示资源
    list_display = ['id','bookName','price','publishDate','bookType']
    search_fields =['bookName','publishDate']
    #重写方法，设置只读字段
    def get_readonly_fields(self, request, obj = None):
        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ['bookName']
        return self.readonly_fields


admin.site.site_title = "后台管理"
admin.site.index_title = "图书管理系统"
admin.site.site_header = "网站管理系统"