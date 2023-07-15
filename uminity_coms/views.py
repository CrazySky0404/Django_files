"""
This module contains the views for handling HTTP requests and generating responses.
"""
from django.db.models import Count
from django.utils import timezone

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import (
    Topic,
    Subtopic,
    Publication,
    Competition,
    CompetitionSingle,
    Books,
    SubtopicComment,
    View,
    Like,
    Dislike,
    CommentLike,
)

from .forms import (
    TopicForm,
    SubtopicForm,
    PublicationForm,
    NewCommentForm,
    CommentFormForum,
    CommentFormStory,
    LikeForm,
    DislikeForm,
    CommentLikeForm,
)


def index(request):
    """Головна сторінка спільноти."""
    return render(request, "uminity_coms/index.html")


def topics(request):
    """Показати всі теми."""
    all_topics = Topic.objects.all()

    last_comments = {}
    for topic in all_topics:
        last_comment = None
        for subtopic in topic.subtopic_set.all():  # pylint: disable=redefined-outer-name
            subtopic_last_comment = subtopic.comments.order_by("-date_added").first()
            if subtopic_last_comment is not None and (
                last_comment is None or subtopic_last_comment.date_added > last_comment.date_added
            ):
                last_comment = subtopic_last_comment
        if last_comment is not None:
            last_comments[topic.id] = last_comment

    context = {
        "topics": all_topics,
        "last_comments": last_comments,
    }
    return render(request, "uminity_coms/forum/topics.html", context)


