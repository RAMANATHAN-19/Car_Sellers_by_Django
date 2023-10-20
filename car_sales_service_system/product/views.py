from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'login.html')

# Create your views here.
def productlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM product_product")
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }
    context['heading'] = "All Product Record";
    return render(request,'product-record.html', context)

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product_product WHERE product_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def update(request, productId):
    context = {
        "fn": "update",
        "productdetails": getData(productId),
        "heading": 'Product Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE product_product
		   SET product_name=%s, product_cost=%s, product_type=%s, product_company=%s,
		   product_stock=%s WHERE product_id=%s""", (
            request.POST['product_name'],
            request.POST['product_cost'],
            request.POST['product_type'],
            request.POST['product_company'],            
            request.POST['product_stock'],
            productId
        ))
        context["productdetails"] =  getData(productId)
        messages.add_message(request, messages.INFO, "Product updated succesfully !!!")
        return redirect('productlisting')
    else:
        return render(request, 'product-add.html', context)

def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Product'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO product_product
		   SET product_name=%s, product_cost=%s, product_type=%s, product_company=%s,
		   product_stock=%s
		""", (
            request.POST['product_name'],
            request.POST['product_cost'],
            request.POST['product_type'],
            request.POST['product_company'],            
            request.POST['product_stock']))
        return redirect('productlisting')
    return render(request, 'product-add.html', context)



def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM product_product WHERE product_id=' + id
    cursor.execute(sql)
    return redirect('productlisting')
