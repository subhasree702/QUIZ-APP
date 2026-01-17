# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .models import Topic, Question
# import matplotlib.pyplot as plt
# import io, base64


# # views.py
# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         confirm = request.POST["confirm_password"]

#         if password != confirm:
#             messages.error(request, "Passwords do not match.")
#             return redirect("signup")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect("signup")

#         User.objects.create_user(username=username, password=password)
#         messages.success(request, "Account created! Please login.")
#         return redirect("login")

#     # ✅ Must pass request here
#     return render(request, "signup.html")

# # ---------- LOGIN ----------
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         # ✅ Check if user exists before authentication
#         if not User.objects.filter(username=username).exists():
#             messages.error(request, "User not found! Please sign up first.")
#             return redirect("login")  # 👈 stay on login page

#         # ✅ Authenticate existing user
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # messages.success(request, f"Welcome back, {username} 👋")  # ❌ Remove this line
#             return redirect("home")
#         else:
#             messages.error(request, "Invalid credentials. Please try again.")
#             return redirect("login")

#     return render(request, "login.html")

# # ---------- LOGOUT ----------
# def logout_view(request):
#     logout(request)
#     return redirect("login")


# # ---------- HOME ----------
# @login_required
# def home_view(request):
#     topics = Topic.objects.all()
#     return render(request, "home.html", {"topics": topics})


# # ---------- QUIZ ----------
# @login_required
# def quiz_view(request, topic_id):
#     topic = get_object_or_404(Topic, id=topic_id)
#     # get questions for topic (randomize if you want)
#     questions = list(Question.objects.filter(topic=topic)[:10])

#     if request.method == "POST":
#         score = 0
#         wrong_questions = []

#         # iterate the same questions shown to user
#         for q in questions:
#             # read the POST value; use None if not present
#             selected = request.POST.get(str(q.id), None)

#             # if user didn't select anything, show friendly label
#             if selected is None:
#                 selected_display = "No answer"
#             else:
#                 selected_display = selected

#             # compare selected answer to correct answer (exact string match)
#             if selected is not None and selected == q.correct_answer:
#                 score += 1
#             else:
#                 # add to wrong_questions with clear fields for template
#                 wrong_questions.append({
#                     "question": q.question_text,
#                     "selected": selected_display,
#                     "correct": q.correct_answer
#                 })

#         context = {
#             "score": score,
#             "total": len(questions),
#             "wrong_questions": wrong_questions,
#             "username": request.user.username,
#         }
#         return render(request, "result.html", context)

#     # GET request — show quiz page
#     return render(request, "quiz.html", {"topic": topic, "questions": questions})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.messages import get_messages
# from django.contrib.auth.decorators import login_required
# from .models import Topic, Question, UserProgress


# # ---------- SIGNUP ----------
# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         confirm = request.POST["confirm_password"]

#         if password != confirm:
#             messages.error(request, "Passwords do not match.")
#             return redirect("signup")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect("signup")

#         User.objects.create_user(username=username, password=password)
#         messages.success(request, "Account created successfully! Please log in.")
#         return redirect("login")

#     return render(request, "signup.html")


# # ---------- LOGIN ----------
# def login_view(request):
#     # 🧹 Clear any leftover messages (e.g., from logout or quiz completion)
#     storage = get_messages(request)
#     list(storage)  # Mark all existing messages as read

#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         # Check if user exists
#         if not User.objects.filter(username=username).exists():
#             messages.error(request, "User not found! Please sign up first.")
#             return redirect("login")

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)

#             # ✅ Reset quiz progress each time user logs in again
#             UserProgress.objects.filter(user=user).update(current_level=1)

#             messages.success(request, f"Welcome back, {username}! Your progress has been reset.")
#             return redirect("home")
#         else:
#             messages.error(request, "Invalid credentials. Please try again.")
#             return redirect("login")

#     return render(request, "login.html")


# # ---------- LOGOUT ----------
# def logout_view(request):
#     logout(request)
#     return redirect("login")


# # ---------- HOME ----------
# @login_required
# def home_view(request):
#     topics = Topic.objects.all()
#     return render(request, "home.html", {"topics": topics})


# # ---------- QUIZ ----------
# @login_required
# def quiz_view(request, topic_id):
#     topic = get_object_or_404(Topic, id=topic_id)

#     # ✅ Get or create user progress
#     progress, created = UserProgress.objects.get_or_create(
#         user=request.user,
#         topic=topic,
#         defaults={"current_level": 1, "highest_score": 0},
#     )

#     # ✅ Load questions for current level
#     questions = list(Question.objects.filter(topic=topic, level=progress.current_level)[:10])

#     if not questions:
#         messages.info(request, "No questions available for this level yet.")
#         return redirect("home")

#     if request.method == "POST":
#         score = 0
#         wrong_questions = []

#         for q in questions:
#             selected = request.POST.get(str(q.id))
#             if selected == q.correct_answer:
#                 score += 1
#             else:
#                 wrong_questions.append({
#                     "question": q.question_text,
#                     "selected": selected or "No answer",
#                     "correct": q.correct_answer,
#                 })

#         total = len(questions)
#         percentage = (score / total) * 100

#         # ✅ Level advancement logic
#         if percentage >= 70:
#             if progress.current_level < 2:
#                 messages.success(
#                     request,
#                     f"🎉 Great job {request.user.username}! You passed Level {progress.current_level}. Unlock Level {progress.current_level + 1}!"
#                 )
#             else:
#                 messages.success(request, f"🎉 Congratulations {request.user.username}! You completed all levels!")
#         else:
#             messages.info(request, "Try again to move to the next level.")

#         # ✅ Save highest score
#         progress.highest_score = max(progress.highest_score, percentage)
#         progress.save()

