from haystack import indexes
from haystack.backends.solr_backend import SolrSearchBackend
from django.template import RequestContext, loader, Context
from web.models import Atom, BaseCategory, Class, LectureNote, Example
from pybb.models import Category, Forum, Topic, Post

class AtomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    AtomTitle = indexes.CharField(model_attr='name')
    AtomSum = indexes.CharField(model_attr='summary')
    AtomSuggestions = indexes.FacetCharField()
    rendered = indexes.CharField(use_template=True, indexed=False)
    #Auto_Suggestions = indexes.EdgeNgramField(model_attr='name') #for haystack-autocomplete

    def get_model(self):
        return Atom

    def prepare(self, obj):
        prepared_data = super(AtomIndex, self).prepare(obj)
        prepared_data['AtomSuggestions'] = prepared_data['text']
        return prepared_data


class BaseCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    BaseCatTitle = indexes.CharField(model_attr='name')
    BaseCatSum = indexes.CharField(model_attr='summary')
    BaseCatSuggestions = indexes.FacetCharField()
    rendered = indexes.CharField(use_template=True, indexed=False)
    #Auto_Suggestions = indexes.EdgeNgramField(model_attr='name') #for haystack-autocomplete

    def get_model(self):
        return BaseCategory

    def prepare(self, obj):
        prepared_data = super(BaseCategoryIndex, self).prepare(obj)
        prepared_data['BaseCatSuggestions'] = prepared_data['text']
        return prepared_data


class ClassIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    ClassTitle = indexes.CharField(model_attr='name')
    ClassAuthor = indexes.CharField(model_attr='author', faceted=True)
    ClassStatus = indexes.CharField(model_attr='status', faceted=True)
    #Auto_Suggestions = indexes.EdgeNgramField(model_attr='name') #for haystack-autocomplete

    def get_model(self):
        return Class


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    CatTitle = indexes.CharField(model_attr='name')

    def get_model(self):
        return Category


class ForumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    ForumTitle = indexes.CharField(model_attr='name')
    ForumDescription = indexes.CharField(model_attr='description')
    #ForumMod = indexes.CharField(model_attr='moderators')
    
    def get_model(self):
        return Forum


class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    TopicTitle = indexes.CharField(model_attr='name')
    
    def get_model(self):
        return Topic


class RenderableItemIndex(indexes.SearchIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    Message = indexes.CharField(model_attr='body')

    class Meta:
        abstract = True

    def get_model(self):
        return RenderableItem


class PostIndex(RenderableItemIndex, indexes.Indexable):
    createTime = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Post

class LectureNoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    LecOwner = indexes.CharField(model_attr='owner')
    LecName = indexes.CharField(model_attr='filename')
    
    def get_model(self):
        return LectureNote
    
    def prepare(self, obj):
        data = super(LectureNoteIndex, self).prepare(obj)
        try:
            if obj.file:
                file_path = obj.file.path
                file_obj = open(file_path, "r+")
                extracted_data = self._get_backend(None).extract_file_contents(file_obj)
    
    # Now we'll finally perform the template processing to render the
    # text field with *all* of our metadata visible for templating:
                t = loader.select_template(('search/indexes/web/lecturenote_text.txt', ))
                data['text'] = t.render(Context({'object': obj,
                                    'extracted': extracted_data}))
            return data
        except:
            print("FileIndex: error accessing "+ obj.file.path+ " [Solr may not be open].")
            return data


class ExampleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    ExampleOwner = indexes.CharField(model_attr='owner')
    ExampleName = indexes.CharField(model_attr='filename')
    
    def get_model(self):
        return Example
    
    def prepare(self, obj):
        data = super(ExampleIndex, self).prepare(obj)
        try:
            if obj.file:
                file_path = obj.file.path
                file_obj = open(file_path, "r+")
                extracted_data = self._get_backend(None).extract_file_contents(file_obj)
            
            # Now we'll finally perform the template processing to render the
            # text field with *all* of our metadata visible for templating:
                t = loader.select_template(('search/indexes/web/example_text.txt', ))
                data['text'] = t.render(Context({'object': obj,
                                            'extracted': extracted_data}))
            return data
        except:
            print("FileIndex: error accessing " + obj.file.path + " [Solr may not be open].")
            return data
    
    




