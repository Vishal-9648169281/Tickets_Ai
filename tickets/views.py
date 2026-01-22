"""
AI-Based IT Ticket Auto-Triage System
- BERT for root cause prediction
- Rule-based priority & team assignment
- Confidence-based manual review fallback
"""



from django.shortcuts import render
from .bert_model import predict_category
from .models import Ticket


# ---------- BUSINESS LOGIC ----------

def get_priority(text):
    text = text.lower()
    if "down" in text or "outage" in text or "crashed" in text:
        return "P1"
    elif "slow" in text or "delay" in text:
        return "P2"
    else:
        return "P3"


def assign_team(category):
    team_map = {
        "Network": "Network Support Team",
        "Software": "Application Support Team",
        "Hardware": "Hardware Support Team",
        "Access": "IT Admin Team",
        "Manual Review": "L1 Support Team"
    }
    return team_map.get(category, "L1 Support Team")


def generate_auto_reply(category):
    if category == "Manual Review":
        return (
            "Your ticket has been received and is under manual review "
            "by our support team."
        )
    return (
        f"Your ticket has been successfully registered. "
        f"It has been identified as a {category} related issue. "
        f"Our support team will work on it shortly."
    )


# ---------- MAIN VIEW ----------

def home(request):
    result = None

    if request.method == "POST":
        desc = request.POST.get("description", "").strip().lower()

        if not desc:
            result = {
                "category": "N/A",
                "confidence": 0,
                "reply": "Please enter a valid issue description."
            }
            return render(request, "tickets/index.html", {"result": result})

        # 🔴 STRONG KEYWORD RULES (FIRST)
        if "network" in desc or "internet" in desc or "wifi" in desc:
            category = "Network"
            confidence = 1.0
        elif "password" in desc or "reset" in desc or "login" in desc:
            category = "Access"
            confidence = 1.0
        elif "hardware" in desc or "keyboard" in desc or "screen" in desc:
            category = "Hardware"
            confidence = 1.0
        else:
            # 🔴 AI FALLBACK
            category, confidence = predict_category(desc)

            # 🔴 CONFIDENCE CHECK (LAST)
            if confidence < 0.45:
                category = "Manual Review"

        priority = get_priority(desc)
        team = assign_team(category)
        auto_reply = generate_auto_reply(category)

        Ticket.objects.create(
            description=desc,
            category=category,
            priority=priority,
            assigned_team=team,
            auto_reply=auto_reply
        )

        result = {
            "category": category,
            "confidence": round(confidence, 2),
            "reply": auto_reply
        }

    return render(request, "tickets/index.html", {"result": result})

        # 🔴 KEYWORD OVERRIDE 


# ---------- DASHBOARD ----------

def dashboard(request):
    priority_order = {'P1': 1, 'P2': 2, 'P3': 3}

    tickets = sorted(
        Ticket.objects.all(),
        key=lambda t: priority_order.get(t.priority, 4)
    )

    return render(request, 'tickets/dashboard.html', {'tickets': tickets})
