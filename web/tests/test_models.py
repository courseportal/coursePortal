from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from web.models import (BaseCategory, Atom, Video, Class, 
    validate_youtube_video_id, Exposition, validate_link, Note, validate_uploaded_file)

class BaseCategoryTests(TestCase):
    r"""Tests for BaseCategory."""
    def setUp(self):
        r"""Create the test environment for testing BaseCategory."""
        g = BaseCategory.objects.get_or_create(title='g')[0]
        p = BaseCategory.objects.get_or_create(title='p')[0]
        #p.parent_categories.add(g)
        c1 = BaseCategory.objects.get_or_create(title='c1')[0]
        c2 = BaseCategory.objects.get_or_create(title='c2')[0]
        #c1.parent_categories.add(p)
        #p.child_categories.add(c2)
        o = BaseCategory.objects.get_or_create(title='orphan', summary='s')[0]
        
    def test_hierarchy(self):
        r"""Tests that the ManyToMany relationship with itself is working properly from both sides."""
        g = BaseCategory.objects.get(title='g')
        p = BaseCategory.objects.get(title='p')
        c1 = BaseCategory.objects.get(title='c1')
        c2 = BaseCategory.objects.get(title='c2')
        self.assertEqual(len(g.child_categories.all()), 0)
        try:
            p.parent_categories.add(g)
            c1.parent_categories.add(p)
            p.child_categories.add(c2)
        except:
            self.fail('Failed to add ManyToMany relationship with self in field `parent_categories`.')
        self.assertEqual(g.child_categories.all()[0].title, p.title)
        self.assertEqual(c1.parent_categories.all()[0].title, p.title)
        parent = g.child_categories.all()[0]
        for child in parent.child_categories.all():
            self.assertEqual(child.parent_categories.all()[0].title, 
                parent.title)
        self.assertEqual(len(c1.child_categories.all()), 0)
        self.assertEqual(len(g.parent_categories.all()), 0)
        
    def test_inherited_fields(self):
        r"""Tests fields inherited from ``web.WebBaseModel``."""
        with self.assertRaisesRegexp(ValidationError, "title"):
            obj = BaseCategory.objects.create()
            obj.clean()
        obj = BaseCategory.objects.create(title='test')
        created = obj.date_created
        self.assertEqual(obj.title, 'test')
        obj.save()
        self.assertEqual(obj.date_created, created)
        self.assertGreater(obj.date_modified, obj.date_created)
        
    def test_summary(self):
        r"""Tests the summary field."""
        obj = BaseCategory.objects.get(title='orphan')
        obj2 = BaseCategory.objects.get(title='c1')
        self.assertEqual(obj.summary, 's')
        self.assertEqual(obj2.summary, _('There is currently no summary.'))
        
    def test_stringify(self):
        r"""Tests that the object stringifies correctly."""
        obj = BaseCategory.objects.get(title='orphan')
        self.assertEqual(str(obj), 'orphan')
        
    def test_meta(self):
        r"""Tests the Meta class ordering."""
        objects = list(BaseCategory.objects.all())
        g = BaseCategory.objects.get(title='g')
        p = BaseCategory.objects.get(title='p')
        c1 = BaseCategory.objects.get(title='c1')
        c2 = BaseCategory.objects.get(title='c2')
        o = BaseCategory.objects.get(title='orphan')
        object_list = [c1, c2, g, o, p]
        self.assertEqual(objects, object_list)
        
class AtomTests(TestCase):
    r"""Test the Atom model."""
    def setUp(self):
        r"""Set up models for testing on."""
        self.c = BaseCategory.objects.get_or_create(title='cat')[0]
        self.a1 = Atom.objects.get_or_create(title='a1', base_category=self.c, 
            summary='s')[0]
        self.a2 = Atom.objects.get_or_create(title='a2', base_category=self.c)[0]
        
    def test_base_category_relationship(self):
        r"""Tests the `base_category` foreign key from both ends."""
        self.assertEqual(len(self.c.child_atoms.all()), 2)
        self.assertEqual(self.a1.base_category, self.c)
        with self.assertRaisesRegexp(IntegrityError, "base_category_id"):
            Atom.objects.create(title='a1')
    
    def test_summary(self):
        r"""Tests the summary field."""
        obj = Atom.objects.get(title='a1')
        obj2 = Atom.objects.get(title='a2')
        self.assertEqual(obj.summary, 's')
        self.assertEqual(obj2.summary, _('There is currently no summary.'))
        
    def test_stringify(self):
        r"""Tests that the object stringifies correctly."""
        obj = Atom.objects.get(title='a1')
        self.assertEqual(str(obj), 'a1')
        
    def test_meta(self):
        r"""Tests the Meta class ordering."""
        objects = list(Atom.objects.all())
        object_list = [self.a1, self.a2]
        self.assertEqual(objects, object_list)
        
    def test_inherited_fields(self):
        r"""Tests fields inherited from ``web.WebBaseModel``."""
        with self.assertRaisesRegexp(ValidationError, "title"):
            obj = Atom.objects.create(base_category=self.c)
            obj.clean()
        obj = Atom.objects.create(title='test', base_category=self.c)
        created = obj.date_created
        self.assertEqual(obj.title, 'test')
        obj.save()
        self.assertEqual(obj.date_created, created)
        self.assertGreater(obj.date_modified, obj.date_created)
        
