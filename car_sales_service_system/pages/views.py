from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')	
	
def listing(request, productId):
    try:
        productlist =  product.objects.filter(Q(product_level=productId))
    except Exception, e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))

    context = {
        "showmsg": True,
        "message": "User Updated Successfully",
        "productlist": productlist
    }	
	    # Message according Users Role #
    if(productId == "1"):
        context['heading'] = "Product Report";
    return render(request,'product-report.html',context)
	