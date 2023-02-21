from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer): #( 장고 -> 유저 / 유저 -> 장고 ) python -> json / json -> python (이 과정에서 유저가 보낸 데이터를 serializer 에서 유효성 검사를 할 수있다! 대박)

    class Meta:
        model = Category # serializer가 Category model을 위한 serializer를 만들어줌 + 자동적으로 create와 update 메소드를 만들어줌
        fields = ('name', 'kind',)



    # pk = serializers.IntegerField(read_only = True) # 유저가 데이터를 보낼 때 (POST) 작성하지 않아도 되게 만들어주기!
    # name = serializers.CharField(required=True, max_length = 50)
    # kind = serializers.ChoiceField(choices = Category.CategoryKindChoices.choices)
    # created = serializers.DateTimeField(read_only = True) # 유저가 데이터를 보낼 때 (POST) 작성하지 않아도 되게 만들어주기!

    # def create(self, validated_data): # serializer로부터 넘어온 유효성 검증을 통과한 validated_data
    #     return Category.objects.create(**validated_data) # **validated_data -> 자동으로 유저에게 받은 유효한 데이터 넣어줌
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name) # dictionary.get('name', default값) # partial = True 로 해놨기에 값이 없는 것도 있을 수 있으니 default 값으로 미리 설정해두기
    #     instance.kind = validated_data.get('kind', instance.kind)
    #     instance.save()
    #     return instance