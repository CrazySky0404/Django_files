from itertools import chain

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Subtopic, Entry, Publication
from .forms import TopicForm, SubtopicForm, EntryForm


def index(request):
    """Головна сторінка спільноти."""
    return render(request, 'ruminity_coms/index.html')


def topics(request):
    """Відображає всі теми."""
    topics = Topic.objects.all()
    sumen = {}
    last_entries = {}
    entry3 =[]
    entry4 =[]
    dict_topic_text = {}
    dict_entry_text = {}

    for topic in topics:
        subtopics = Subtopic.objects.filter(topic__text=topic).order_by('-id')
        list_entry = []
        list_entry_id_2 = []
        dict_topic_text1 = {topic.id: topic.text}

        for subtopic in subtopics:
            entries = Entry.objects.filter(subtopic__text=subtopic).order_by('-id')[:1]
            if not entries:
                pass
            else:
                list_entry.append(entries)
                for entry in Entry.objects.filter(subtopic__text=subtopic).order_by('-id'):
                    list_entry_id_2.append(entry.id)
                    dict_entry_text2 = {entry.id: entry.text}
                    dict_entry_text.update(dict_entry_text2)

            for entry in Entry.objects.filter(subtopic__text=subtopic).order_by('-id'):
                entry1 = entry.text
                entry2 = entry.id
                entry3.append(entry2)
                entry4.append(entry1)
        dict_topic_text.update(dict_topic_text1)

        list_y = sorted(list_entry_id_2)
        for x in list_y:
             last_entries1 = {topic.id: x}

        last_entries.update(last_entries1)

    for topic in topics:
        subtopics2 = Subtopic.objects.filter(topic__text=topic).order_by('-date_added')
        sum_entries = 0
        for subtopic in subtopics2:
            entries = Entry.objects.filter(subtopic__text=subtopic).order_by('-date_added').count()
            sum_entries += entries
            sumen1 = {topic.id: sum_entries}
        sumen.update(sumen1)


    context = {'topics': topics, 'sumen': sumen.items(), 'last_entries': last_entries.items(),
               'dict_entry_text':dict_entry_text.items()}
    return render(request, 'ruminity_coms/topics.html', context)

    for topic in topics:
        subtopics2 = Subtopic.objects.filter(topic__text=topic).order_by('-date_added')
        sum_entries = 0
        for subtopic in subtopics2:
            entries = Entry.objects.filter(subtopic__text=subtopic).order_by('-date_added').count()
            sum_entries += entries
            sumen1 = {topic.id: sum_entries}
        sumen.update(sumen1)
    #for k,value in sumen.items():
        #print(k,value)
    context = {'topics': topics, 'sumen': sumen.items(), 'last_entries': last_entries.items(),
               'dict_entry_text': dict_entry_text, 'list_last': list_last}
    return render(request, 'ruminity_coms/topics.html', context)


def subtopics(request, topic_id):
    """Показати всі підтеми до вибраної теми."""
    topic = Topic.objects.get(id=topic_id)
    subtopics = topic.subtopic_set.order_by('-date_added')
    context = {'topic': topic, 'subtopics': subtopics}
    return render(request, 'ruminity_coms/topic.html', context)


@login_required
def subtopic(request, subtopic_id):
    """Показати вибрану підтему з усіма записами."""
    subtopic = Subtopic.objects.get(id=subtopic_id)
    entries = subtopic.entry_set.order_by('-date_added')
    context = {'subtopic': subtopic, 'entries': entries}
    return render(request, 'ruminity_coms/subtopic.html', context)


@login_required
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


@login_required
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


@login_required
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
            new_entry.owner = request.user
            new_entry.save()
            return redirect('ruminity_coms:subtopic', subtopic_id=subtopic_id)

    context = {'subtopic': subtopic, 'form': form}
    return render(request, 'ruminity_coms/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редагування допису."""
    entry = Entry.objects.get(id=entry_id)
    subtopic = entry.subtopic

    if entry.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ruminity_coms:subtopic', subtopic_id=subtopic.id)

    context = {'entry': entry, 'subtopic': subtopic, 'form': form}
    return render(request, 'ruminity_coms/edit_entry.html', context)


@login_required
def publications(request):
    """Показати список публікацій."""
    publications = Publication.objects.all()
    context = {'publications': publications, }
    return render(request, 'ruminity_coms/publications.html', context)


@login_required
def publication(request, publication_id):
    """Показати вибрану публікацію."""
    publication = Publication.objects.get(id=publication_id)
    context = {'publication': publication, }
    return render(request, 'ruminity_coms/publication.html', context)



