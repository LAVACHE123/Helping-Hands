# Helping Hands Submission Checklist

## WiseFlow

- [ ] Upload the final report PDF.
- [ ] Include the public GitHub repository link.
- [ ] Include the video presentation link if aiming for grade A or B.

## GitHub repository

- [ ] Full Django codebase is pushed.
- [ ] `project/requirements.txt` is included.
- [ ] `project/data.json` or `project/fixtures/data.json` is included.
- [ ] `project/helply/static/helply/css/style.css` is included.
- [ ] Media/avatar files referenced by the fixture are included.
- [ ] README includes setup instructions and sample credentials.

## Final report

- [ ] Project purpose and target audience.
- [ ] Main features.
- [ ] Architecture overview: models, views, templates, forms.
- [ ] GitHub repository link.
- [ ] Video presentation link.
- [ ] Peer review reflection.
- [ ] Sample user credentials.
- [ ] AI usage documentation.

## Final local check

```bash
cd project
python3 manage.py check
python3 manage.py migrate
python3 manage.py loaddata data.json
python3 manage.py runserver
```