class VideoTests(TestCase):
    r"""Tests videos and relevant validators."""
    def setUp(self):
        r"""Sets up the test environment."""
        self.u = User.objects.get_or_create(username='username', 
            password='password')[0]
        self.c1 = Class.objects.get_or_create(title='c1', owner=self.u)[0]
        self.c2 = Class.objects.get_or_create(title='c2', owner=self.u)[0]
        self.b = BaseCategory.objects.get_or_create(title='cat')[0]
        self.a1 = Atom.objects.get_or_create(title='a1', 
            base_category=self.b)[0]
        self.a2 = Atom.objects.get_or_create(title='a2', 
            base_category=self.b)[0]
    
        self.v1 = Video.objects.get_or_create(title='v1', owner=self.u, 
            content='c', video='0123-5678_0')[0]
        self.v2 = Video.objects.get_or_create(title='v2', owner=self.u,
            video='0123')[0]
        self.v3 = Video.objects.get_or_create(title='v3', owner=self.u,
                video='01234567890123')[0]
        self.v4 = Video.objects.get_or_create(title='v4', owner=self.u,
            video='01234/67890')[0]
        
    def test_inherited_fields(self):
        r"""Tests fields inherited from ``web.WebBaseModel``."""
        with self.assertRaisesRegexp(ValidationError, "title"):
            obj = Video.objects.create(owner=self.u)
            obj.clean()
        obj = Video.objects.create(title='test', owner=self.u)
        created = obj.date_created
        self.assertEqual(obj.title, 'test')
        obj.save()
        self.assertEqual(obj.date_created, created)
        self.assertGreater(obj.date_modified, obj.date_created)
            
    def test_content(self):
        r"""Tests the content of Video."""
        self.assertEqual(self.v1.content, 'c')
        self.assertEqual(self.v2.content, '-')
        
    def test_meta(self):
        r"""Tests the Meta class ordering."""
        objects = list(Video.objects.all())
        object_list = [self.v1, self.v2, self.v3, self.v4]
        self.assertEqual(objects, object_list)
        
    def test_stringify(self):
        r"""Tests that the object stringifies correctly."""
        obj = Video.objects.get(title='v1')
        self.assertEqual(str(obj), 'v1')
        
    def test_owner(self):
        r"""Tests the `owner` field."""
        with self.assertRaisesRegexp(IntegrityError, "owner_id"):
            Video.objects.create(title='title')
        self.assertEqual(self.v1.owner, self.u)
        
    def test_atoms_relationship(self):
        r"""Tests that the atoms relationship works correctly from both sides."""
        self.v1.atoms.add(self.a1)
        self.v2.atoms.add(self.a2)
        self.v3.atoms.add(self.a1, self.a2)
        self.assertEqual(len(self.a1.video_set.all()), 2)
        self.assertEqual(len(self.a2.video_set.all()), 2)
        self.assertEqual(len(self.v1.atoms.all()), 1)
        self.assertEqual(len(self.v3.atoms.all()), 2)
        self.v1.atoms.clear()
        self.a1.video_set.add(self.v1)
        self.assertEqual(self.v1.atoms.all()[0], self.a1)
        
    def test_classes_stickied_in(self):
        r"""Tests the `classes_stickied_in` relationship."""
        self.v1.classes_stickied_in.add(self.c1)
        self.c2.stickied_videos.add(self.v2)
        self.assertEqual(self.v1.classes_stickied_in.all()[0], self.c1)
        self.assertEqual(self.v2.classes_stickied_in.all()[0], self.c2)
        
    def test_validate_youtube_video_id(self):
        r"""Tests the custom validation for the 'video' field."""
        try:
            validate_youtube_video_id(self.v1.video)
        except:
            self.fail("'validate_youtube_id' rejected a correct id.")
        with self.assertRaisesRegexp(ValidationError, 'not a valid YouTube'):
            validate_youtube_video_id(self.v2.video)
        with self.assertRaisesRegexp(ValidationError, 'not a valid YouTube'):
            validate_youtube_video_id(self.v3.video)
        with self.assertRaisesRegexp(ValidationError, 'not a valid YouTube'):
            validate_youtube_video_id(self.v4.video)
            
