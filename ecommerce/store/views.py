from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import csv, io
from .forms import CreateUserForm, LoginForm, UserAdminCreationForm
from .models import *
from django.http import JsonResponse
import requests
import json
from django.contrib.auth import logout
from pprint import pprint



# Create your views here.

# from django.http import HttpResponse
# from ecommerce.ecommerce.store.forms import UserAdminCreationForm
# from ecommerce.ecommerce.store.forms import UserAdminCreationForm

def store(request):

    if request.user.is_authenticated:
        items = request.user.cartdetail_set.all()
        cart = Cart.objects.get(user_id_id=request.user.id)
        # cartItems = CustomUser.get_cart_items

    else:
        items = []
        cart={'get_cart_total':0, 'get_cart_items':0}
        # cartItems = carti['get_cart_items']
    products = Product.objects.all().order_by('id')[:12]
    context = {'products': products,'cart':request.user}
    return render(request, 'store/store.html', context)

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "store/product_list.html"

class SearchProductView(ListView):
    template_name = 'store/product_list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        #print(request.GET)
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()


def cart(request):
    if request.user.is_authenticated:
        items = request.user.cartdetail_set.all()
        cart = Cart.objects.get(user_id_id=request.user.id)
        # cartItems = CustomUser.get_cart_items

    else:
        items = []
        cart=[]
        # carti = {'get_cart_total': 0, 'get_cart_items': 0}
        # cartItems = carti['get_cart_items']

    context = {'items': items, 'cart':request.user,}
    return render(request, 'store/cart.html', context)
    # if request.user.is_authenticated:
    #     username = request.user.id
    #     cart, created = Cart.objects.get_or_create(user_id_id=username)
    #     items=cart.cartdetails_set.all()
    #     return items
    #     # cart_objj= Cart.objects.filter(user_id_id=username).all()
    #     # return cart_objj
    #     # cart_obj = CartDetail.objects.filter(user_id_id=cart_objj.user_id_id).all()
    #     # return cart_obj.products.all()
    #     # context = {'cart': cart_obj}
    #
    #     #return render(request, 'store/cart.html', context)
    # else:
    #     items = []
    #     context = {'items': items}
    #     return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        items = request.user.cartdetail_set.all()
        cart = Cart.objects.get(user_id_id=request.user.id)
        # cartItems = CustomUser.get_cart_items

    else:
        items = []
        cart = []
        # carti = {'get_cart_total': 0, 'get_cart_items': 0}
        # cartItems = carti['get_cart_items']

    context = {'items': items, 'cart': request.user,}
    return render(request, 'store/checkout.html', context)


def main(request):
    context = {}
    return render(request, 'store/main.html', context)


def register(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            email = form.cleaned_data.get('email')
            messages.success(request, 'Acccount was created for', email)
            return redirect('login')
    return render(request, 'store/register.html', {'form': form})


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    print("User logged in")
    # print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)

        # print(request.user.is_authenticated())
        if user is not None:
            # print(request.user.is_authenticated())
            login(request, user)
            # Redirect to a success page.
            context['form'] = LoginForm()
            return redirect("/")
        else:
            # Return an 'invalid login' error message.
            return redirect("/error")

    return render(request, "store/login.html", context)


# @permission_required('admin.can_add_log_entry')
def shop_upload(request):
    template = "store/shop_upload.html"
    # data = Shop.objects.all()
    prompt = {
        'order': 'Order of the CSV should be id, name, description, slug, profile_pic, email, address, phone, active, '
                 'pickup, delivery '
        # 'profiles': data

    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Shop.objects.update_or_create(
            id=column[0],
            name=column[1],
            description=column[2],
            slug=column[3],
            profile_pic=column[4],
            email=column[5],
            address=column[6],
            phone=column[7],
            active=column[8],
            pickup=column[9],
            delivery=column[10]
        )
    context = {}
    return render(request, template, context)


def category_upload(request):
    template = "store/category_upload.html"
    # data = Shop.objects.all()
    prompt = {
        'order': 'Order of the CSV should be id, name, slug, description'
        # 'profiles': data

    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Category.objects.update_or_create(
            id=column[0],
            name=column[1],
            slug=column[2],
            description=column[3],
        )
    context = {}
    return render(request, template, context)


def product_upload(request):
    template = "store/product_upload.html"
    # data = Shop.objects.all()
    prompt = {
        'order': 'Order of the CSV should be id, name, description, selling_price, actual_price, unit, '
                 'category_id_id, shop_id_id, slug '

        # 'profiles': data

    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Product.objects.update_or_create(
            id=column[0],
            name=column[1],
            description=column[2],
            selling_price=column[3],
            actual_price=column[4],
            unit=column[5],
            category_id_id=column[6],
            shop_id_id=column[7],
            slug=column[8],
        )
    context = {}
    return render(request, template, context)


def customuser_upload(request):
    template = "store/customuser_upload.html"
    # data = Shop.objects.all()
    prompt = {
        'order': 'Order of the CSV should be id, password, is_superuser, first_name, last_name, is_staff, '
                 'is_active, email, address, profile_pic, slug, phone'
        # 'profiles': data

    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = CustomUser.objects.update_or_create(
            id=column[0],
            password=column[1],
            # last_login=column[2],
            is_superuser=column[3],
            first_name=column[4],
            last_name=column[5],
            is_staff=column[6],
            is_active=column[7],
            # date_joined=column[8],
            email=column[9],
            address=column[10],
            profile_pic=column[11],
            slug=column[12],
            phone=column[13],

        )
    context = {}
    return render(request, template, context)


def cartdetail_upload(request):
    template = "store/cartdetail_upload.html"
    # data = Shop.objects.all()
    prompt = {
        'order': 'Order of the CSV should be id, product_id_id, user_id_id, quantity'
        # 'profiles': data

    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = CartDetail.objects.update_or_create(
            id=column[0],
            product_id_id=column[1],
            user_id_id=column[2],
            quantity=column[3],

        )
    context = {}
    return render(request, template, context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId:', productId)
    print('Action:', action)

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user_id_id=request.user.id)
    cartItem, created = CartDetail.objects.get_or_create(user_id_id=request.user.id, product_id=product)

    if action == 'add':
        cartItem.quantity = cartItem.quantity+1
    elif action == 'remove':
        cartItem.quantity = cartItem.quantity-1

    cartItem.save()

    if(cartItem.quantity<=0):
        cartItem.delete()
    return JsonResponse('Item was added', safe=False)


def logout_page(request):
    logout(request)
    return redirect("/main")

def login_page_new(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    print("User logged in")
    # print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)

        # print(request.user.is_authenticated())
        if user is not None:
            # print(request.user.is_authenticated())
            login(request, user)
            # Redirect to a success page.
            context['form'] = LoginForm()
            return redirect("/")
        else:
            # Return an 'invalid login' error message.
            return redirect("/error")

    return render(request, "store/login.html", context)
