
import logging

from django.test import TestCase

from ..account.models import User
from ..tab.models import TabPage
from ..common.choices import UserStatus, Status
from ..common.utils import mills_timestamp

logger = logging.getLogger('django')


class TestModel(TestCase):

    def test_user(self):
        logger.info('Testing Insert User')

        user = User(email='test@test.com', password='test', avatar_url='testing', first_name='test', last_name='user',
                    theme='None', status=UserStatus.valid.key, create_date=mills_timestamp(),
                    update_date=mills_timestamp())
        user.save()
        check_user = User.objects.get(user_id=user.user_id, status=UserStatus.valid.key)
        assert check_user

        logger.info('Testing Update User')
        user.email = 'new@test.com'
        user.save()

        check_user = User.objects.get(user_id=user.user_id, status=UserStatus.valid.key)
        assert check_user.email == user.email

        logger.info('Testing Delete User')
        user.status = UserStatus.invalid.key
        user.save()

        check_user = User.objects.filter(user_id=user.user_id, status=UserStatus.valid.key)
        assert len(check_user) == 0

        logger.info('User Test Passed')

    def test_tab(self):
        logger.info('Testing Insert Tab')

        tab = TabPage(user_id=1, title='Test', content='None', status=Status.valid.key, create_date=mills_timestamp(),
                      update_date=mills_timestamp())
        tab.save()
        check_tab = TabPage.objects.get(tab_id=tab.tab_id, status=Status.valid.key)
        assert check_tab

        logger.info('Testing Update Tab')
        tab.content = 'Updated'
        tab.save()

        check_tab = TabPage.objects.get(tab_id=tab.tab_id, status=Status.valid.key)
        assert check_tab

        logger.info('Testing Delete Tab')
        tab.status = Status.invalid.key
        tab.save()

        check_user = TabPage.objects.filter(tab_id=tab.tab_id, status=Status.invalid.key)
        assert len(check_user) == 0

        logger.info('Tab Test Passed')

