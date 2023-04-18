from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from .models import Topic, Subtopic, Publication, Competition, CompetitionSingle
from .forms import TopicForm, SubtopicForm, PublicationForm, NewCommentForm, CommentFormForum, CommentFormStory


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

        list_y = sorted(list_entry_id_2)
        for x in list_y:
             last_entries1 = {topic.id: x}


    context = {'topics': topics, 'sumen': sumen.items(), 'last_entries': last_entries.items(),
               'dict_entry_text':dict_entry_text.items()}
    return render(request, 'ruminity_coms/topics.html', context)

    # for topic in topics:
    #     subtopics2 = Subtopic.objects.filter(topic__text=topic).order_by('-date_added')
    #     sum_entries = 0
    #     for subtopic in subtopics2:
    #         entries = Entry.objects.filter(subtopic__text=subtopic).order_by('-date_added').count()
    #         sum_entries += entries
    #         sumen1 = {topic.id: sum_entries}
    #     sumen.update(sumen1)

    # context = {'topics': topics, 'sumen': sumen.items(), 'last_entries': last_entries.items(),
    #            'dict_entry_text': dict_entry_text, 'list_last': list_last}
    # return render(request, 'ruminity_coms/topics.html', context)


def subtopics(request, topic_id):
    """Показати всі підтеми до вибраної теми."""
    topic = Topic.objects.get(id=topic_id)
    subtopics = topic.subtopic_set.order_by('-date_added')

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(subtopics, results)

    try:
        subtopics = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        subtopics = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        subtopics = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    context = {'topic': topic, 'subtopics': subtopics, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'ruminity_coms/topic.html', context)


@login_required
def subtopic(request, subtopic_id):
    """Показати вибрану підтему з усіма записами."""
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)
    comments = subtopic.comments.all()

    if request.method != 'POST':
        form = CommentFormForum()
    else:
        form = CommentFormForum(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.subtopic = subtopic
            new_comment.save()
            return HttpResponseRedirect('/topic/' + f'{subtopic_id}')

    context = {'subtopic': subtopic, 'comments': comments, 'form': form}
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


# @login_required
# def new_entry(request, subtopic_id):
#     """Створення нового Допису."""
#     subtopic = Subtopic.objects.get(id=subtopic_id)
#     if request.method != 'POST':
#         form = EntryForm()
#     else:
#         form = EntryForm(data=request.POST)
#         if form.is_valid():
#             new_entry = form.save(commit=False)
#             new_entry.subtopic = subtopic
#             new_entry.owner = request.user
#             new_entry.save()
#             return redirect('ruminity_coms:subtopic', subtopic_id=subtopic_id)
#
#     context = {'subtopic': subtopic, 'form': form}
#     return render(request, 'ruminity_coms/new_entry.html', context)


# @login_required
# def edit_entry(request, entry_id):
#     """Редагування допису."""
#     entry = Entry.objects.get(id=entry_id)
#     subtopic = entry.subtopic
#
#     if entry.owner != request.user:
#         raise Http404
#
#     if request.method != 'POST':
#         form = EntryForm(instance=entry)
#     else:
#         form = EntryForm(instance=entry, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('ruminity_coms:subtopic', subtopic_id=subtopic.id)
#
#     context = {'entry': entry, 'subtopic': subtopic, 'form': form}
#     return render(request, 'ruminity_coms/edit_entry.html', context)


@login_required
def publications(request):
    """Показати список публікацій."""
    publications = Publication.objects.all()

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(publications, results)

    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        publications = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        publications = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    context = {'publications': publications, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'ruminity_coms/publications.html', context)


@login_required
def publication(request, publication_id):
    """Показати вибрану публікацію."""
    publication = get_object_or_404(Publication, id=publication_id)
    comments = publication.comments.all()

    new_comment = None

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.publication = publication
            new_comment.save()
            return HttpResponseRedirect('/publication/' + f'{publication_id}')
    else:
        form = NewCommentForm()

    context = {'publication': publication, 'comments': comments, 'form': form, 'new_comment': new_comment}
    return render(request, 'ruminity_coms/publication.html', context)


@login_required
def new_publication(request):
    """Створення нової публікацію."""
    if request.method != 'POST':
        form = PublicationForm()
    else:
        form = PublicationForm(data=request.POST)
        if form.is_valid():
            new_publication = form.save(commit=False)
            new_publication.owner = request.user
            print("TEXT: " + form.cleaned_data["text"])
            print("DESCRIPTION: " + form.cleaned_data["description"])
            new_publication.save()
            return redirect('ruminity_coms:publications')
    text = "10"
    count_symbol = len(text)

    context = {'form': form, 'count_symbol': count_symbol}
    return render(request, 'ruminity_coms/new_publication.html', context)


@login_required
def edit_publication(request, publication_id):
    """Редагування допису."""
    publication = Publication.objects.get(id=publication_id)

    if publication.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = PublicationForm(instance=publication)
    else:
        form = PublicationForm(instance=publication, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ruminity_coms:publication', publication_id=publication.id)

    context = {'publication': publication, 'form': form}
    return render(request, 'ruminity_coms/edit_publication.html', context)


@login_required
def competitions(request):
    """Показати всі конкурси."""
    competitions = Competition.objects.all()

    context = {'competitions': competitions}
    return render(request, 'ruminity_coms/competitions.html', context)


#@login_required
# def stories(request, competition_slug):
#     """Показати всі твори до вибраного конкурсу."""
#     competition = get_object_or_404(Competition, slug=competition_slug)
#
#     list_stories = stories.single.order_by('-date_added')
#     context = {'list_stories': list_stories, 'competition': competition}
#     return render(request, 'ruminity_coms/list_competitions.html', context)
@login_required
def stories(request, competition_slug):
    """Показати всі твори до вибраного конкурсу."""
    competition = get_object_or_404(Competition, slug=competition_slug)

    list_stories = competition.single.order_by('-date_added')
    context = {'list_stories': list_stories, 'competition': competition}
    return render(request, 'ruminity_coms/list_competitions.html', context)



@login_required
def post(request, competition_slug, post):
    """Показати окрему роботу до вибраного конкурсу."""
    post = get_object_or_404(CompetitionSingle, slug=post, competition__slug=competition_slug)
    comments = post.comments.all()

    new_comment = None

    if request.method == 'POST':
        form = CommentFormStory(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('ruminity_coms:post', competition_slug=post.competition.slug, post=post.slug)
    else:
        form = CommentFormStory()

    context = {'post': post, 'comments': comments, 'form': form, 'new_comment': new_comment}
    return render(request, 'ruminity_coms/post.html', context)

