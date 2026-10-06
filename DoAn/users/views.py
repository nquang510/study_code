from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, ForgotPasswordForm, ResetPasswordForm
from .models import Product, Category, Brand, History
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os, time
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            user.is_superuser = False
            user.is_staff = False

            user.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = get_user_model().objects.filter(email__iexact=email, is_active=True)

            try:
                for user in users:
                    gui_mail_quen_mat_khau(request, user)
            except Exception as e:
                messages.error(request, f"Gửi mail thất bại: {e}")
                return render(request, "forgot_password.html", {"form": form})

            messages.success(request, "Đã gửi link đặt lại mật khẩu, vui lòng kiểm tra email của bạn.")
            return redirect("forgot_password")
    else:
        form = ForgotPasswordForm()
    return render(request, "forgot_password.html", {"form": form})


def gui_mail_quen_mat_khau(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = request.build_absolute_uri(reverse("reset_password", args=[uid, token]))

    subject = "Đặt lại mật khẩu - E-Shopper"
    text_content = f"Chào {user.username}, click vào link sau để đặt lại mật khẩu: {link}"
    html_content = render_to_string("emails/reset_password_email.html", {
        "user": user,
        "link": link,
    })

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def reset_password_view(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, "reset_password.html", {"link_hop_le": False})

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            messages.success(request, "Đổi mật khẩu thành công, vui lòng đăng nhập lại.")
            return redirect("login")
    else:
        form = ResetPasswordForm()
    return render(request, "reset_password.html", {"form": form, "link_hop_le": True})


def custom_logout(request):
    logout(request)
    return redirect("login")


@login_required
def index(request):
    return render(request, 'index.html')



@login_required
def account_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Update successfully!")
            return redirect("account_update")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "account.html", {"form": form})

@login_required
def add_product(request):
    return render(request, "add_product.html", {
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
    })


@login_required
def my_product(request):
    products = Product.objects.filter(id_user=request.user).order_by("-id")
    return render(request, "my_product.html", {"products": products})



@login_required
@require_POST
def add_product_ajax(request):
    name    = (request.POST.get("name") or "").strip()
    price   = (request.POST.get("price") or "").strip()
    status  = request.POST.get("status") or "0"
    sale    = request.POST.get("sale") or "0"
    company = (request.POST.get("company") or "").strip()
    detail  = (request.POST.get("detail") or "").strip()
    id_category = request.POST.get("id_category")
    id_brand    = request.POST.get("id_brand")

    files = request.FILES.getlist("images")
    errors = {}

    if not name:
        errors["name"] = "Tên sản phẩm không được để trống."
    if not price:
        errors["price"] = "Giá không được để trống."
    if not id_category:
        errors["id_category"] = "Vui lòng chọn category."
    if not id_brand:
        errors["id_brand"] = "Vui lòng chọn brand."

    if not files:
        errors["images"] = "Phải chọn ít nhất một ảnh."
    elif len(files) > 3:
        errors["images"] = "Tối đa chỉ được upload 3 hình."
    else:
        for f in files:
            if f.content_type not in ["image/jpeg", "image/png"]:
                errors["images"] = f"{f.name} không phải là ảnh hợp lệ (jpg/png)."
                break
            if f.size > 1 * 1024 * 1024:
                errors["images"] = f"{f.name} vượt quá 1MB."
                break

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    save_folder = os.path.join(settings.MEDIA_ROOT, "products")
    os.makedirs(save_folder, exist_ok=True)

    saved_names = []
    for f in files:
        filename = f.name.replace(" ", "_")
        base, ext = os.path.splitext(filename)
        new_name = f"{base}_{int(time.time() * 1000)}{ext.lower()}"

        path = os.path.join(save_folder, new_name)
        with open(path, "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)

        saved_names.append(new_name)

    Product.objects.create(
        id_user=request.user,
        name=name,
        price=price,
        id_category_id=id_category,
        id_brand_id=id_brand,
        status=int(status),
        sale=int(sale) if status == "1" else 0,
        company=company,
        detail=detail,
        images=saved_names,
    )

    return JsonResponse({"status": "ok"})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, id_user=request.user)
    return render(request, "edit_product.html", {
        "product": product,
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
    })

