from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    return render(request, 'notebooks/index.html')

@login_required
def topics(request):
    """Sows all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'notebooks/topics.html', context)

@login_required
def topic(request, topic_id):
    """Shows a single topic and its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(topic.owner, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'notebooks/topic.html', context)

@login_required
def new_topic(request):
    """Adds new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('notebooks:topics'))
    
    context = {'form': form}
    return render(request, 'notebooks/new_topic.html', context)

@login_required
def delete_topic(request, topic_id):
    """Deletes a specific topic."""
    topic = Topic.objects.get(id=topic_id)
    topic.delete()
    context = {'topic': topic}
    return render(request, 'notebooks/delete_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adds a new entry to a specific topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner, request)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('notebooks:topic',
                                        args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'notebooks/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edits an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic.owner, request)

    if request.method != 'POST':
        # Pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('notebooks:topic', 
                                        args=[topic.id]))
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'notebooks/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """Deletes a specific entry."""
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    context = {'entry': entry}
    return render(request, 'notebooks/delete_entry.html', context)

def check_topic_owner(owner, request):
    """Makes sure user associated with a topic
    matches the currently logged in user."""
    if owner != request.user:
        raise Http404
