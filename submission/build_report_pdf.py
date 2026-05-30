from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
    Image,
)


OUT = Path(__file__).resolve().parent / "Helping_Hands_Final_Report.pdf"
SCHEMA = Path(__file__).resolve().parent / "Helping_Hands_Relational_Schema.png"


def styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(
        name="ReportTitle",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111111"),
        spaceAfter=6,
    ))
    base.add(ParagraphStyle(
        name="Subtitle",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        spaceAfter=16,
    ))
    base.add(ParagraphStyle(
        name="H1Custom",
        parent=base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2E74B5"),
        spaceBefore=12,
        spaceAfter=6,
    ))
    base.add(ParagraphStyle(
        name="H2Custom",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2E74B5"),
        spaceBefore=10,
        spaceAfter=5,
    ))
    base.add(ParagraphStyle(
        name="BodyCustom",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=6,
    ))
    base.add(ParagraphStyle(
        name="Small",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=11,
    ))
    return base


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=16) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=18,
    )


def table(headers, rows, widths, style):
    data = [[Paragraph(h, style) for h in headers]]
    data.extend([[Paragraph(str(cell), style) for cell in row] for row in rows])
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F4F7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111111")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C0CC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(7.5 * inch, 0.45 * inch, f"Helping Hands final report | Page {doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.75 * inch,
    )
    story = []

    story.append(p("Helping Hands", s["ReportTitle"]))
    story.append(p("Final project report - ELE 3921 Web Applications Development", s["Subtitle"]))
    story.append(p("<i>Team members: [add names] | GitHub: [add public repository link] | Video: [add video link]</i>", s["Subtitle"]))

    story.append(p("Project summary", s["H1Custom"]))
    story.append(p("Helping Hands is a Django web application designed to connect seniors who need help with everyday tasks to trusted local helpers who want to earn money by helping their community. The project addresses a practical local problem: many older adults can live independently, but still need occasional support with errands, technology, housework, transport, gardening, or small maintenance tasks.", s["BodyCustom"]))
    story.append(p("The application has two main user roles: requesters and helpers. Requesters can create job posts, review applications, select a helper, message the selected person, mark jobs as completed, and leave reviews. Helpers can browse open jobs, apply with a short message, track pending applications, message requesters after selection, and build reputation through reviews.", s["BodyCustom"]))

    story.append(p("Main features", s["H1Custom"]))
    story.append(bullets([
        "Registration and authentication using Django's built-in user system.",
        "Role-based accounts for requesters and helpers, with different dashboards and redirects.",
        "Job posting, category browsing, job details, applications, helper selection, and completion flow.",
        "Per-job messaging between the requester and selected helper.",
        "Profile pages with bio, location, avatar, posted/accepted jobs, and reviews.",
        "Review and report features after relevant job interactions.",
        "Admin interface for managing users, profiles, categories, jobs, applications, messages, reviews, and reports.",
        "Seeded demo data, uploaded avatars, Bootstrap, and a custom static stylesheet.",
    ], s["BodyCustom"]))

    story.append(p("Architecture overview", s["H1Custom"]))
    if SCHEMA.exists():
        story.append(Image(str(SCHEMA), width=6.5 * inch, height=4.6 * inch))
        story.append(p("<i>Figure 1. Relational schema for the Helping Hands application.</i>", s["Small"]))
        story.append(Spacer(1, 6))

    story.append(p("Models", s["H2Custom"]))
    story.append(table(
        ["Model", "Purpose", "Important relationships"],
        [
            ["Category", "Stores job categories such as errands, cleaning, garden work, and tech help.", "Referenced by Job with protected deletion."],
            ["Profile", "Extends Django User with role, bio, location, and avatar.", "One-to-one with User."],
            ["Job", "Stores task posts, requester, helper, budget, timing, location, and status.", "Requester/helper connect to User; category connects to Category."],
            ["JobApplication", "Stores helper applications and optional application messages.", "Connects Job and applicant User; unique per job/applicant pair."],
            ["Message", "Stores messages in a job-specific conversation.", "Connects sender User to a Job."],
            ["Review", "Stores rating and comment after completed jobs.", "Connects reviewer, reviewee, and Job."],
            ["Report", "Stores reports for moderation and safety.", "Connects reporter, reported user, and related job."],
        ],
        [1.1 * inch, 2.75 * inch, 2.65 * inch],
        s["Small"],
    ))
    story.append(Spacer(1, 6))

    story.append(p("Views and templates", s["H2Custom"]))
    story.append(p("The project uses Django templates for server-side rendering. Most user actions are implemented as regular Django views with redirects and messages after successful changes. The main views include home, registration/login/logout, profile pages, dashboard pages, job list/detail/create/apply/select/complete, messaging, review creation, and report creation.", s["BodyCustom"]))

    story.append(p("Forms and validation", s["H2Custom"]))
    story.append(p("The application uses Django forms and model forms for user input. RegisterForm extends UserCreationForm and creates both the User and Profile. JobForm, ProfileForm, MessageForm, ReviewForm, and ReportForm handle the main user interactions. Form validation errors are displayed in the templates, while successful actions use Django messages to give feedback.", s["BodyCustom"]))

    story.append(p("Authentication and access control", s["H2Custom"]))
    story.append(p("Authentication is based on Django's built-in User model. Views that require a logged-in user use login_required. Additional permission checks are handled in the views: only a requester can select a helper or complete their own job; only the requester and selected helper can access a message thread; reviews can only be left for completed jobs; and duplicate reviews/applications are prevented.", s["BodyCustom"]))

    story.append(p("Development process", s["H1Custom"]))
    story.append(p("The project was developed around the core marketplace workflow. The models were created first so the main relationships were clear, then views and templates were added around the requester and helper journeys. The design aims to feel calm and trustworthy for seniors while still being easy for helpers to scan and use.", s["BodyCustom"]))
    story.append(p("Most functionality is server-side Django, with only light JavaScript for interface details such as the role picker during registration and the message box scroll behavior. This kept the application simple and aligned with the course focus on Django, templates, forms, authentication, and database relationships.", s["BodyCustom"]))

    story.append(p("Front-end design", s["H1Custom"]))
    story.append(p("The interface uses Bootstrap together with a custom static CSS file. The visual style uses a dark navigation bar, off-white page background, white content cards, terracotta accent buttons, serif headings, and readable form styling. The home page uses a large image hero, while the app pages are more functional and compact.", s["BodyCustom"]))
    story.append(p("A custom static stylesheet is included at helply/static/helply/css/style.css. This was added so the project has committed static assets instead of relying only on inline CSS and external CDNs.", s["BodyCustom"]))

    story.append(p("Peer review reflection", s["H1Custom"]))
    story.append(p("The peer review highlighted several strengths: the model design, the requester/helper split, access control, the admin setup, messaging, and the report feature. It also pointed out areas to improve before submission, especially the need for a clear requirements file, data dump, and custom static assets.", s["BodyCustom"]))
    story.append(p("After reviewing the feedback, the project was cleaned up for submission. The repository now includes requirements.txt, a cleaner data dump, custom static CSS, and a README with setup instructions and sample credentials. JobApplication was also added to the admin interface so all important project data can be managed through Django admin.", s["BodyCustom"]))

    story.append(p("Future improvements", s["H1Custom"]))
    story.append(bullets([
        "Add search and filtering by location, budget, time window, and review rating.",
        "Add notifications by email or in-app alerts when someone applies, is selected, or sends a message.",
        "Add stronger trust features such as identity verification, references, and admin moderation tools.",
        "Add payment handling or clear payment confirmation for real marketplace use.",
        "Improve mobile responsiveness further and add more automated tests for critical permission flows.",
    ], s["BodyCustom"]))

    story.append(p("Sample user credentials", s["H1Custom"]))
    story.append(p("The following demo accounts can be used to test the application. All use the password <b>password123</b>.", s["BodyCustom"]))
    story.append(table(
        ["Role", "Username", "Purpose"],
        [
            ["Admin", "louie", "Superuser account for Django admin."],
            ["Requester", "bjorn_h", "Senior/requester account for posting and managing jobs."],
            ["Requester", "ragnhild_s", "Requester account with example job activity."],
            ["Helper", "magnus_a", "Helper account for browsing and applying to jobs."],
            ["Helper", "soupy", "Additional helper account for testing role-specific flows."],
        ],
        [1.1 * inch, 1.4 * inch, 4.0 * inch],
        s["Small"],
    ))

    story.append(p("Submission links and files", s["H1Custom"]))
    story.append(bullets([
        "GitHub repository: [add public repository link]",
        "Video presentation: [add video link]",
        "Data dump: project/data.json and project/fixtures/data.json",
        "Requirements file: project/requirements.txt",
        "Static CSS: project/helply/static/helply/css/style.css",
    ], s["BodyCustom"]))

    story.append(p("AI tool usage", s["H1Custom"]))
    story.append(p("AI assistance was used for review and cleanup support near the end of the project: comparing the assignment requirements with the project, identifying missing submission checklist items, moving existing CSS into a static file, registering a missing admin model, preparing cleaner submission notes, and drafting this report. The core project concept, Django architecture, models, views, and workflows should be understood and explained by the team during the presentation.", s["BodyCustom"]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    build()