@login_required
@require_POST
def edit_product_ajax(request, pk):
    product = get_object_or_404(Product, pk=pk, id_user=request.user)

    name    = (request.POST.get("name") or "").strip()
    price   = (request.POST.get("price") or "").strip()
    status  = request.POST.get("status") or "0"
    sale    = request.POST.get("sale") or "0"
    company = (request.POST.get("company") or "").strip()
    detail  = (request.POST.get("detail") or "").strip()
    id_category = request.POST.get("id_category")
    id_brand    = request.POST.get("id_brand")

    hinh_cu      = product.images or []
    hinh_xoa     = request.POST.getlist("hinhxoa")
    hinh_con_lai = [img for img in hinh_cu if img not in hinh_xoa]
    files        = request.FILES.getlist("images")

    errors = {}

    if not name:
        errors["name"] = "Tên sản phẩm không được để trống."
    if not price:
        errors["price"] = "Giá không được để trống."
    if not id_category:
        errors["id_category"] = "Vui lòng chọn category."
    if not id_brand:
        errors["id_brand"] = "Vui lòng chọn brand."

    tong_hinh = len(hinh_con_lai) + len(files)
    if tong_hinh == 0:
        errors["images"] = "Sản phẩm phải có ít nhất một hình."
    elif tong_hinh > 3:
        errors["images"] = (
            f"Tổng số hình phải <= 3 "
            f"(còn {len(hinh_con_lai)} hình cũ + {len(files)} hình mới)."
        )
    else:
        for f in files:
            if f.content_type not in ["image/jpeg", "image/png"]:
                errors["images"] = f"{f.name} không phải là ảnh hợp lệ (jpg/png)."
                break
            if f.size > 1 * 1024 * 1024:
                errors["images"] = f"{f.name} vượt quá 1MB."
                break

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    save_folder = os.path.join(settings.MEDIA_ROOT, "products")
    os.makedirs(save_folder, exist_ok=True)

    saved_names = []
    for f in files:
        filename = f.name.replace(" ", "_")
        base, ext = os.path.splitext(filename)
        new_name = f"{base}_{int(time.time() * 1000)}{ext.lower()}"

        with open(os.path.join(save_folder, new_name), "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)

        saved_names.append(new_name)

    for img in hinh_xoa:
        if img in hinh_cu:                      
            path = os.path.join(save_folder, img)
            if os.path.exists(path):
                os.remove(path)

    product.name        = name
    product.price       = price
    product.id_category_id = id_category
    product.id_brand_id    = id_brand
    product.status      = int(status)
    product.sale        = int(sale) if status == "1" else 0
    product.company     = company
    product.detail      = detail
    product.images      = hinh_con_lai + saved_names
    product.save()

    return JsonResponse({"status": "ok"})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, id_user=request.user)

    save_folder = os.path.join(settings.MEDIA_ROOT, "products")
    for img in product.images or []:
        path = os.path.join(save_folder, img)
        if os.path.exists(path):
            os.remove(path)

    product.delete()
    return redirect("my_product")

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)

    gia_sale = None
    if product.status == 1 and product.sale:
        gia_sale = product.price * (100 - product.sale) / 100

    return render(request, 'product_details.html', {
        'product': product,
        'gia_sale': gia_sale,
    })

@require_POST
def add_to_cart_ajax(request):
    product_id = request.POST.get("id")
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get("cart", {})

    key = str(product.id)

    if key in cart:
        cart[key]["qty"] += 1
    else:
        cart[key] = {
            "name": product.name,
            "price": float(product.price),
            "image": product.images[0] if product.images else "",
            "qty": 1,
        }

    request.session["cart"] = cart
    tong = 0
    for item in cart.values():
        tong += item["qty"]

    return JsonResponse({"status": "ok", "cart_count": tong})


def tinh_cart_count(cart):
    tong = 0
    for item in cart.values():
        tong += item["qty"]
    return tong


def tinh_sub_total(cart):
    tong = 0
    for item in cart.values():
        tong += item["price"] * item["qty"]
    return round(tong, 2)


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    for key, item in cart.items():
        items.append({
            "id": key,
            "name": item["name"],
            "price": item["price"],
            "image": item["image"],
            "qty": item["qty"],
            "total": round(item["price"] * item["qty"], 2),
        })

    return render(request, "cart.html", {
        "items": items,
        "sub_total": tinh_sub_total(cart),
    })