#         context = {
#             "topic": topic,
#             "score": score,
#             "total": total,
#             "percentage": round(percentage, 2),
#             "wrong_questions": wrong_questions,
#             "current_level": progress.current_level,
#             "username": request.user.username,
#         }

#         return render(request, "result.html", context)

#     return render(request, "quiz.html", {
#         "topic": topic,
#         "questions": questions,
#         "current_level": progress.current_level
#     })


# # ---------- NEXT LEVEL ----------
# @login_required
# def next_level_view(request, topic_id):
#     topic = get_object_or_404(Topic, id=topic_id)
#     progress = get_object_or_404(UserProgress, user=request.user, topic=topic)

#     # ✅ Allow next level only if not at max
#     if progress.current_level < 2:
#         progress.current_level += 1
#         progress.save()
#         messages.success(request, f"Level {progress.current_level} unlocked! 🚀")
#     else:
#         messages.info(request, "🎉 You’ve completed all levels!")

#     return redirect('quiz', topic_id=topic.id)
# views.py (full)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Topic, Question, UserProgress

# ---------- SIGNUP ----------
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        try:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Signup successful! Please login.")
            return redirect('login')
        except:
            messages.error(request, "Username already exists.")
            return redirect('signup')

    return render(request, "signup.html")

# ---------- LOGIN ----------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, "login.html")

# ---------- LOGOUT ----------
@login_required
def logout_view(request):
    list(messages.get_messages(request))  
    logout(request)
    return redirect('login')

# ---------- HOME ----------
@login_required
def home_view(request):
    topics = Topic.objects.all()
    return render(request, "home.html", {"topics": topics})


@login_required
def reset_level_view(request, topic_id):
    """
    'Choose Another Subject' resets progress for that topic.
    If ?keep_level=2 is passed, the user failed Level 2 and
    should start again from Level 2 next time.
    """
    progress = get_object_or_404(UserProgress, user=request.user, topic_id=topic_id)

    keep_level = request.GET.get("keep_level")  

    if keep_level == "2":
        progress.current_level = 2
        progress.passed_level1 = True   
        progress.passed_level2 = False
    else:

        progress.current_level = 1
        progress.passed_level1 = False
        progress.passed_level2 = False

    progress.highest_score = 0.0
    progress.save()

    
    request.session.pop("wrong_answers", None)

    return redirect('home')

# ---------- QUIZ ----------
@login_required
def quiz_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    user = request.user

    progress, created = UserProgress.objects.get_or_create(
        user=user,
        topic=topic,
        defaults={"current_level": 1, "highest_score": 0.0,
                  "passed_level1": False, "passed_level2": False},
    )

    
    if progress.passed_level2:
        progress.current_level = 1
    elif progress.passed_level1 and not progress.passed_level2:
        progress.current_level = 2
    else:
        progress.current_level = 1
    progress.save()

    
    if request.method == "GET" and request.GET.get("reset") == "1":
        request.session.pop("wrong_answers", None)


    questions = list(Question.objects.filter(topic=topic, level=progress.current_level)[:10])
    if not questions:
        messages.info(request, "No questions available for this level.")
        return redirect("home")

    if request.method == "POST":
        completed_level = progress.current_level
        score = 0
        wrong_questions_current = []

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1
            else:
                wrong_questions_current.append({
                    "level": progress.current_level,
                    "question": q.question_text,
                    "selected": selected or "No answer",
                    "correct": q.correct_answer,
                })

        total = len(questions)
        percentage = (score / total) * 100

        stored_wrong = request.session.get("wrong_answers", [])
        stored_wrong.extend(wrong_questions_current)
        request.session["wrong_answers"] = stored_wrong

        eligible = False

        # ---------- FIXED LEVEL LOGIC ----------
        if progress.current_level == 1:
            if percentage >= 70:
                progress.passed_level1 = True
                progress.passed_level2 = False  
                progress.current_level = 2
                progress.highest_score = max(progress.highest_score, percentage)
                eligible = True
            else:
                progress.passed_level1 = False
                progress.passed_level2 = False
                progress.current_level = 1
                progress.highest_score = max(progress.highest_score, percentage)
                eligible = False

        elif progress.current_level == 2:
            if percentage >= 70:
                progress.passed_level2 = True
                progress.current_level = 1  
                progress.highest_score = max(progress.highest_score, percentage)
                eligible = True
            else:
                progress.passed_level2 = False
                progress.current_level = 2  
                progress.highest_score = max(progress.highest_score, percentage)
                eligible = False

        progress.save()

        all_levels_completed = (progress.passed_level1 and progress.passed_level2)
        wrong_to_show = request.session.get("wrong_answers", []) if all_levels_completed else []

        context = {
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": round(percentage, 2),
            "current_level": progress.current_level,
            "username": user.username,
            "eligible": eligible,
            "all_levels_completed": all_levels_completed,
            "wrong_questions": wrong_to_show,
            "completed_level": completed_level,
        }

        return render(request, "result.html", context)

    return render(request, "quiz.html", {
        "topic": topic,
        "questions": questions,
        "current_level": progress.current_level
    })

# ---------- NEXT LEVEL ----------
@login_required
def next_level_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    progress = get_object_or_404(UserProgress, user=request.user, topic=topic)
    progress.current_level = 2
    progress.save()
    return redirect('quiz', topic_id=topic.id)

# ---------- RETRY LEVEL ----------
@login_required
def retry_level_view(request, topic_id):
    """
    Allow user to retry Level 2 after failing.
    Does not reset progress of level 1 or wrong answers.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    progress = get_object_or_404(UserProgress, user=request.user, topic=topic)
    progress.current_level = 2
    progress.save()
    request.session.pop("wrong_answers", None)

    return redirect('quiz', topic_id=topic.id)
