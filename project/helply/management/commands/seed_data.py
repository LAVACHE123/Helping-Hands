import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from helply.models import Profile, Job, Category

# ── Helpers (young people) ────────────────────────────────────────────────────
HELPERS = [
    ("magnus_a",  "Magnus",  "Andersen",    "magnus.andersen@email.com",  "Oslo"),
    ("ingrid_h",  "Ingrid",  "Hansen",      "ingrid.hansen@email.com",    "Bærum"),
    ("erik_j",    "Erik",    "Johansen",    "erik.johansen@email.com",    "Asker"),
    ("astrid_l",  "Astrid",  "Larsen",      "astrid.larsen@email.com",    "Oslo"),
    ("jonas_b",   "Jonas",   "Berg",        "jonas.berg@email.com",       "Lørenskog"),
    ("maja_k",    "Maja",    "Kristiansen", "maja.kristiansen@email.com", "Oslo"),
    ("tobias_h",  "Tobias",  "Holm",        "tobias.holm@email.com",      "Lillestrøm"),
    ("frida_o",   "Frida",   "Olsen",       "frida.olsen@email.com",      "Sandvika"),
]

HELPER_BIOS = [
    "University student looking to help my community while earning extra income. Reliable and hardworking.",
    "I enjoy helping others and have a lot of free time between classes. Happy to assist with errands, tech, or chores.",
    "Friendly and patient — especially good with seniors. Available most weekdays.",
    "Recent high school grad with time to spare. I'm handy around the house and love animals.",
    "I've helped elderly neighbors my whole life and want to make it official. Trustworthy and punctual.",
    "Part-time student, full-time helper! I drive and can assist with shopping, appointments, or odd jobs.",
    "Experienced with garden work and basic home repairs. Happy to help with anything physical.",
    "Tech-savvy and patient. Great at explaining things slowly — phones, tablets, computers, no problem.",
]

# ── Requesters (seniors) ──────────────────────────────────────────────────────
REQUESTERS = [
    ("bjorn_h",    "Bjørn",    "Haugen",    "bjorn.haugen@email.com",    "Oslo"),
    ("sigrid_d",   "Sigrid",   "Dahl",      "sigrid.dahl@email.com",     "Bærum"),
    ("olav_m",     "Olav",     "Moen",      "olav.moen@email.com",       "Oslo"),
    ("ragnhild_s", "Ragnhild", "Strand",    "ragnhild.strand@email.com", "Asker"),
    ("knut_b",     "Knut",     "Bakke",     "knut.bakke@email.com",      "Lillestrøm"),
    ("marit_s",    "Marit",    "Sørensen",  "marit.sorensen@email.com",  "Oslo"),
    ("harald_l",   "Harald",   "Lund",      "harald.lund@email.com",     "Sandvika"),
    ("solveig_n",  "Solveig",  "Nygaard",   "solveig.nygaard@email.com", "Lørenskog"),
]

REQUESTER_BIOS = [
    "Retired teacher. I live alone and sometimes need a helping hand with errands and technology.",
    "78 years old, still active but could use help with heavier tasks around the house.",
    "I love my garden but my knees don't cooperate anymore. Looking for someone reliable and kind.",
    "Widower, living independently. I need occasional help with grocery runs and appointments.",
    "I'm fiercely independent but smart enough to ask for help when I need it!",
    "Recently moved to a new apartment and need help getting settled and organized.",
    "Looking for someone patient to help me with my phone and computer. My grandchildren are too busy!",
    "Retired engineer. I can manage most things but appreciate help with the heavy lifting.",
]

