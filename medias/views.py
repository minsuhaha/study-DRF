from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly #(인증 받았거나 혹은 읽기 전용)
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo

class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated] # 로그인 되어 있는지 확인 하는 permission

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
        
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (photo.experience and photo.experience.host != request.user):
            raise PermissionDenied
        # false일 경우
        photo.delete()
        return Response(status=HTTP_200_OK)