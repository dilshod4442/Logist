from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .models import Topic, TopicProgress, Lecture, PracticeTask
from materials.models import Material
def home(request):
    topics = Topic.objects.published().select_related("section")[:6]
    progress = None
    if request.user.is_authenticated:
        completed = TopicProgress.objects.filter(user=request.user).count()
        total = Topic.objects.published().count()
        progress = {"completed": completed, "total": total, "percent": round(completed / total * 100) if total else 0}
    return render(request, "courses/home.html", {"topics": topics, "progress": progress, "recent_materials": Material.objects.filter(status="published", is_public=True).select_related("topic")[:4]})
def about(request): return render(request, "courses/about.html")
def topic_list(request):
    q, section = request.GET.get("q", "").strip(), request.GET.get("section", "")
    topics = Topic.objects.published().select_related("section")
    if q: topics = topics.filter(Q(title__icontains=q) | Q(summary__icontains=q))
    if section: topics = topics.filter(section_id=section)
    from .models import Section
    return render(request, "courses/topic_list.html", {"topics": topics, "sections": Section.objects.all(), "q": q, "selected_section": section})
def topic_detail(request, slug):
    topic = get_object_or_404(Topic.objects.published().select_related("section").prefetch_related("lectures", "practice_tasks", "materials", "videos", "quizzes"), slug=slug)
    completed = request.user.is_authenticated and TopicProgress.objects.filter(user=request.user, topic=topic).exists()
    return render(request, "courses/topic_detail.html", {"topic": topic, "completed": completed})
@login_required
def toggle_complete(request, slug):
    if request.method != "POST": return HttpResponseForbidden()
    topic = get_object_or_404(Topic.objects.published(), slug=slug)
    progress, created = TopicProgress.objects.get_or_create(user=request.user, topic=topic)
    if not created: progress.delete()
    return redirect(topic.get_absolute_url())
def lectures(request):
    entries = Lecture.objects.filter(published=True, topic__status="published").select_related("topic")
    return render(request, "courses/lectures.html", {"lectures": entries})
def practice(request):
    entries = PracticeTask.objects.filter(published=True, topic__status="published").select_related("topic")
    return render(request, "courses/practice.html", {"tasks": entries})
