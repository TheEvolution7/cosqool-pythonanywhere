from .serializers import BookmarkSerializer, Bookmark
from core.api.views import *

class BookmarkViewSet(CoreViewSet):  
    queryset = Bookmark.objects.all()  
    serializer_class = BookmarkSerializer
    
class AdminBookmarkViewSet(AdminCoreViewSet, BookmarkViewSet):  
    pass

class DashboardBookmarkViewSet(DashboardCoreViewSet, BookmarkViewSet):
    
    @action(detail=False, methods=['post'])
    def ajax_bookmark(self, request, format=None):
        user = request.user
        part = request.data['part']
        question = request.data['question']
        bookmark, created = Bookmark.objects.get_or_create(user=user, part_id=part, question_id=question)
        if not created:
            bookmark.delete()
            return Response({})
        
        serializer = BookmarkSerializer(bookmark)

        return Response(serializer.data)
        