# ── Job postings ──────────────────────────────────────────────────────────────
JOB_TEMPLATES = [
    # (category_name, title, description, time_window, budget)
    ("Errands & Transportation",
     "Grocery run to IGA",
     "I need someone to pick up my weekly groceries at the IGA on Sherbrooke. I'll give you the list and money beforehand. Should take about an hour.",
     "Any weekday morning", 25),

    ("Tech & Digital Help",
     "Help setting up my new iPad",
     "My daughter bought me a new iPad for my birthday and I have no idea how to set it up. Need someone patient to help me get started with email and video calls.",
     "Weekend afternoon", 30),

    ("Around the House",
     "Moving furniture in living room",
     "I'd like to rearrange my living room furniture but it's too heavy for me. Just a couch, two armchairs and a bookshelf. Shouldn't take more than an hour.",
     "Saturday or Sunday", 35),

    ("Cleaning & Tidying",
     "Spring cleaning help",
     "Looking for someone to help with a thorough spring cleaning — windows, baseboards, and getting into corners I can't reach anymore. About 3-4 hours of work.",
     "Flexible, any weekday", 60),

    ("Garden & Outdoor",
     "Lawn mowing and hedge trimming",
     "My backyard lawn needs mowing and the hedges along the fence need a trim. I have all the equipment. About 2 hours of work.",
     "Weekend morning", 45),

    ("Errands & Transportation",
     "Drive to medical appointment",
     "I have a doctor's appointment downtown and no longer drive. Need a ride there and back, about 2 hours total including waiting time.",
     "Tuesday June 3rd, 10am", 30),

    ("Tech & Digital Help",
     "Set up online banking on my computer",
     "My bank is pushing me to use online banking but I'm nervous about doing it alone. Need someone to sit with me, help set it up, and show me how it works safely.",
     "Any afternoon this week", 40),

    ("Home Repairs & Maintenance",
     "Hang 4 picture frames",
     "I have 4 framed photos I'd like to hang in the hallway. I have a hammer and nails but my hands shake too much to do it myself.",
     "Flexible", 20),

    ("Pet & Animal Care",
     "Dog walking — twice daily for a week",
     "I'm recovering from a minor surgery and can't walk my golden retriever Biscuit for about a week. Twice a day, 20 minutes each walk in the neighbourhood.",
     "Starting this Monday, 1 week", 80),

    ("Administrative & Personal",
     "Help filling out government forms",
     "I received some forms from the government and I'm confused by the language. Need someone to sit with me and help fill them out correctly.",
     "Any weekday", 35),

    ("Garden & Outdoor",
     "Plant flowers in front garden",
     "I bought a flat of petunias and marigolds from the nursery. Just need someone to help me plant them — I'll direct, you dig! About 1.5 hours.",
     "This weekend", 30),

    ("Cleaning & Tidying",
     "Help organizing my basement",
     "My basement has accumulated years of stuff. I need someone energetic to help me sort, box, and carry things to donate. Could be a 2-day project.",
     "Two weekday afternoons", 90),

    ("Around the House",
     "Change smoke detector batteries",
     "I have 6 smoke detectors and a carbon monoxide detector, all beeping. I can't safely climb a ladder anymore. Simple job for someone tall!",
     "As soon as possible", 15),

    ("Tech & Digital Help",
     "Teach me how to use WhatsApp",
     "My family uses WhatsApp to share photos and do group calls but I can't figure it out. Need a patient teacher for about an hour.",
     "Any evening", 25),

    ("Errands & Transportation",
     "Pick up prescription from pharmacy",
     "My prescription is ready at the Jean Coutu on Notre-Dame but I'm not feeling well enough to go out. Need someone to pick it up and drop it off.",
     "Today or tomorrow", 20),
]


class Command(BaseCommand):
    help = 'Seed the database with sample users and job postings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        categories = {c.name: c for c in Category.objects.all()}

        # Create helpers
        helper_users = []
        for i, (username, first, last, email, location) in enumerate(HELPERS):
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                self.stdout.write(f'  Skipped existing helper: {username}')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first,
                    last_name=last,
                    email=email,
                    password='password123',
                )
                Profile.objects.filter(user=user).update(
                    role='helper',
                    bio=HELPER_BIOS[i],
                    location=location,
                )
                self.stdout.write(f'  Created helper: {first} {last}')
            helper_users.append(user)

        # Create requesters
        requester_users = []
        for i, (username, first, last, email, location) in enumerate(REQUESTERS):
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                self.stdout.write(f'  Skipped existing requester: {username}')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first,
                    last_name=last,
                    email=email,
                    password='password123',
                )
                Profile.objects.filter(user=user).update(
                    role='requester',
                    bio=REQUESTER_BIOS[i],
                    location=location,
                )
                self.stdout.write(f'  Created requester: {first} {last}')
            requester_users.append(user)

        # Create job postings
        jobs_created = 0
        for cat_name, title, description, time_window, budget in JOB_TEMPLATES:
            if Job.objects.filter(title=title).exists():
                continue
            requester = random.choice(requester_users)
            category = categories.get(cat_name)
            if not category:
                continue
            Job.objects.create(
                requester=requester,
                category=category,
                title=title,
                description=description,
                location=requester.profile.location,
                time_window=time_window,
                budget=budget,
                budget_negotiable=random.choice([True, False]),
                status='open',
            )
            jobs_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {len(helper_users)} helpers, {len(requester_users)} requesters, {jobs_created} job postings.'
        ))
        self.stdout.write('All passwords are: password123')
