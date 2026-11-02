# from django.shortcuts import render

# Create your views here.


# from django.shortcuts import render, get_object_or_404
# from .models import Dictation


# def dictation_detail(request, id):
#     dictation = get_object_or_404(Dictation, id=id)

#     result = None

#     if request.method == "POST":
#         user_text = request.POST.get("user_text", "")

#         correct_text = dictation.text.strip().lower()
#         user_text = user_text.strip().lower()

#         if user_text == correct_text:
#             result = "درست است ✅"
#         else:
#             result = "اشتباه است ❌"

#     return render(
#         request,
#         "base/dictation_detail.html",
#         {
#             "dictation": dictation,
#             "result": result,
#         }
#     )










from django.shortcuts import render, get_object_or_404,redirect
from .models import Dictation, VocabularyTopic, VocabularyCard, GrammarTopic, GrammarExercise,Article

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, ReadingPassage, Dictation
from .forms import StudentProfileForm

from django.http import FileResponse, Http404
from django.db.models import Q


# from rest_framework import generics





def home(request):
    latest_articles = Article.objects.filter(
        is_published=True
    ).order_by("-created_at")[:3]

    return render(
        request,
        "base/index.html",
        {
            "latest_articles": latest_articles,
        }
    )




def grammar(request):
    topics = GrammarTopic.objects.all()

    return render(
        request,
        "base/grammar.html",
        {
            "topics": topics
        }
    )

def grammar_exercises(request, id):
    topic = get_object_or_404(GrammarTopic, id=id)

    exercises = topic.exercises.filter(
        level="A1"
    ).order_by("order", "id")

    results = {}

    if request.method == "POST":
        for exercise in exercises:
            answer = request.POST.get(
                f"exercise_{exercise.id}", ""
            )

            if answer:
                results[exercise.id] = {
                    "answer": answer,
                    "correct": answer == exercise.correct_option,
                }

    return render(
        request,
        "base/grammar_exercises.html",
        {
            "topic": topic,
            "exercises": exercises,
            "results": results,
        }
    )



def grammar_detail(request, id):
    topic = get_object_or_404(GrammarTopic, id=id)
    page_range = list(GrammarTopic.objects.order_by("order", "id"))
    current_index = page_range.index(topic)


    previous_item = (
        page_range[current_index - 1]
        if current_index > 0
        else None
    )

    next_item = (
        page_range[current_index + 1]
        if current_index < len(page_range) - 1
        else None
    )

    return render(
        request,
        "base/grammar_detail.html",
        {
            "topic": topic,
            "page_range": page_range,
            "current_item": topic,
            "previous_item": previous_item,
            "next_item": next_item,
            "page_url": "/grammar/",
            "previous_url": "/grammar/",
            "next_url": "/grammar/",
        }
    )


def blog(request):
    return render(request, "base/blog.html" )






def reading(request):
    passages = ReadingPassage.objects.filter(
        is_published=True
    ).select_related("level", "topic")

    return render(
        request,
        "base/reading.html",
        {"passages": passages},
    )


def tele(request):
    return render(request, "base/tele.html")


def vocabulary(request):
    topics=VocabularyTopic.objects.all()
    return render(
            request,
            'base/vocabulary.html',
            {'topics':topics} 
        )






def vocabulary_topic(request, id):
    topic = get_object_or_404(VocabularyTopic, id=id)
    cards = topic.cards.all().order_by('order')

    page_range = list(VocabularyTopic.objects.order_by('id'))
    current_index = page_range.index(topic)

    previous_item = (
        page_range[current_index - 1]
        if current_index > 0
        else None
    )

    next_item = (
        page_range[current_index + 1]
        if current_index < len(page_range) - 1
        else None
    )

    return render(
        request,
        'base/vocabulary_topic.html',
        {
            'topic': topic,
            'cards': cards,
            'page_range': page_range,
            'current_item': topic,
            'previous_item': previous_item,
            'next_item': next_item,
            'page_url': '/vocabulary/topic/',
            'previous_url': '/vocabulary/topic/',
            'next_url': '/vocabulary/topic/',
        }
    )


