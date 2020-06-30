from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookModelSerializer, BookDeModelSerializer, BookModelSerializer2

from library.models import Book


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_a = Book.objects.get(pk=book_id)
            book_zhi = BookModelSerializer(book_a).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_zhi
            })

        else:
            book_b = Book.objects.all()
            book_b_ser = BookModelSerializer(book_b,many=True).data
            return Response({
                "status":status.HTTP_200_OK,
                "message":"查询所有图书成功",
                "results":book_b_ser
            })
    def post(self,request,*args,**kwargs):
        '''
        单个添加
        '''
        request_data = request.data
        # 前台发送过来的数据交给反序列化器进行校验
        book_ser = BookDeModelSerializer(data=request_data)
        # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            "result": BookModelSerializer(book_obj).data
        })


class BookAPIView2(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
            book_ser = BookModelSerializer2(book_obj).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializer2(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self,request,*args,**kwargs):
        '''
        单个添加  传递字典
        多个添加  给个列表[{},{}]
        '''
        request_data = request.data
        if isinstance(request_data,dict): #代表增加的是单个对象
            # 将前端发送过来的数据交给反序列化器进行校验
            many = False
        elif isinstance(request_data,list): #加多个图书
            many = True
        else:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "添加图书有误",
            })

        # 前台发送过来的数据交给反序列化器进行校验
        book_ser = BookModelSerializer2(data=request_data,many=many)
        # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            # 当群增多个时，无法序列化多个对象到前台  所以报错
            "result": BookModelSerializer2(book_obj,many=many).data
        })

    def delete(self,request,*args,**kwargs):
        '''
        删除单个  通过urls 的传递id 2/books/1
        删除多个 有多个id{ids:[1,2,3]}
        '''
        book_id = kwargs.get('id')
        if book_id:
            #删除单个
            ids = [book_id]
        else:
           # 删除多个
            ids = request.data.get("ids")
            #判断传递过啊里爱的图书是否在数据库  并且未删除
        response = Book.objects.filter(pk_in=ids,is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败，图书不存在"
        })

    def put(self, request, *args, **kwargs):
        """
        整体修改单个： 修改一个对象的全部字段
        """
        # 修改的参数
        request_data = request.data
        # 要修改的图书的id
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        book_ser = BookModelSerializer2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)

        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializer2(book_obj).data
        })


    def patch(self, request, *args, **kwargs):
        """
        修改一部分
        """
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        #修改局部则需要修改partial
        book_ser = BookModelSerializer2(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)

        book_ser.save()

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializer2(book_obj).data
        })

'''
查单个，查多个，添加单个，添加多个，
局部修改单个，局部修改多个，删除单个，删除多个，
整体修改单个，整体修改多个
'''



