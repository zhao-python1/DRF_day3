from rest_framework import serializers, exceptions

from library.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
#     '''
#     出版社的序列化器
#     '''
    class Meta:
        model = Press
        fields = ('press_name','address','pic')


class BookModelSerializer(serializers.ModelSerializer):

#序列化器
    # TODO 自定义连表查询  查询图书时将图书对应的出版的信息完整的查询出来
    #一个嵌套另一个序列化器连接较多的字段时使用
    #    # 需要与图书表的中外键名保持一致  在连表查询较多字段时推荐使用
    publish = PressModelSerializer()

    class Meta:
        #不需要指定序列化哪个模型
        model = Book

        #z自定序列的字段
        # fields = ('book_name','price','pic','publish_name','author_li')
        fields = ('book_name','price','pic','publish')

        #查所有字段
        # fields = "__all__"

        # #不展示字段
        # exclude = ('is_delete','status')

        # #指定查询的深度  关联对想对像查询
        # depth = 1


class BookDeModelSerializer(serializers.ModelSerializer):
    '''4反序列化器，数据库使用'''
    class Meta:
        model = Book
        fields = ('book_name','price','publish','authors')

        # 添加DRF所提供的校验规
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短啦~"
                }
            },
            "price": {
                "max_digits": 5,
                "decimal_places": 4,
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "色" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
            # 可以通过context 获取到viw传递过来的request对象
        request = self.context.get("request")
        print(request)
        return value

    # 全局校验钩子  可以通过attrs获取到前台发送的所有的参数
    def validate(self, attrs):
        price = attrs.get("price", 0)
        # 没有获取到 price  所以是 NoneType
        if price > 80:
            raise exceptions.ValidationError("超钱了")
        return attrs

# ListSerializer序列化器在定义完后需要使用才生效
class BookListSerializer(serializers.ListSerializer):
    # 使用此序列化器完成修改多个对象
    def update(self, instance, validated_data):
        # print(type(self))  # 当前调用序列化器类
        # print(instance)  # 要修改的对象
        # print(validated_data)   # 要修改的数据
        # print(type(self.child))

        # TODO 将群改 改变成一次改一个  遍历修改
        for index, obj in enumerate(instance):
            # 每遍历一次 就修改一个对象的数据
            self.child.update(obj, validated_data[index])

        return instance

class BookModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields应该填写哪些字段  应该填写序列化与反序列化字段的并集
        fields = ('book_name','price','pic','publish')
        # fields = ("book_name", "price", "publish", "authors", "pic")
        # 为修改多个图书对象提供ListSerializer
        list_serializer_class = BookListSerializer
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "不够长，最小是三个~"
                }
            },
            #在参与只写
            # "publish":{
            #     "write_only":True
            # },
            # # 在参与只读
            # "authors":{
            #     "read_only":True
            # },
            # "pic":{
            #     "read_only":True
            # }
        }











