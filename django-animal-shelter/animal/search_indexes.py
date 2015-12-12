import datetime
from haystack import indexes
from .models import Animal


class AnimalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # The following are just some examples to provide additional filtering options.
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Animal

    def index_queryset(self, using=None):
        return self.get_model().objects.all()