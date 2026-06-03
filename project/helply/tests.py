from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Category, Job, JobApplication, Message, Profile, Review, Report


class BasicTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Errands",
            icon="car"
        )

        self.requester = User.objects.create_user(
            username="requester",
            password="testpass123",
            first_name="Request",
            last_name="User"
        )
        self.requester.profile.role = "requester"
        self.requester.profile.save()

        self.helper = User.objects.create_user(
            username="helper",
            password="testpass123",
            first_name="Helper",
            last_name="User"
        )
        self.helper.profile.role = "helper"
        self.helper.profile.save()

        self.job = Job.objects.create(
            requester=self.requester,
            category=self.category,
            title="Help with groceries",
            description="Need help buying groceries",
            location="Oslo",
            time_window="Tomorrow",
            budget=25,
            budget_negotiable=True,
            status="open"
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_jobs_page_loads(self):
        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Help with groceries")

    def test_job_detail_page_loads(self):
        response = self.client.get(reverse("job_detail", args=[self.job.id]))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        logged_in = self.client.login(
            username="requester",
            password="testpass123"
        )

        self.assertTrue(logged_in)

    def test_wrong_login_does_not_work(self):
        logged_in = self.client.login(
            username="requester",
            password="wrongpass"
        )

        self.assertFalse(logged_in)

    def test_dashboard_needs_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)

    def test_user_can_register(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "role": "helper"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_profile_page_loads_when_logged_in(self):
        self.client.login(username="requester", password="testpass123")

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_edit_profile(self):
        self.client.login(username="helper", password="testpass123")

        response = self.client.post(reverse("profile_edit"), {
            "first_name": "Updated",
            "last_name": "Helper",
            "email": "updated@example.com",
            "bio": "I like helping people",
            "location": "Bergen"
        })

        self.assertEqual(response.status_code, 302)

        self.helper.refresh_from_db()
        self.helper.profile.refresh_from_db()

        self.assertEqual(self.helper.first_name, "Updated")
        self.assertEqual(self.helper.profile.location, "Bergen")

    def test_logged_in_user_can_create_job(self):
        self.client.login(username="requester", password="testpass123")

        response = self.client.post(reverse("job_create"), {
            "title": "Clean my kitchen",
            "description": "Need help cleaning",
            "category": self.category.id,
            "location": "Oslo",
            "time_window": "Friday",
            "budget": "40.00",
            "budget_negotiable": "on"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Job.objects.filter(title="Clean my kitchen").exists())

    def test_logged_out_user_cannot_create_job(self):
        response = self.client.get(reverse("job_create"))

        self.assertEqual(response.status_code, 302)

    def test_helper_can_apply_for_job(self):
        self.client.login(username="helper", password="testpass123")

        response = self.client.post(reverse("job_apply", args=[self.job.id]), {
            "message": "I can help"
        })

        self.assertEqual(response.status_code, 302)

        application = JobApplication.objects.filter(
            job=self.job,
            applicant=self.helper
        )

        self.assertEqual(application.count(), 1)

    def test_requester_cannot_apply_to_own_job(self):
        self.client.login(username="requester", password="testpass123")

        self.client.post(reverse("job_apply", args=[self.job.id]), {
            "message": "I can help myself"
        })

        application = JobApplication.objects.filter(
            job=self.job,
            applicant=self.requester
        )

        self.assertEqual(application.count(), 0)

    def test_helper_cannot_apply_twice(self):
        JobApplication.objects.create(
            job=self.job,
            applicant=self.helper,
            message="First application"
        )

        self.client.login(username="helper", password="testpass123")

        self.client.post(reverse("job_apply", args=[self.job.id]), {
            "message": "Second application"
        })

        applications = JobApplication.objects.filter(
            job=self.job,
            applicant=self.helper
        )

        self.assertEqual(applications.count(), 1)

    def test_requester_can_select_helper(self):
        JobApplication.objects.create(
            job=self.job,
            applicant=self.helper,
            message="I can help"
        )

        self.client.login(username="requester", password="testpass123")

        self.client.get(
            reverse("job_select_helper", args=[self.job.id, self.helper.id])
        )

        self.job.refresh_from_db()

        self.assertEqual(self.job.helper, self.helper)
        self.assertEqual(self.job.status, "accepted")

    def test_helper_cannot_select_himself(self):
        self.client.login(username="helper", password="testpass123")

        self.client.get(
            reverse("job_select_helper", args=[self.job.id, self.helper.id])
        )

        self.job.refresh_from_db()

        self.assertEqual(self.job.status, "open")

    def test_requester_can_complete_job(self):
        self.job.helper = self.helper
        self.job.status = "accepted"
        self.job.save()

        self.client.login(username="requester", password="testpass123")

        self.client.get(reverse("job_complete", args=[self.job.id]))

        self.job.refresh_from_db()

        self.assertEqual(self.job.status, "completed")

    def test_can_send_message(self):
        self.job.helper = self.helper
        self.job.status = "accepted"
        self.job.save()

        self.client.login(username="requester", password="testpass123")

        response = self.client.post(reverse("message_thread", args=[self.job.id]), {
            "body": "Hello"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(body="Hello").exists())

    def test_can_leave_review_after_completed_job(self):
        self.job.helper = self.helper
        self.job.status = "completed"
        self.job.save()

        self.client.login(username="requester", password="testpass123")

        response = self.client.post(reverse("review_create", args=[self.job.id]), {
            "rating": 5,
            "comment": "Good work"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(comment="Good work").exists())

    def test_cannot_review_same_job_twice(self):
        self.job.helper = self.helper
        self.job.status = "completed"
        self.job.save()

        Review.objects.create(
            job=self.job,
            reviewer=self.requester,
            reviewee=self.helper,
            rating=5,
            comment="First review"
        )

        self.client.login(username="requester", password="testpass123")

        self.client.post(reverse("review_create", args=[self.job.id]), {
            "rating": 4,
            "comment": "Second review"
        })

        reviews = Review.objects.filter(
            job=self.job,
            reviewer=self.requester
        )

        self.assertEqual(reviews.count(), 1)

    def test_can_report_user(self):
        self.job.helper = self.helper
        self.job.status = "completed"
        self.job.save()

        self.client.login(username="requester", password="testpass123")

        response = self.client.post(reverse("report_create", args=[self.job.id]), {
            "reason": "Something went wrong"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Report.objects.filter(reason="Something went wrong").exists())