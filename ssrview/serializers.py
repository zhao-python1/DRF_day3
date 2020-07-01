from rest_framework import serializers, exceptions

from library.models import Book


class BookListSerializer(serializers.ListSerializer):
    # 使用此序列化器完成修改多个对象
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            # 每遍历一次 就修改一个对象的数据
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields应该填写哪些字段  应该填写序列化与反序列化字段的并集
        fields = ('book_name','price','pic','publish')
        # fields = ("book_name", "price", "publish", "authors", "pic")
        # 为修改多个图书对象提供ListSerializer
        # list_serializer_class = BookListSerializer
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "不够长，最小是三个~"
                }
            },
            # 在参与只写
            "publish":{
                "write_only":True
            },
            # 在参与只读
            "authors":{
                "read_only":True
            },
            "pic":{
                "read_only":True
            }
        }
    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "色" in value:
            raise serializers.ValidationError("图书名含有敏感字")
            # 可以通过context 获取到viw传递过来的request对象
        request = self.context.get("request")
        print(request)
        return value

    # 全局校验钩子  可以通过attrs获取到前台发送的所有的参数
    def validate(self, attrs):
        price = attrs.get("price", 0)
        # 没有获取到 price  所以是 NoneType
        if price > 80:
            raise serializers.ValidationError("超钱了")
        return attrs