@require_POST
def update_cart_ajax(request):
    key = str(request.POST.get("id"))
    action = request.POST.get("action")

    cart = request.session.get("cart", {})

    if key not in cart:
        return JsonResponse({"status": "error"}, status=400)

    if action == "up":
        cart[key]["qty"] += 1
    elif action == "down":
        if cart[key]["qty"] > 1:
            cart[key]["qty"] -= 1
    elif action == "delete":
        del cart[key]

    request.session["cart"] = cart

    qty = 0
    total = 0
    if key in cart:
        qty = cart[key]["qty"]
        total = round(cart[key]["price"] * qty, 2)

    return JsonResponse({
        "status": "ok",
        "qty": qty,
        "total": total,
        "sub_total": tinh_sub_total(cart),
        "cart_count": tinh_cart_count(cart),
    })


def lay_cart_items(request):
    cart = request.session.get("cart", {})
    items = []
    for key, item in cart.items():
        items.append({
            "id": key,
            "name": item["name"],
            "price": item["price"],
            "image": item["image"],
            "qty": item["qty"],
            "total": round(item["price"] * item["qty"], 2),
        })
    return items, tinh_sub_total(cart)


def checkout_view(request):
    items, sub_total = lay_cart_items(request)

    context = {
        "items": items,
        "sub_total": sub_total,
    }

    if not request.user.is_authenticated:
        context["form"] = UserRegisterForm()

    return render(request, "checkout.html", context)


def gui_mail_don_hang(user, items, sub_total, history):
    subject = f"Xác nhận đơn hàng #{history.id} - E-Shopper"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [history.email]

    text_content = f"""Chao {history.name}, cảm ơn bạn đã đặt hàng tại E-Shopper."""


    html_content = render_to_string("emails/order_email.html", {
        "user": user,
        "history": history,
        "items": items,
        "sub_total": sub_total,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@require_POST
def place_order(request):
    items, sub_total = lay_cart_items(request)

    if not items:
        messages.error(request, "Giỏ hàng trống không thể đặt hàng.")
        return redirect("cart")

    if request.user.is_authenticated:
        user = request.user
    else:
        form = UserRegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "checkout.html", {
                "items": items,
                "sub_total": sub_total,
                "form": form,
            })

        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.is_superuser = False
        user.is_staff = False
        user.save()

        login(request, user)

    ten = (f"{user.first_name} {user.last_name}").strip() or user.username

    history = History.objects.create(
        id_user=user,
        name=ten,
        email=user.email,
        phone=user.phone,
        price=sub_total,
    )

    loi_mail = None
    try:
        gui_mail_don_hang(user, items, sub_total, history)
    except Exception as e:
        loi_mail = str(e)

    request.session["cart"] = {}

    return render(request, "order_success.html", {
        "history": history,
        "items": items,
        "sub_total": sub_total,
        "loi_mail": loi_mail,
    })



PER_PAGE = 3

PRICE_RANGES = [
    ("0-50000", "< 50.000"),
    ("50000-100000", "50.000 - 100.000"),
    ("100000-200000", "100.000 - 200.000"),
    ("200000-500000", "200.000 - 500.000"),
    ("500000-1000000", "500.000 - 1.000.000"),
]


def search_advanced(request):
    return render(request, "search_advanced.html", {
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
        "price_ranges": PRICE_RANGES,
    })


def search_advanced_ajax(request):
    name        = (request.GET.get("name") or "").strip()
    price       = request.GET.get("price") or ""
    id_category = request.GET.get("id_category") or ""
    id_brand    = request.GET.get("id_brand") or ""
    status      = request.GET.get("status") or ""

    products = Product.objects.all()

    if name:
        products = products.filter(name__icontains=name)

    if price:
        try:
            gia_min, gia_max = price.split("-")
            products = products.filter(price__range=(int(gia_min), int(gia_max)))
        except ValueError:
            pass

    if id_category.isdigit():
        products = products.filter(id_category_id=id_category)

    if id_brand.isdigit():
        products = products.filter(id_brand_id=id_brand)

    if status in ("0", "1"):
        products = products.filter(status=int(status))

    products = products.order_by("-created_at", "-id")

    paginator = Paginator(products, PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    html = render_to_string("search_results.html", {"page_obj": page_obj}, request=request)

    return JsonResponse({
        "status": "ok",
        "html": html,
        "total": paginator.count,
    })