class ExpositionTests(TestCase):
    r"""Tests for the Exposition model."""
    def setUp(self):
        r"""Sets up the testing environment."""
        self.u = User.objects.get_or_create(username='username', 
            password='password')[0]
        self.c1 = Class.objects.get_or_create(title='c1', owner=self.u)[0]
        self.c2 = Class.objects.get_or_create(title='c2', owner=self.u)[0]
        self.b = BaseCategory.objects.get_or_create(title='cat')[0]
        self.a1 = Atom.objects.get_or_create(title='a1', 
            base_category=self.b)[0]
        self.a2 = Atom.objects.get_or_create(title='a2', 
            base_category=self.b)[0]
            
        self.e1 = Exposition.objects.get_or_create(title='e1', owner=self.u,
            link="http://www.wikipedia.com")[0]
        self.e2 = Exposition.objects.get_or_create(title='e2', owner=self.u)[0]
        self.e3 = Exposition.objects.get_or_create(title='e3', owner=self.u,
            link="https://www.wikipedia.com")[0]
        self.e4 = Exposition.objects.get_or_create(title='e4', owner=self.u,
            link="https://")[0]
        self.e5 = Exposition.objects.get_or_create(title='e5', owner=self.u,
            link="google.com")[0]
        
            
    def test_inherited_fields(self):
        r"""Tests fields inherited from ``web.WebBaseModel``."""
        with self.assertRaisesRegexp(ValidationError, "title"):
            obj = Exposition.objects.create(owner=self.u)
            obj.clean()
        obj = Video.objects.create(title='test', owner=self.u)
        created = obj.date_created
        self.assertEqual(obj.title, 'test')
        obj.save()
        self.assertEqual(obj.date_created, created)
        self.assertGreater(obj.date_modified, obj.date_created)
        
    def test_meta(self):
        r"""Tests the Meta class ordering."""
        objects = list(Exposition.objects.all())
        object_list = [self.e1, self.e2, self.e3, self.e4, self.e5]
        self.assertEqual(objects, object_list)
        
    def test_stringify(self):
        r"""Tests that the object stringifies correctly."""
        obj = Exposition.objects.get(title='e1')
        self.assertEqual(str(obj), 'e1')
        
    def test_owner(self):
        r"""Tests the `owner` field."""
        with self.assertRaisesRegexp(IntegrityError, "owner_id"):
            Exposition.objects.create(title='title')
        self.assertEqual(self.e1.owner, self.u)
        
    def test_atoms_relationship(self):
        r"""Tests that the atoms relationship works correctly from both sides."""
        self.e1.atoms.add(self.a1)
        self.e2.atoms.add(self.a2)
        self.e3.atoms.add(self.a1, self.a2)
        self.assertEqual(len(self.a1.exposition_set.all()), 2)
        self.assertEqual(len(self.a2.exposition_set.all()), 2)
        self.assertEqual(len(self.e1.atoms.all()), 1)
        self.assertEqual(len(self.e3.atoms.all()), 2)
        self.e1.atoms.clear()
        self.a1.exposition_set.add(self.e1)
        self.assertEqual(self.e1.atoms.all()[0], self.a1)
        
        self.e4.atoms.add(self.a1)
        self.e4.atoms.add(self.a1)
        self.e4.atoms.add(self.a1)
        self.assertEqual(len(self.e4.atoms.all()), 1)
        
    def test_classes_stickied_in(self):
        r"""Tests the `classes_stickied_in` relationship."""
        self.e1.classes_stickied_in.add(self.c1)
        self.c2.stickied_expositions.add(self.e2)
        self.assertEqual(self.e1.classes_stickied_in.all()[0], self.c1)
        self.assertEqual(self.e2.classes_stickied_in.all()[0], self.c2)
        
    def test_validate_link_and_link_field(self):
        r"""Tests the custom link validator and the link field."""
        self.assertEquals(self.e2.link, 'http://')
        test = Exposition.objects.get_or_create(title='test', owner=self.u,
            link='http:/www.google.com')[0]
        try:
            validate_link(self.e1.link)
            validate_link(self.e2.link)
            validate_link(self.e3.link)
            validate_link(self.e4.link)
        except:
            self.fail('Good link rejected.')
        with self.assertRaisesRegexp(ValidationError, 'The link must begin'):
            validate_link(self.e5.link)
        with self.assertRaisesRegexp(ValidationError, 'The link must begin'):
            validate_link(test.link)
        test.link = 'ttp://www.google.com'
        test.save()
        with self.assertRaisesRegexp(ValidationError, 'The link must begin'):
            validate_link(test.link)
            
class NoteTests(TestCase):
    r"""Tests for the `Note` model."""
    def setUp(self):
        r"""Sets up the test environment."""
        