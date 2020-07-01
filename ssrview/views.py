from django.shortcuts import render
# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets

from utils.response import APIResponse
from .serializers import BookModelSerializer
from rest_framework.views import APIView
from library.models import Book
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin


class BookAPIView(APIView):

    def get(self,request,*args,**kwargs):
        book_id = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_id,many=True).data
        return APIResponse(results=data_ser)



class BookGenericAPIView(ListModelMixin,
                         GenericAPIView,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         RetrieveModelMixin):
#由于GenericAPIView继承了APIView，所以两者可以相互兼容
# 重点分析GenericAPIView
     #提供一个queryset属性
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    # 指定获取单条信息的主键的名称
    lookup_field = "id"

    #通过ListModelMixin完成查询所有数据
    # 通过RetrieveModelMixin完成查询单个数据
    def get(self,request,*args,**kwargs):
        if "id" in kwargs:
            return self.retrieve(request,*args,**kwargs)
        else:
            return self.list(request,*args,**kwargs)

    #新加图书  通过CreateModelMixin,完成单个数据的添加
    def post(self,request,*args,**kwargs):
        response = self.create(request,*args,**kwargs)
        return APIResponse(results=response.data)

     #单个修改
    def put(self,request,*args,**kwargs):
        res = self.update(request,*args,**kwargs)
        return APIResponse(results=res.data)

    #单局修改
    def patch(self,request,*args,**kwargs):
        res = self.partial_update(request,*args,**kwargs)
        return APIResponse(results=res.data)

    # 通过继承DestroyModelMixin 获取self
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return APIResponse(http_status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"
    #注册逻辑
    #新加图书  通过CreateModelMixin,完成单个数据的添加
    def register(self,request,*args,**kwargs):
        response = self.create(request,*args,**kwargs)
        return APIResponse(results=response.data)

class BookGenericsViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"
    #怎样确定post请求是需要登录的
    def login(self,request,*args,**kwargs):
        #在这个方法中完整登录的逻辑
         return self.retrieve(request,*args,**kwargs)
    def get_count(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)




    # def get(self,request,*args,**kwargs):
    #     return self.list(request,*args,**kwargs)

    # def list(self,request,*args,**kwargs):
    #     # 获取所有的数据对象
    #     # book_list = Book.objects.filter(is_delete=False)
    #     book_list = self.get_queryset()
    #     # 获取序列化器
    #     data_ser = self.get_serializer(book_list, many=True)
    #     data = data_ser.data
    #     return APIResponse(results=data)


    # def get(self,request,*args,**kwargs):
    #     book_obj = self.get_object()
    #     data_ser = self.get_serializer(book_obj)
    #     data = data_ser.data
    #     return APIResponse(results=data)