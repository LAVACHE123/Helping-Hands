# Helping Hands

Helping Hands is a Django web application that connects seniors who need help with trusted local helpers. Requesters can post jobs, review applicants, select a helper, message them, mark jobs as completed, and leave reviews. Helpers can browse open jobs, apply, manage active work, message requesters, and receive reviews.

## Main features

- User registration, login, logout, and role-based profiles.
- Two user flows: requester and helper.
- Job posting, browsing, category filtering, applications, and helper selection.
- Dashboard for active jobs and pending applications.
- Per-job messaging between requester and selected helper.
- Completed job history, reviews, and reports.
- Django admin management for the main database models.
- Custom static CSS, Bootstrap, uploaded avatars, and seeded demo data.

## Setup

From the repository root:

```bash
cd project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata data.json
python3 manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Sample credentials

All sample accounts below use:

```text
password123
```

| Role | Username | Notes |
| --- | --- | --- |
| Admin | `louie` | Superuser/admin access |
| Requester | `bjorn_h` | Senior/requester account |
| Requester | `ragnhild_s` | Senior/requester account with posted jobs |
| Helper | `magnus_a` | Helper account |
| Helper | `soupy` | Helper account |

## Repository files

- Data dump: `project/data.json`
- Fixture copy: `project/fixtures/data.json`
- Python dependencies: `project/requirements.txt`
