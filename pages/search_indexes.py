import datetime
from haystack import indexes
from .models import *

class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Page
    
    content_auto = indexes.EdgeNgramField(model_attr='content')
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