def subtopics(request, topic_id):  # pylint: disable=too-many-locals
    """Показати всі підтеми до вибраної теми."""
    topic = Topic.objects.get(id=topic_id)
    subtopics_list = topic.subtopic_set.order_by("-date_added")

    for subtopic in subtopics_list:  # pylint: disable=redefined-outer-name
        subtopic.comment_count = SubtopicComment.objects.filter(subtopic=subtopic).count()
        subtopic.save()

    current_datetime = timezone.now()
    comments_with_time = []

    comments = SubtopicComment.objects.filter(subtopic__in=subtopics_list).order_by("-date_added")[:10]

    for comment in comments:
        comment_date_added = comment.date_added

        time_difference = current_datetime - comment_date_added

        total_seconds = int(time_difference.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60

        if days > 0:
            time_ago = f"{days} днів тому"
        elif hours > 0:
            time_ago = f"{hours} годин тому"
        else:
            time_ago = f"{minutes} хвилин тому"

        comments_with_time.append(
            {
                "comment": comment,
                "time_ago": time_ago,
            }
        )

    context = {
        "topic": topic,
        "subtopics": subtopics_list,
        "comments_time_ago": comments_with_time,
    }
    return render(request, "uminity_coms/forum/topic.html", context)

    page = request.GET.get("page")  # pylint: disable=unreachable
    results = 3
    paginator = Paginator(subtopics_list, results)

    try:
        subtopics_list = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        subtopics_list = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        subtopics_list = paginator.page(page)

    left_index = int(page) - 4

    # if left_index < 1:
    #     left_index = 1
    left_index = max(left_index, 1)

    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    context = {
        "topic": topic,
        "subtopics": subtopics_list,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    return render(request, "uminity_coms/topic.html", context)


def subtopic(request, subtopic_id):
    """Показати вибрану підтему з усіма записами."""
    all_subtopic = get_object_or_404(Subtopic, id=subtopic_id)
    comments = all_subtopic.comments.all()
    topic_comments = all_subtopic.comments.all().order_by("-date_added")[:10]
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)

    subtopic.views += 1
    subtopic.save()

    likes_count = Like.objects.filter(subtopic=subtopic).count()
    dislike_count = Dislike.objects.filter(subtopic=subtopic).count()
    most_liked_comment = SubtopicComment.objects.annotate(like_count=Count('commentlike')).filter(like_count__gte=1).order_by('-like_count').first()
    user_likes = CommentLike.objects.filter(user=request.user, comment__in=comments).values_list('comment_id',
                                                                                                 flat=True)
    form = CommentFormForum()
    like_form = LikeForm()
    dislike_form = DislikeForm()

    if request.method == "POST":
        if 'like_comment_button' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(SubtopicComment, id=comment_id)
            existing_like = CommentLike.objects.filter(user=request.user, comment=comment)
            if existing_like.exists():
                existing_like.first().delete()
            else:
                CommentLike.objects.create(user=request.user, comment=comment)
        if 'like_button' in request.POST:
            existing_like = Like.objects.filter(user=request.user, subtopic=subtopic)
            existing_dislike = Dislike.objects.filter(user=request.user, subtopic=subtopic)
            if existing_like.exists():
                existing_like.first().delete()
            else:
                if existing_dislike.exists():
                    existing_dislike.first().delete()
                Like.objects.create(user=request.user, subtopic=subtopic)
        elif 'dislike_button' in request.POST:
            existing_like = Like.objects.filter(user=request.user, subtopic=subtopic)
            existing_dislike = Dislike.objects.filter(user=request.user, subtopic=subtopic)
            if existing_dislike.exists():
                existing_dislike.first().delete()
            else:
                if existing_like.exists():
                    existing_like.first().delete()
                Dislike.objects.create(user=request.user, subtopic=subtopic)
        elif 'comment_button' in request.POST:
            form = CommentFormForum(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.subtopic = all_subtopic
                if request.user.is_authenticated:
                    new_comment.name = request.user.username
                else:
                    return redirect('users:login')
                if 'parent' in request.POST:
                    try:
                        parent_id = int(request.POST.get('parent'))
                        parent_comment = SubtopicComment.objects.get(id=parent_id)
                        new_comment.parent = parent_comment
                    except:
                        pass
                new_comment.save()
                #comment_id = new_comment.id
                #return HttpResponseRedirect(f"/topic/{subtopic_id}#comment-{comment_id}")
        return HttpResponseRedirect(f"/topic/{subtopic_id}")
    else:
        form = CommentFormForum()

    context = {
        "subtopic": subtopic,
        "comments": comments,
        "form": form,
        "like_form": like_form,
        "dislike_form": dislike_form,
        "most_liked_comment": most_liked_comment,
        "user_likes": user_likes,
        "topic_comments": topic_comments,
        "likes_count": likes_count,
        "dislike_count": dislike_count,
    }
    return render(request, "uminity_coms/forum/subtopic.html", context)


@login_required
def new_topic(request):
    """Створення нової теми."""
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("uminity_coms:topics")

    context = {"form": form}
    return render(request, "uminity_coms/forum/new_topic.html", context)


@login_required
def new_subtopic(request, topic_id):
    """Створення нової Підтеми."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        form = SubtopicForm()
    else:
        form = SubtopicForm(data=request.POST)
        if form.is_valid():
            fresh_subtopic = form.save(commit=False)
            fresh_subtopic.topic = topic
            fresh_subtopic.save()
            return redirect("uminity_coms:subtopics", topic_id=topic_id)

    context = {"topic": topic, "form": form}
    return render(request, "uminity_coms/forum/new_subtopic.html", context)


@login_required
def books(request):
    """Показати список книг."""
    all_books = Books.objects.all()

    context = {
        "blocks": all_books,
    }
    return render(request, "uminity_coms/book/books.html", context)


@login_required
def publications(request):
    """Показати список публікацій."""
    all_publications = Publication.objects.all()

    page = request.GET.get("page")
    results = 3
    paginator = Paginator(all_publications, results)

    try:
        all_publications = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        all_publications = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        all_publications = paginator.page(page)

    left_index = int(page) - 4

    # if left_index < 1:
    #     left_index = 1
    left_index = max(left_index, 1)

    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    context = {
        "publications": all_publications,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    return render(request, "uminity_coms/public/publications.html", context)


@login_required
def publication(request, publication_id):
    """Показати вибрану публікацію."""
    all_publication = get_object_or_404(Publication, id=publication_id)
    comments = all_publication.comments.all()

    new_comment = None

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.publication = all_publication
            new_comment.save()
            return HttpResponseRedirect("/publication/" + f"{publication_id}")
    else:
        form = NewCommentForm()

    context = {
        "publication": all_publication,
        "comments": comments,
        "form": form,
        "new_comment": new_comment,
    }
    return render(request, "uminity_coms/public/publication.html", context)


@login_required
def new_publication(request):
    """Створення нової публікацію."""
    if request.method != "POST":
        form = PublicationForm()
    else:
        form = PublicationForm(data=request.POST)
        if form.is_valid():
            fresh_publication = form.save(commit=False)
            fresh_publication.owner = request.user
            print("TEXT: " + form.cleaned_data["text"])
            print("DESCRIPTION: " + form.cleaned_data["description"])
            fresh_publication.save()
            return redirect("uminity_coms:publications")
    text = "10"
    count_symbol = len(text)

    context = {"form": form, "count_symbol": count_symbol}
    return render(request, "uminity_coms/public/new_publication.html", context)


@login_required
def edit_publication(request, publication_id):
    """Редагування допису."""
    all_publication = Publication.objects.get(id=publication_id)

    if all_publication.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = PublicationForm(instance=all_publication)
    else:
        form = PublicationForm(instance=all_publication, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("uminity_coms:publication", publication_id=all_publication.id)

    context = {"publication": all_publication, "form": form}
    return render(request, "uminity_coms/public/edit_publication.html", context)


@login_required
def competitions(request):
    """Показати всі конкурси."""
    all_competitions = Competition.objects.all()

    context = {"competitions": all_competitions}
    return render(request, "uminity_coms/comps/competitions.html", context)


@login_required
def stories(request, competition_slug):
    """Показати всі твори до вибраного конкурсу."""
    competition = get_object_or_404(Competition, slug=competition_slug)

    list_stories = competition.single.order_by("-date_added")
    context = {"list_stories": list_stories, "competition": competition}
    return render(request, "uminity_coms/comps/list_competitions.html", context)


@login_required
def post(request, competition_slug, post):  # pylint: disable=redefined-outer-name
    """Показати окрему роботу до вибраного конкурсу."""
    post = get_object_or_404(CompetitionSingle, slug=post, competition__slug=competition_slug)
    comments = post.comments.all()

    new_comment = None

    if request.method == "POST":
        form = CommentFormStory(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.story = post  # змінено з new_comment.post на new_comment.story
            new_comment.save()
            return redirect(
                "uminity_coms:post",
                competition_slug=post.competition.slug,
                post=post.slug,
            )
    else:
        form = CommentFormStory()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "new_comment": new_comment,
    }
    return render(request, "uminity_coms/comps/post.html", context)


def my_account(request):
    """Відображає профіль користувача."""
    return render(request, "uminity_coms/profile/my_account.html")
