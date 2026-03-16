from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

from .models import Post
from .forms import CommentForm, EmailPostForm
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            print(cd)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            title = f"{cd['name']} sizga {post.title} ni o'qishini taklif etadi."
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(title, message, 'akbarboy77777@gmail.com', [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                                             'form': form,
                                                                             'sent': sent,})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post.published, slug=slug, created_at__year=year, created_at__month=month,
                             created_at__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'new_comment': new_comment
                   })
