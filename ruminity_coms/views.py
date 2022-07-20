from django.shortcuts import render

from .models import Topic, Subtopic


def index(request):
    """Головна сторінка спільноти."""
    return render(request, 'ruminity_coms/index.html')


def topics(request):
    """Відображає всі теми."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'ruminity_coms/topics.html', context)


def subtopics(request, topic_id):
    """Показати всі підтеми до вибраної теми."""
    topic = Topic.objects.get(id=topic_id)
    subtopics = topic.subtopic_set.order_by('-date_added')
    context = {'topic': topic, 'subtopics': subtopics}
    return render(request, 'ruminity_coms/topic.html', context)


def subtopic(request, subtopic_id):
    """Показати вибрану підтему з усіма записами."""
    subtopic = Subtopic.objects.get(id=subtopic_id)
    entries = subtopic.entry_set.order_by('-date_added')
    context = {'subtopic': subtopic, 'entries': entries}
    return render(request, 'ruminity_coms/subtopic.html', context)