import datetime
from haystack import indexes
from .models import *

class MenuItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return MenuItem
