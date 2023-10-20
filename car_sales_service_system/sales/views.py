from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.


def order_details(request, id):
    context = {}
    context['orderItems'] = getOrderItems(id)
    context['order_details'] = getProductDetails(id)
    context['total_cost'] = getTotal(id)

    # Message according Sales #
    context['heading'] = "Sales Details";
    return render(request, 'sales-details.html', context)

def saleslisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM `order`")
    saleslist = dictfetchall(cursor)

    context = {
        "saleslist": saleslist
    }

    # Message according Sales #
    context['heading'] = "Sales Details";
    return render(request, 'sales-view.html', context)

def getOrderItems(orderID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM `order`, order_item, product_product WHERE product_id = oi_product_id AND oi_order_id = order_id AND order_id = "+str(orderID))
    return dictfetchall(cursor)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;


def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales WHERE sales_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];


def add(request):
    if (request.method == "POST"):
        if(request.POST['act'] == "create_order"):
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO `order`
            SET order_customer_name=%s, order_customer_mobile=%s, order_date=%s		   
            """, (
                request.POST['order_customer_name'],
                request.POST['order_customer_mobile'],
                'ddddd'))
            messages.add_message(request, messages.INFO, "Item added to cart successfully !!!")
            request.session['order_id'] = cursor.lastrowid
        elif(request.POST['act'] == "save_order"):
            orderID = request.session['order_id']
            request.session['order_id'] = 0
            return redirect('order_details', id=orderID)
        else:
            cursor = connection.cursor()
            product_cost = getProductCost(request.POST['oi_product_id'])
            cursor.execute("""
            INSERT INTO order_item
            SET oi_order_id=%s, oi_product_id=%s, oi_cost=%s		   
            """, (
                request.POST['oi_order_id'],
                request.POST['oi_product_id'],
                product_cost))
            messages.add_message(request, messages.INFO, "Item added to cart successfully !!!")

    context = {
        "fn": "add",
        "producttypelist": getDropDown('product_product', 'product_id'),
        "heading": 'Sales Details'
    }
    if(request.session.get('order_id')):
      context['orderItems'] = getOrderItems(request.session.get('order_id'))
      context['order_details'] = getProductDetails(request.session['order_id'])
      context['total_cost'] = getTotal(request.session['order_id'])
      context['order_id'] = request.session['order_id']
    
    return render(request, 'sales.html', context)


def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM sales WHERE sales_id=' + id
    cursor.execute(sql)
    return redirect('saleslisting')

def getProductCost(productId):
    cursor = connection.cursor()
    cursor.execute("SELECT product_cost FROM product_product WHERE product_id = " + str(productId))
    dataList = dictfetchall(cursor)
    return dataList[0]['product_cost']

def getTotal(orderID):
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(oi_cost) as `Total` FROM order_item WHERE oi_order_id = " + str(orderID))
    dataList = dictfetchall(cursor)
    return dataList[0]['Total']

def getProductDetails(orderID):
    if(orderID):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `order` WHERE order_id = " + str(orderID))
        dataList = dictfetchall(cursor)
        return dataList[0]

def delete_oi(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM order_item WHERE oi_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Item deleted successfully !!!")
    return redirect('add')
