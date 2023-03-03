from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer

class Wishlists(APIView):

    permission_classes = [IsAuthenticated] # 로그인 된 유저만 permission

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user) # filter 메소드를 사용하여 지금 현재 요청한 유저가 쓴 wishlist만 가져오도록 설정
        serializer = WishlistSerializer(all_wishlists, many=True, context = {"request":request})
        return Response(serializer.data)

    def post(self, request):
        serializer =  WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user,)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WishlistDetail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user): # 기존 detail에서는 self, pk만 받았다면 wishlistdetail에서는 get도 유저 자신의 wishlist만 볼수있어야 하니
                                    # user 인자를 하나 더 받음
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user) # 로그인 확인은 이미 했고 url을 요청한 유저가 wishlist를 작성한 유저만 같은 유저인지
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    

    def delete(self,request,pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, data = request.data, partial = True)
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
