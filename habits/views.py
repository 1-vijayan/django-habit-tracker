from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from datetime import date, timedelta

from .models import Habit, HabitLog
from .forms import RegisterForm


# PROFILE PAGE
@login_required
def profile(request):

    user = request.user
    habits = Habit.objects.filter(user=user)

    total_habits = habits.count()
    best_streak = habits.order_by("-streak").first()

    completed = HabitLog.objects.filter(habit__user=user).count()

    context = {
        "user": user,
        "total_habits": total_habits,
        "best_streak": best_streak,
        "completed": completed
    }

    return render(request, "profile.html", context)


# REGISTER
def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# DASHBOARD
@login_required
def home(request):

    # ADD HABIT
    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        category = request.POST.get("category")

        if name:
            Habit.objects.create(
                user=request.user,
                name=name,
                description=description,
                category=category
            )

        return redirect("home")

    habits = Habit.objects.filter(user=request.user)

    today = date.today()

    # DASHBOARD STATS
    total_habits = habits.count()

    completed_today = HabitLog.objects.filter(
        habit__user=request.user,
        date=today
    ).count()

    # WEEKLY CHART DATA
    week_labels = []
    week_data = []

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        label = day.strftime("%a")

        count = HabitLog.objects.filter(
            habit__user=request.user,
            date=day
        ).count()

        week_labels.append(label)
        week_data.append(count)

    # ACTIVITY CALENDAR (LAST 30 DAYS)
    activity = []

    for i in range(30):

        day = today - timedelta(days=i)

        count = HabitLog.objects.filter(
            habit__user=request.user,
            date=day
        ).count()

        activity.append({
            "date": day,
            "count": count
        })

    activity.reverse()

    context = {
        "habits": habits,
        "total_habits": total_habits,
        "completed_today": completed_today,
        "activity": activity,
        "week_labels": week_labels,
        "week_data": week_data
    }

    return render(request, "home.html", context)


# COMPLETE HABIT
@login_required
def complete_habit(request, habit_id):

    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    today = date.today()

    HabitLog.objects.get_or_create(
        habit=habit,
        date=today
    )

    if habit.last_completed == today:
        return redirect("home")

    if habit.last_completed:

        difference = (today - habit.last_completed).days

        if difference == 1:
            habit.streak += 1
        else:
            habit.streak = 1

    else:
        habit.streak = 1

    habit.last_completed = today
    habit.save()

    return redirect("home")


# DELETE HABIT
@login_required
def delete_habit(request, habit_id):

    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    habit.delete()

    return redirect("home")