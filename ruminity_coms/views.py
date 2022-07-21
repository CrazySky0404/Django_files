from django.shortcuts import render, redirect

from .models import Topic, Subtopic, Entry
from .forms import TopicForm, SubtopicForm, EntryForm


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


def new_topic(request):
    """Створення нової теми."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ruminity_coms:topics')

    context = {'form': form}
    return render(request, 'ruminity_coms/new_topic.html', context)


def new_subtopic(request, topic_id):
    """Створення нової Підтеми."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = SubtopicForm()
    else:
        form = SubtopicForm(data=request.POST)
        if form.is_valid():
            new_subtopic = form.save(commit=False)
            new_subtopic.topic = topic
            new_subtopic.save()
            return redirect('ruminity_coms:subtopics', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'ruminity_coms/new_subtopic.html', context)


def new_entry(request, subtopic_id):
    """Створення нового Допису."""
    subtopic = Subtopic.objects.get(id=subtopic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.subtopic = subtopic
            new_entry.save()
            return redirect('ruminity_coms:subtopic', subtopic_id=subtopic_id)

    context = {'subtopic': subtopic, 'form': form}
    return render(request, 'ruminity_coms/new_entry.html', context)


def edit_entry(request, entry_id):
    """Редагування допису."""
    entry = Entry.objects.get(id=entry_id)
    subtopic = entry.subtopic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ruminity_coms:subtopic', subtopic_id=subtopic.id)

    context = {'entry': entry, 'subtopic': subtopic, 'form': form}
    return render(request, 'ruminity_coms/edit_entry.html', context)