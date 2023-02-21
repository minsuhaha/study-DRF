from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    


# class Categories(APIView):
    
#     def get(self, request):
#         category = Category.objects.all()
#         serialzer = CategorySerializer(category, many=True) # CategorySerializer는 하나의 list 데이터만 받을거라 생각했는데 all_categories가 list형태로 무더기 데이터를 보내기때문에 (many=True) 설정을 해줘야함.
#         # all_categories = Category.objects.all() # queryset은 json 형태가 아니여서 json 형태로 변환을 해주어야함!
#         return Response(serialzer.data)

#     def post(self, request):
#         serialzer = CategorySerializer(data = request.data) # 유저가 보낸 데이터를 받아(request.data) 역직렬화!
#         if serialzer.is_valid():
#             new_category = serialzer.save() # serializer.save()를 하면 자동적으로 create 메소드를 찾아 실행 def create 메소드 실행
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serialzer.errors)


# class CategoryDetail(APIView):

#     def get_object(self, pk):
#         try: # pk가 있는 pk -> 정상 작동하면
#             return Category.objects.get(pk = pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         serializer = CategorySerializer(self.get_object(pk)) # 장고의 모델형태를 유저에게 보여주기 직렬화!
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         serializer = CategorySerializer(self.get_object(pk), data = request.data, partial=True) # partial = True -> 여기로 들어오는 데이터가 완벽한 형태이지 않을 수 있다.
#         if serializer.is_valid():
#             updated_category = serializer.save() # update를 자동적으로 실행
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         self.get_object(pk).delete()
#         return Response(status=HTTP_204_NO_CONTENT)




