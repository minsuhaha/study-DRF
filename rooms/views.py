from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer

# 모든 view function은 request를 받는다는것을 꼭 생각하고 있을 것!
class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save() # 자동으로 create 메소드 실행됨
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)

class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    # put(update)는 AmenitySerializer에 두 개의 데이터 필요 (1.업데이트하고 싶은 amenity, 2.사용자가 보낸 수정데이터)
    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity,data=request.data, partial=True) # partial = True 부분적으로 수정가능하도록!
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)


    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # 로그인 한 유저만 post를 가능하게 하기 위해서
        if request.user.is_authenticated: # 요청한 user가 로그인이 되어있는 상태인지 반대는 is_anonymous (로그아웃 상태인지)
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get('category') 
                if not category_pk: # category를 입력받지 못했을때
                    raise ParseError("Category is required!") # 400 bad request error
                try: 
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES: # 카테고리가 ROOMS이 아닌 EXPERIENCES이면
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist: # category가 기존에 없는 카테고리로 입력받는다면
                    raise ParseError("Category not found")
                try: 
                    with transaction.atomic(): # 장고 DB에 즉시 반영 X (에러가 하나라도 있으면 DB에 반영 X)
                        room = serializer.save(owner=request.user, category=category) # owner=request.user는 자동으로 validated_data에 추가됨.
                        amenities = request.data.get('amenities')
                        for amenity_pk in amenities: # amenity 제대로 작성되었는지 확인차
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity) # manytomany 관계이기 때문에 add ,remove 가능!    
                        return Response(RoomDetailSerializer(room).data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
        
class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound
        
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated: # 유저가 로그인 된 유저인지
            raise NotAuthenticated
        if room.owner != request.user: # 방의 주인과 로그인 한 유저가 같은 사람인지 아닌지
            raise PermissionDenied
        
        serializer = RoomDetailSerializer(room, data=request.data, partial = True)
        
        # foreign key로 연결되어 있는 부분은 제한이 있기에 설정
        if serializer.is_valid():
            if 'category' in request.data:
                category_pk = request.data.get('category')
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'room'")
                except Category.DoesNotExist:
                    raise ParseError("category not found")
                
                try:
                    with transaction.atomic(): # 중간에 하나라도 오류가 있으면 db에 저장이 안됨
                        updated_room = serializer.save(owner=request.user, category=category) # update 메소드 실행됨.
                        if 'amenities' in request.data:
                            amenities = request.data.get('amenities')
                            updated_room.amenities.clear() # amenities를 수정하기 위해서 어차피 amenities 데이터를 받기 때문에 초기화해주고 시작.
                            for amenity_pk in amenities:
                                amenity = Amenity.objects.get(pk=amenity_pk)
                                updated_room.amenities.add(amenity) # manytomany 관계이기 때문에 add 메소드?함수? 가능.
                                serializer = RoomDetailSerializer(updated_room)
                        return Response(serializer.data)
                except Exception:
                    return ParseError("Can't update room")
        else:
            return Response(serializer.errors)

        #  여기 들어갈 코드를 작성하기 (hint : Post 했던 부분 참고해서 작성해보기!) # 

    # 방 주인과 로그인 한 유저가 같을 경우에만 삭제가능.
    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated: # 요청한 유저가 로그인 된 유저인지
            raise NotAuthenticated
        if room.owner != request.user: # 방의 주인과 로그인 한 유저가 같은 사람인지 아닌지
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound 
           
    def get(self, request, pk):
        # page
        page = request.query_params.get("page", 1)
        page = int(page) # 계산을 위해 정수형으로 형변환.
        page_size = 1 # 한 페이지당 크기
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end], 
            many=True)
        return Response(serializer.data)