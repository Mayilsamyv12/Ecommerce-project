
# Create your views here.
from django.shortcuts import render , redirect , HttpResponseRedirect , get_object_or_404
from django.views import View
from store.models import Products
from django.contrib.auth.hashers import check_password
from store.models import Order
from django.contrib.auth.hashers import make_password
from store.models import Customer
from store.models import Category
from store.models import Feedback



class Cart(View):
    def get(self , request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
            cart = {}
        ids = list(cart.keys())
        products = Products.get_products_by_id(ids)
        return render(request , 'cart.html' , {'products' : products} )
    
class CheckOut(View):
    def post(self, request):
        name = request.POST.get('name')
        house_no = request.POST.get('house_no')
        area = request.POST.get('area')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        
        address = f"Name: {name}, {house_no}, {area}, Near {landmark}, {city} - {pincode}"
        
        # Save to session instead of DB
        request.session['checkout_data'] = {
            'address': address,
            'phone': phone,
        }
        return redirect('payment')

class Payment(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            return redirect('store')
        
        products = Products.get_products_by_id(list(cart.keys()))
        total = 0
        for product in products:
            total += product.price * cart.get(str(product.id))
            
        return render(request, 'payment.html', {'total': total})

class PlaceOrder(View):
    def post(self, request):
        try:
            checkout_data = request.session.get('checkout_data')
            customer_id = request.session.get('customer')
            cart = request.session.get('cart')
            
            if not checkout_data:
                return redirect('cart')
                
            if not customer_id:
                return redirect('login')
                
            products = Products.get_products_by_id(list(cart.keys()))
            
            for product in products:
                 order = Order(customer=Customer(id=customer_id),
                              product=product,
                              price=product.price,
                              address=checkout_data.get('address', ''),
                              phone=checkout_data.get('phone', ''),
                              quantity=cart.get(str(product.id)),
                              delivery_status='Placed')
                 order.save()
            
            request.session['cart'] = {}
            request.session['checkout_data'] = {}
            return render(request, 'order_success.html')
        except:
             return redirect('cart')
    
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        clear = request.POST.get('clear')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if clear:
                    cart.pop(product)
                elif remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        
        return_url = request.POST.get('return_url')
        if return_url:
             return redirect(return_url)
             
        return redirect('homepage')



    def get(self , request):

        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        # Check if category is ID (digit)
        if str(categoryID).isdigit():
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            # Fallback for name-based lookup
            try:
                # 1. Try exact match first
                cat = Category.objects.get(name__iexact=categoryID)
                products = Products.get_all_products_by_categoryid(cat.id)
            except Category.DoesNotExist:
                # 2. Try fuzzy matching for legacy/friendly names
                query = str(categoryID).lower()
                cat = None
                
                # Map common terms to DB names
                if query in ['men', 'man']:
                     # "Men Clothing"
                     cat = Category.objects.filter(name__icontains='Men').exclude(name__icontains='Women').first()
                elif query in ['women', 'woman']:
                     # "Womens Clothing"
                     cat = Category.objects.filter(name__icontains='Women').first()
                elif query in ['kids', 'kid']:
                     # "Kids Clothing"
                     cat = Category.objects.filter(name__icontains='Kid').first()
                
                if cat:
                    products = Products.get_all_products_by_categoryid(cat.id)
                else:
                    products = []
    else:
        products = Products.get_all_products()
        # Group products by category for the home page sections
        products_by_category = []
        for category in categories:
            category_products = Products.get_all_products_by_categoryid(category.id)
            if category_products:
                products_by_category.append((category, category_products))

    data = {}
    data['products'] = products
    data['categories'] = categories
    # Add the grouped data to the context
    if 'products_by_category' in locals():
        data['products_by_category'] = products_by_category

    return render(request, 'index.html', data)

class Login(View):
    return_url = None

    def get(self, request):
        request.session['return_url'] = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                return_url = request.session.get('return_url')
                if return_url:
                    request.session['return_url'] = None
                    return HttpResponseRedirect(return_url)
                else:
                    return redirect('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request , 'orders.html'  , {'orders' : orders})

class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

from store.models import Category
from store.models import Feedback

# ... existing imports ...

from django.db.models import Avg

# ... imports ...

class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Products, id=pk)
        categories = Category.get_all_categories()
        reviews = Feedback.get_reviews_by_product(pk)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        # Check if user can review
        can_review = False
        customer_id = request.session.get('customer')
        if customer_id:
            # Check for delivered order
            orders = Order.objects.filter(customer=customer_id, product=product, delivery_status='Delivered')
            if orders.exists():
                can_review = True
        
        return render(request, 'product_detail.html', {
            'product': product, 
            'categories': categories,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'can_review': can_review
        })

class SubmitReview(View):
    def post(self, request):
        product_id = request.POST.get('product')
        customer_id = request.session.get('customer')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if customer_id:
            product = Products.objects.get(id=product_id)
            customer = Customer.objects.get(id=customer_id)
            
            # Verify purchase and delivery again for security
            orders = Order.objects.filter(customer=customer, product=product, delivery_status='Delivered')
            if orders.exists():
                feedback = Feedback(customer=customer, product=product, rating=rating, comment=comment)
                feedback.save()
        
        return redirect('product_detail', pk=product_id)

class Profile(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        if not customer_id:
            return redirect('login')
        customer = Customer.objects.get(id=customer_id)
        return render(request, 'profile.html', {'customer': customer})

    def post(self, request):
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id)
        postData = request.POST
        customer.first_name = postData.get('firstname')
        customer.last_name = postData.get('lastname')
        customer.phone = postData.get('phone')
        
        customer.save()
        customer.save()
        return render(request, 'profile.html', {'customer': customer, 'success': 'Profile Updated Successfully'})

class ChangePassword(View):
    def post(self, request):
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id)
        postData = request.POST
        old_password = postData.get('old_password')
        new_password = postData.get('new_password')
        
        if check_password(old_password, customer.password):
            customer.password = make_password(new_password)
            customer.save()
            return render(request, 'profile.html', {'customer': customer, 'success': 'Password Changed Successfully'})
        else:
            return render(request, 'profile.html', {'customer': customer, 'error': 'Old Password Does Not Match'})


def search(request):
    query = request.GET.get('query')
    if query:
        products = Products.objects.filter(name__icontains=query) | Products.objects.filter(description__icontains=query) | Products.objects.filter(category__name__icontains=query)
    else:
        products = Products.get_all_products()
    
    categories = Category.get_all_categories()
    data = {
        'products': products,
        'categories': categories,
        'query': query
    }
    return render(request, 'search.html', data)




def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    return render(request, 'contact.html')

def licence(request):
    return render(request, 'licence.html')
