from haystack import indexes

from web.models import Atom, BaseCategory, Class


class AtomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    AtomTitle = indexes.CharField(model_attr='name')
    AtomSum = indexes.CharField(model_attr='summary')
    AtomTitle_auto = indexes.EdgeNgramField(model_attr='name') #for haystack-autocomplete
    AtomSuggestions = indexes.FacetCharField()
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Atom

    def prepare(self, obj):
        print("prepare for AtomIndex is called!!!!")
        prepared_data = super(AtomIndex, self).prepare(obj)
        prepared_data['AtomSuggestions'] = prepared_data['text']
        return prepared_data


class BaseCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    BaseCatTitle = indexes.CharField(model_attr='name')
    BaseCatSum = indexes.CharField(model_attr='summary')
    BaseCatSuggestions = indexes.FacetCharField()
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return BaseCategory

    def prepare(self, obj):
        print("prepare for BaseCategoryIndex is called!!!!")
        prepared_data = super(BaseCategoryIndex, self).prepare(obj)
        prepared_data['BaseCatSuggestions'] = prepared_data['text']
        return prepared_data


class ClassIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ClassTitle = indexes.CharField(model_attr='name')
    ClassAuthor = indexes.CharField(model_attr='author', faceted=True)
    ClassStatus = indexes.BooleanField(model_attr='status', faceted=True)

    def get_model(self):
        return Class










