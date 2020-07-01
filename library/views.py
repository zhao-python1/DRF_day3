from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response import APIResponse
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
            # return Response({
            #     "status": status.HTTP_200_OK,
            #     "message": "查询单个图书成功",
            #     "results": book_ser
            # })
            return APIResponse(results=book_ser)
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializer2(book_list, many=True).data
            # return Response({
            #     "status": status.HTTP_200_OK,
            #     "message": "查询所有图书成功",
            #     "results": book_list_ser
            # })
            return APIResponse(100,"查询已经成功了",results=book_list_ser)

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
        book_ser = BookModelSerializer2(data=request_data,many=many,context={"request":request})
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


    # def patch(self, request, *args, **kwargs):
    #     """
    #     修改一部分
    #     """
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "图书不存在"
    #         })
    #     #修改局部则需要修改partial
    #     book_ser = BookModelSerializer2(data=request_data, instance=book_obj, partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #
    #     book_ser.save()
    #
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "更新成功",
    #         "results": BookModelSerializer2(book_obj).data
    #     })
    # def patch(self,request,*args,**kwargs):
    #     '''
    #     单个修改: pk 传递要修改的内容  1{boo_name:php}
    #     局部修改多个与整天修改多个多id 多 request.data
    #     前端发送的数据要有一定的格式
    #     [{pk:1,book_name:python},{pk:2,publish:2},{pk:3,price:88.11}]
    #     '''
    #     request_data= request.data
    #     book_id = kwargs.get("id")
    #     #
    #     # #id存在传递的是字典，修改一个，也相当于群该一个
    #     if book_id and isinstance(request_data,dict):
    #         book_ids = [book_id,]
    #         request_data = [request_data]
    #     #
    #     #     #如果不存在则显示的是列表，修改一个
    #     elif not book_id and isinstance(request_data,list):
    #         book_ids = []
    #     #     #要修改的图示id取出来放进book_ids里面
    #         for dic in request_data:
    #             pk = dic.pop("pk", None)
    #             if pk:
    #                 book_ids.append(pk)
    #             else:
    #                 return Response({
    #                     "status": status.HTTP_400_BAD_REQUEST,
    #                     "message": "PK不存在",
    #                 })
    #     else:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "数据格式有误",
    #         })
    #     print(request_data)
    #     print(book_ids)
    #     #
    #     # #对传递过来的id与 request_data 进行筛选id对应的图书是否存在
    #     # #id对应的图书不存在，移除id，id对应的request_data也要移除  如果存在 则查询出对应的图书进行修改
    #     book_list = []  #要修改的图数是对象
    #     new_data = []  #所有的要修改的的参数
    #     # #禁止再循环中对列表长度进行改变
    #     for index, pk in enumerate(book_ids):
    #         try:
    #             book_obj = Book.objects.get(pk=pk)
    #             book_list.append(book_obj)
    #             new_data.append(request_data[index])
    #         except:
    #     #         #图是不存在，移除id和对应的数据
    #                continue
    #
    #     book_ser = BookModelSerializer2(data=new_data, instance=book_list, partial=True, many=True)
    #     book_ser.is_valid(raise_exception=True)
    #     book_ser.save()
    #
    #     return Response({
    #         "status": status.HTTP_200_OK,
    #         "message": "修改成功",
    #     })

    def patch(self, request, *args, **kwargs):
        """
        单个修改： pk  传递要修改的内容    1  {book_name: php}
        局部修改多个与整体修改多个: 多个id   多个  request.data
        id:[1,2,3]  request.data:[{},{},{}]   如何确定要修改的id与值的对应关系
        要求前端发送过来的数据按照一定的格式
        [{pk:1,book_name: python},{pk:2,publish:2},{pk:3,price:88.88}]
        """
        request_data = request.data
        book_id = kwargs.get("id")

        # 如果id存在且传递的参数是字典   单个修改  修改单个  群改一个
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]
            request_data = [request_data]

        # 如果id不存在且参数是列表 修改多个
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            # 将要修改的图书的id取出放进 book_ids中
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在",
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "数据格式有误",
            })

        # print(request_data)
        # print(book_ids)

        # TODO  需要对传递过来的id与 request_data 进行筛选  id对应的图书是否存在
        # TODO 如果id对应的图书不存在  移除id  id对应的request_data也要移除  如果存在 则查询出对应的图书进行修改
        book_list = []  # 所有要修改的图书对象
        new_data = []  # 所有要修改的参数
        # TODO 禁止在循环中对列表的长度做改变
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
                # print(request_data[index])
            except:
                # 如果图书对象不存在  则将id与对应数据都移除
                # index = book_ids.index(pk)
                # request_data.pop(index)
                continue

        book_ser = BookModelSerializer2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        })




'''
查单个，查多个，添加单个，添加多个，
局部修改单个，局部修改多个，删除单个，删除多个，
整体修改单个，整体修改多个
'''



