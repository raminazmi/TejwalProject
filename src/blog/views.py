from django.shortcuts import render
from .models import Post , PartsPost
# Create your views here.
def Articles(request):
    posts = Post.objects.all()
    context = {'articles':posts}
    return render(request, 'blog/articles.html',context)

def GetArticle(request,slug):
    post = Post.objects.get(slug=slug);
    Parts = PartsPost.objects.filter(post__slug = slug);
    posts = Post.objects.all()[:4]

    context = {'post':post,
               'parts':Parts,
               'articles':posts}
    
    return render(request , 'blog/article.html',context)
    