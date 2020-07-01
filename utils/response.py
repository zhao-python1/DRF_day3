from rest_framework.response import Response
class APIResponse(Response):
    def __init__(self, data_status=200,data_message=0,results=None,
                 http_status=None, headers=None,exception=False,**kwargs):
        #定义数据返回的状态
        data={
            "status": data_status,
            "message": data_message
        }


        # 判断results是否有结果
        if results is not None:
            data['results'] = results

        data.update(kwargs)

        # 获取一个response对象  需要将自定义的response响应回去
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)
