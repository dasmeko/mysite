from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new_or_edit(request, **kwargs):
    if len(kwargs):
        edit = True
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
    else:
        edit = False
    
    if request.method == "POST":
        if edit:
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        if edit:
            form = PostForm(instance=post)
        else:
            form = PostForm()
    
    return render(request, 'blog/post_edit.html', {'form': form})
    