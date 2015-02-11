import unittest
import transaction

from pyramid import testing

from .models import (
    DBSession,
    is_valid_ean13,
    )

class TestEAN13Validation(unittest.TestCase):
    def test_ean13_validation(self):
        test_cases = (
            # Code             Valid
            ('9781933988788',  True),
            ('9780321349606',  True),
            ('978032134960X',  False), # non-digit checksum
            ('X780321349606',  False), # non-digit number
            ('7980321349606',  False), # first two digits swapped
            ('780321349606',   False), # missing one digit 
            ('99780321349606', False), # extra digit 
            ('',               False), # empty string
        )

        for ean13, valid in test_cases:
            self.assertEqual(is_valid_ean13(ean13), valid, ean13)


#class TestMyViewSuccessCondition(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#        from sqlalchemy import create_engine
#        engine = create_engine('sqlite://')
#        from .models import (
#            Base,
#            MyModel,
#            )
#        DBSession.configure(bind=engine)
#        Base.metadata.create_all(engine)
#        with transaction.manager:
#            model = MyModel(name='one', value=55)
#            DBSession.add(model)
#
#    def tearDown(self):
#        DBSession.remove()
#        testing.tearDown()
#
#    def test_passing_view(self):
#        from .views import my_view
#        request = testing.DummyRequest()
#        info = my_view(request)
#        self.assertEqual(info['one'].name, 'one')
#        self.assertEqual(info['project'], 'PyramidDemo')
#
#
#class TestMyViewFailureCondition(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#        from sqlalchemy import create_engine
#        engine = create_engine('sqlite://')
#        from .models import (
#            Base,
#            MyModel,
#            )
#        DBSession.configure(bind=engine)
#
#    def tearDown(self):
#        DBSession.remove()
#        testing.tearDown()
#
#    def test_failing_view(self):
#        from .views import my_view
#        request = testing.DummyRequest()
#        info = my_view(request)
#        self.assertEqual(info.status_int, 500)