def dictation_detail(request, id):
    dictation = get_object_or_404(Dictation, id=id)

    # دریافت تمام دیکته‌ها برای صفحه‌بندی
    page_range = list(Dictation.objects.order_by("id"))
    total_dictations = len(page_range)

    # پیدا کردن شماره صفحه فعلی
    current_index = page_range.index(dictation)
    page_number = current_index + 1

    # دیکته قبلی
    previous_dictation = (
        page_range[current_index - 1]
        if current_index > 0
        else None
    )

    # دیکته بعدی
    next_dictation = (
        page_range[current_index + 1]
        if current_index < len(page_range) - 1
        else None
    )

    # متغیرهای صفحه‌بندی مشترک
    current_item = dictation
    previous_item = previous_dictation
    next_item = next_dictation

    page_url = "/dictation/"
    previous_url = "/dictation/"
    next_url = "/dictation/"

    # متغیرهای تصحیح پاسخ
    result = None
    score = None
    correct_count = 0
    wrong_count = 0

    if request.method == "POST":
        user_text = request.POST.get("user_text", "")

        correct_words = dictation.text.lower().split()
        user_words = user_text.lower().split()

        # مقایسه کلمات پاسخ کاربر با متن اصلی
        for correct_word, user_word in zip(
            correct_words, user_words
        ):
            if correct_word == user_word:
                correct_count += 1
            else:
                wrong_count += 1

        # محاسبه کلمات جاافتاده یا اضافه
        wrong_count += abs(
            len(correct_words) - len(user_words)
        )

        # محاسبه امتیاز
        if correct_words:
            score = round(
                (correct_count / len(correct_words)) * 100
            )

        # نمایش پیام نتیجه
        if score == 100:
            result = "عالی! پاسخ کاملاً درست است ✅"
        elif score >= 70:
            result = "خوب بود! چند اشتباه داشتی 🟡"
        else:
            result = "نیاز به تمرین بیشتری داری ❌"

    return render(
        request,
        "base/dictation.html",
        {
            "dictation": dictation,
            "result": result,
            "score": score,
            "correct_count": correct_count,
            "wrong_count": wrong_count,

            # اطلاعات صفحه‌بندی قبلی
            "previous_dictation": previous_dictation,
            "next_dictation": next_dictation,
            "page_number": page_number,
            "total_dictations": total_dictations,

            # اطلاعات قالب صفحه‌بندی مشترک
            "page_range": page_range,
            "current_item": current_item,
            "previous_item": previous_item,
            "next_item": next_item,
            "page_url": page_url,
            "previous_url": previous_url,
            "next_url": next_url,
        }
    )
@login_required(login_url='login')
def dictation_audio(request, id):
    dictation = get_object_or_404(Dictation, id=id)
    print("Audio name:", dictation.audio.name)
    print("Audio path:", dictation.audio.path)

    if not dictation.audio:
        raise Http404("فایل صوتی پیدا نشد.")

    return FileResponse(
        dictation.audio.open('rb'),
        content_type='audio/mpeg'
    )






    



def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "ثبت‌نام شما با موفقیت انجام شد."
            )

            return redirect("home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "base/inscription.html",
        {"form": form}
    )


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "نام کاربری یا رمز عبور اشتباه است."

    return render(
        request,
        "base/login.html",
        {"error": error}
    )









@login_required(login_url="login")
def profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = StudentProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = StudentProfileForm(instance=profile)

    return render(
        request,
        "base/profile.html",
        {"form": form, "profile": profile}
    )
# ROOM API
# from .serializers import RoomSerializer
# class RoomApi(generics.ListAPIView):
#     queryset= Room.objects.all()
#     serializer_class=RoomSerializer





@login_required(login_url='login')
def dictation_audio(request, id):
    dictation = get_object_or_404(Dictation, id=id)

    if not dictation.audio:
        from django.http import Http404
        raise Http404("فایل صوتی پیدا نشد.")

    return FileResponse(
        dictation.audio.open('rb'),
        content_type='audio/mpeg'
    )


def reading_list(request):
    passages=ReadingPassage.objects.filter(
        is_published=True

    ).select_related("level", "topic")

    return render(
        request,
        "base/reading_list.html",
        {"passages": passages},
    )




