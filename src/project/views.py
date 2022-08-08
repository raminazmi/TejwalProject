from django.shortcuts import render

def handler_404(request,exception):
    return render(request,'home/404.html')

