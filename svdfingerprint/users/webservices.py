import json
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from .models import UploadImage
from .serialziers import ImageSerializer

class ImageViewSet(ListAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = UploadImage.objects.create(image=file)

        return HttpResponse(
            json.dumps({
                'message': "Uploaded", 
                "route": str(image.image)
            }), status=200)