def reading_topic(request):
    passages = ReadingPassage.objects.filter(
        is_published=True
    ).select_related("level", "topic")

    return render(
        request,
        "base/reading_topic.html",
        {"passages": passages},
    )





def reading_detail(request, id):
    passage = get_object_or_404(
        ReadingPassage,
        id=id,
        is_published=True,
    )

    # همه متن‌های منتشرشده، به ترتیب
    page_range = list(
        ReadingPassage.objects.filter(
            is_published=True
        ).order_by("id")
    )

    # شماره متن فعلی
    current_index = next(
        i for i, item in enumerate(page_range)
        if item.id == passage.id
    )

    page_number = current_index + 1
    total_pages = len(page_range)

    # متن قبلی
    previous_item = (
        page_range[current_index - 1]
        if current_index > 0
        else None
    )

    # متن بعدی
    next_item = (
        page_range[current_index + 1]
        if current_index < total_pages - 1
        else None
    )

    # اطلاعات صفحه‌بندی
    current_item = passage
    page_url = "/reading_topic/"
    previous_url = "/reading_topic/"
    next_url = "/reading_topic/"

    # سؤال‌ها
    questions = list(passage.questions.all())
    score = None

    if request.method == "POST":
        score = 0

        for question in questions:
            selected = request.POST.get(
                f"question_{question.id}"
            )

            question.selected_answer = selected
            question.is_correct = (
                selected == question.correct_answer
            )

            if question.is_correct:
                score += 1

    return render(
        request,
        "base/reading_detail.html",
        {
            "passage": passage,
            "questions": questions,
            "score": score,
            "page_range": page_range,
            "page_number": page_number,
            "total_pages": total_pages,
            "current_item": current_item,
            "previous_item": previous_item,
            "next_item": next_item,
            "page_url": page_url,
            "previous_url": previous_url,
            "next_url": next_url,
        },
    )




def dictation_topic(request):
    dictations = Dictation.objects.all().order_by("-created_at")

    context = {
        "dictations": dictations,
    }

    return render(request, "base/dictation_topic.html", context)




def search(request):
    query = request.GET.get("q", "").strip()

    vocabulary_topics = VocabularyTopic.objects.none()
    vocabulary_cards = VocabularyCard.objects.none()
    grammar_topics = GrammarTopic.objects.none()
    grammar_exercises = GrammarExercise.objects.none()
    reading_passages = ReadingPassage.objects.none()
    dictations = Dictation.objects.none()

    if query:
        vocabulary_topics = VocabularyTopic.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(level__name__icontains=query)
        )

        vocabulary_cards = VocabularyCard.objects.filter(
            Q(word__icontains=query) |
            Q(pronunciation__icontains=query) |
            Q(topic__title__icontains=query)
        ).select_related("topic")

        grammar_topics = GrammarTopic.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        grammar_exercises = GrammarExercise.objects.filter(
            Q(question__icontains=query) |
            Q(option_a__icontains=query) |
            Q(option_b__icontains=query) |
            Q(option_c__icontains=query) |
            Q(option_d__icontains=query) |
            Q(explanation__icontains=query) |
            Q(topic__title__icontains=query)
        ).select_related("topic")

        reading_passages = ReadingPassage.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(topic__name__icontains=query) |
            Q(level__name__icontains=query),
            is_published=True,
        ).select_related("level", "topic")

        dictations = Dictation.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(description__icontains=query) |
            Q(level__name__icontains=query)
        ).select_related("level")

    context = {
        "query": query,
        "vocabulary_topics": vocabulary_topics,
        "vocabulary_cards": vocabulary_cards,
        "grammar_topics": grammar_topics,
        "grammar_exercises": grammar_exercises,
        "reading_passages": reading_passages,
        "dictations": dictations,
    }

    return render(request, "base/search_results.html", context)



def article_list(request):
    articles = Article.objects.filter(
        is_published=True
    ).order_by("-created_at")

    return render(
        request,
        "base/article_list.html",
        {"articles": articles}
    )


def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True
    )

    return render(
        request,
        "base/article_detail.html",
        {"article": article}
    )










