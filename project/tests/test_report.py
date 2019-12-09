from report.models import User, Organization
from django.test import TestCase

class objectReportTest(TestCase):

    def test_user(self):
        user = User(first_name="x")
        user.save()
        user.last_name = "y"
        user.email = "x@email.com"
        user.save()
        user.delete()

    def test_org(self):
        org = Organization(name="A", slug="a")
        org.save()
        org.name = "B"
        org.save()
