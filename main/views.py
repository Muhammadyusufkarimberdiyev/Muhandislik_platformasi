# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.text import slugify

from .models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.utils import timezone
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


def get_client_ip(request):
    """Client IP addressni olish"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Login/Signup View
class LoginSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:sections')
        return render(request, 'login-signup.html')
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Profil yangilash
                profile = user.profile
                profile.last_login_time = timezone.now()
                profile.login_count += 1
                profile.save()
                
                # Login tarixini saqlash
                LoginHistory.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                return redirect('main:sections')
            else:
                messages.error(request, "Login yoki parol noto'g'ri!")
                return render(request, 'login-signup.html', {'error': 'invalid'})
        
        elif action == 'signup':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, "Parollar mos kelmadi!")
                return render(request, 'login-signup.html', {'error': 'password_mismatch'})
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu foydalanuvchi nomi band!")
                return render(request, 'login-signup.html', {'error': 'username_exists'})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan!")
                return render(request, 'login-signup.html', {'error': 'email_exists'})
            
            # Yangi foydalanuvchi yaratish
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Avtomatik login
            login(request, user)
            
            # Login tarixini saqlash
            LoginHistory.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('main:sections')
        
        return render(request, 'login-signup.html')


# Logout View
@login_required(login_url='main:login')
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz!")
    return redirect('main:home')


# SectionsPage ni login required qilish
@method_decorator(login_required(login_url='main:login'), name='dispatch')
class SectionsPage(View):
    def get(self, request):
        cats = ExperimentCategory.objects.all().order_by("name")
        return render(request, "sections.html", {"ExpCategory": cats})

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

# --- BOSH SAHIFA ---
class Home(View):
    def get(self, request):
        ctx = {
            "Bcategory": BookCategory.objects.all(),
            "books": Book.objects.all(),
            "VCategory": VideoCategory.objects.all(),
            "videos": Video.objects.all(),
        }
        return render(request, 'index.html', ctx)

# --- KITOBLAR ---
class BooksPage(View):
    def get(self, request):
        qs = Book.objects.select_related('category').all()
        category_id = request.GET.get("category")
        active_category = int(category_id) if category_id else None
        if active_category:
            qs = qs.filter(category_id=active_category)
        paginator = Paginator(qs, 6)
        page = paginator.get_page(request.GET.get('page', 1))
        ctx = {
            "Bcategory": BookCategory.objects.all(),
            "books": page.object_list,
            "page": page,
            "paginator": paginator,
            "active_category": active_category,
            "query": "",
        }
        return render(request, 'books.html', ctx)

def bsearch(request):
    q = (request.POST.get('q') or "").strip()
    if not q:
        return redirect('main:books')
    qs = Book.objects.select_related('category').filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    )
    paginator = Paginator(qs, 6)
    page = paginator.get_page(request.GET.get('page', 1))
    ctx = {
        "Bcategory": BookCategory.objects.all(),
        "books": page.object_list,
        "page": page,
        "paginator": paginator,
        "active_category": None,
        "query": q,
    }
    return render(request, 'books.html', ctx)

# --- VIDEOLAR ---
class VideosPage(View):
    def get(self, request):
        qs = Video.objects.all().select_related('category')
        cat_id = request.GET.get("category")
        active_vcat = int(cat_id) if cat_id else None
        if active_vcat:
            qs = qs.filter(category_id=active_vcat)
        paginator = Paginator(qs, 6)
        page = paginator.get_page(request.GET.get('page', 1))
        ctx = {
            "VCategory": VideoCategory.objects.all(),
            "videos": page.object_list,
            "page": page,
            "paginator": paginator,
            "active_vcat": active_vcat,
        }
        return render(request, 'videos.html', ctx)

def vsearch(request):
    q = (request.POST.get('q') or "").strip()
    if not q:
        return redirect('main:videos')
    qs = Video.objects.select_related('category').filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    )
    paginator = Paginator(qs, 6)
    page = paginator.get_page(request.GET.get('page', 1))
    ctx = {
        "VCategory": VideoCategory.objects.all(),
        "videos": page.object_list,
        "page": page,
        "paginator": paginator,
        "active_vcat": None,
        "vquery": q,
    }
    return render(request, 'videos.html', ctx)

# --- YORDAMCHI FUNKSIYALAR ---
def _open_url(exp):
    """Tajriba uchun ochish linki"""
    for attr in ("html_file", "file", "link", "youtubelink1", "youtubelink2", "youtubelink3"):
        if hasattr(exp, attr):
            val = getattr(exp, attr)
            try:
                if val and hasattr(val, "url"):
                    return val.url
            except:
                pass
            if val:
                return val
    return "#"

def _paginate_qs(qs, request, per_page=9):
    paginator = Paginator(qs, per_page)
    page = paginator.get_page(request.GET.get("page", 1))
    for e in page.object_list:
        e.open_url = _open_url(e)
    return paginator, page

def _get_class_category_by_slug(slug):
    """ClassCategory'ni slug orqali topish"""
    for cat in ClassCategory.objects.all():
        if slugify(cat.name) == slug:
            return cat
    return None

# --- TAJRIBALAR (EXPERIMENTS) ---
try:
    from .models import Experiment, ExperimentCategory
except:
    from .models import Expirements as Experiment
    from .models import ExpirementCategory as ExperimentCategory


# Kategoriya bo'yicha sahifa
class ExperimentSection(View):
    PER_PAGE = 6
    def get(self, request, slug):
        cat = get_object_or_404(ExperimentCategory, slug=slug)
        qs = Experiment.objects.select_related("category").filter(category=cat).order_by("-id")
        q = (request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        paginator, page = _paginate_qs(qs, request, per_page=self.PER_PAGE)
        # Template tanlash
        TEMPLATE_MAP = {
            "arduino": "robotselect.html",
            "elektronika": "elektrselect.html",
            "3d-chizmalar": "3dselect.html",
            "loyihalar": "loyihselect.html",
        }
        tpl = TEMPLATE_MAP.get(slug, "robotselect.html")
        ctx = {
            "experiments": page.object_list,
            "page": page,
            "paginator": paginator,
            "equery": q,
            "active_ecat": cat.id,
        }
        return render(request, tpl, ctx)

# --- ROBOTLAR (ARDUINO) ---
class RobotSelectPage(View):
    def get(self, request):
        qs = Experiment.objects.select_related("category").filter(
            Q(category__slug__iexact="arduino") | Q(category__name__icontains="ardu")
        )
        q = (request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        paginator, page = _paginate_qs(qs.order_by("-id"), request, per_page=9)
        ctx = {
            "experiments": page.object_list,
            "page": page,
            "paginator": paginator,
            "equery": q,
        }
        return render(request, "robotselect.html", ctx)

def asearch(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("main:robotselect")
    qs = Experiment.objects.select_related("category").filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    )
    paginator, page = _paginate_qs(qs.order_by("-id"), request, per_page=9)
    ctx = {
        "experiments": page.object_list,
        "page": page,
        "paginator": paginator,
        "equery": q,
    }
    return render(request, "robotselect.html", ctx)

# --- ELEKTRONIKA VIDEOLARI ---
class ElektrSelectPage(View):
    def get(self, request):
        # Elektronika kategoriyasidagi VIDEOLARNI olish
        qs = Experiment.objects.select_related("category").filter(
            Q(category__slug__iexact="elektronika") | Q(category__name__icontains="elektr")
        ).exclude(
            Q(link__isnull=True) & Q(youtubelink1__isnull=True)
        )
        
        q = (request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        
        paginator = Paginator(qs.order_by("-id"), 6)
        page = paginator.get_page(request.GET.get("page", 1))
        
        ctx = {
            "experiments": page.object_list,
            "page": page,
            "paginator": paginator,
            "equery": q,
        }
        return render(request, "elektrselect.html", ctx)

def esearch(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("main:elektrselect")
    
    qs = Experiment.objects.select_related("category").filter(
        Q(category__slug__iexact="elektronika") | Q(category__name__icontains="elektr")
    ).filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    ).exclude(
        Q(link__isnull=True) & Q(youtubelink1__isnull=True)
    )
    
    paginator = Paginator(qs.order_by("-id"), 6)
    page = paginator.get_page(request.GET.get("page", 1))
    
    ctx = {
        "experiments": page.object_list,
        "page": page,
        "paginator": paginator,
        "equery": q,
    }
    return render(request, "elektrselect.html", ctx)

# --- 3D CHIZMALAR VIDEOLARI ---
class Select3DPage(View):
    def get(self, request):
        # 3D kategoriyasidagi VIDEOLARNI olish
        qs = Experiment.objects.select_related("category").filter(
            Q(category__slug__iexact="3d-chizmalar") | Q(category__name__icontains="3d")
        ).exclude(
            Q(link__isnull=True) & Q(youtubelink1__isnull=True)
        )
        
        q = (request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        
        paginator = Paginator(qs.order_by("-id"), 6)
        page = paginator.get_page(request.GET.get("page", 1))
        
        ctx = {
            "experiments": page.object_list,
            "page": page,
            "paginator": paginator,
            "equery": q,
        }
        return render(request, "3dselect.html", ctx)

def dsearch(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("main:3dselect")
    
    qs = Experiment.objects.select_related("category").filter(
        Q(category__slug__iexact="3d-chizmalar") | Q(category__name__icontains="3d")
    ).filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    ).exclude(
        Q(link__isnull=True) & Q(youtubelink1__isnull=True)
    )
    
    paginator = Paginator(qs.order_by("-id"), 6)
    page = paginator.get_page(request.GET.get("page", 1))
    
    ctx = {
        "experiments": page.object_list,
        "page": page,
        "paginator": paginator,
        "equery": q,
    }
    return render(request, "3dselect.html", ctx)

# --- LOYIHALAR VIDEOLARI ---
class LoyihSelectPage(View):
    def get(self, request):
        # Loyihalar kategoriyasidagi VIDEOLARNI olish
        qs = Experiment.objects.select_related("category").filter(
            Q(category__slug__icontains="loyiha") | Q(category__name__icontains="loyiha")
        ).exclude(
            Q(link__isnull=True) & Q(youtubelink1__isnull=True)
        )
        
        q = (request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        
        paginator = Paginator(qs.order_by("-id"), 6)
        page = paginator.get_page(request.GET.get("page", 1))
        
        ctx = {
            "experiments": page.object_list,
            "page": page,
            "paginator": paginator,
            "equery": q,
        }
        return render(request, "loyihselect.html", ctx)

def lsearch(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("main:loyihselect")
    
    qs = Experiment.objects.select_related("category").filter(
        Q(category__slug__icontains="loyiha") | Q(category__name__icontains="loyiha")
    ).filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    ).exclude(
        Q(link__isnull=True) & Q(youtubelink1__isnull=True)
    )
    
    paginator = Paginator(qs.order_by("-id"), 6)
    page = paginator.get_page(request.GET.get("page", 1))
    
    ctx = {
        "experiments": page.object_list,
        "page": page,
        "paginator": paginator,
        "equery": q,
    }
    return render(request, "loyihselect.html", ctx)

# --- SINFLAR (CLASS) BO'LIMI ---
class ClassSectionsPage(View):
    """Kategoriyalar ro'yxati - sections.html kabi"""
    def get(self, request):
        cats = ClassCategory.objects.all().order_by("name")
        return render(request, "class.html", {"ClassCategory": cats})

class ClassSelectPage(View):
    """Sinf videolari - robotselect strukturasi, videos dizayni"""
    PER_PAGE = 9
    def get(self, request):
        qs = ClassVideo.objects.select_related("category").all().order_by("-date")
        
        # Kategoriya filtri
        category_id = request.GET.get("category")
        active_ccat = int(category_id) if category_id else None
        if active_ccat:
            qs = qs.filter(category_id=active_ccat)
        
        # Qidiruv
        q = (request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        
        paginator = Paginator(qs, self.PER_PAGE)
        page = paginator.get_page(request.GET.get("page", 1))
        
        ctx = {
            "ClassCategory": ClassCategory.objects.all(),
            "videos": page.object_list,
            "page": page,
            "paginator": paginator,
            "cquery": q,
            "active_ccat": active_ccat,
        }
        return render(request, "classselect.html", ctx)

def csearch(request):
    """Class qidiruv"""
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("main:classselect")
    qs = ClassVideo.objects.select_related("category").filter(
        Q(name__icontains=q) | Q(category__name__icontains=q)
    )
    paginator = Paginator(qs.order_by("-date"), 9)
    page = paginator.get_page(request.GET.get("page", 1))
    ctx = {
        "ClassCategory": ClassCategory.objects.all(),
        "videos": page.object_list,
        "page": page,
        "paginator": paginator,
        "cquery": q,
        "active_ccat": None,
    }
    return render(request, "classselect.html", ctx)

# --- BOSHQA SAHIFALAR ---
class AIPage(View):
    def get(self, request):
        return render(request, 'AI.html')

class ProgramPage(View):
    def get(self, request):
        return render(request, 'programm.html')

class Back(View):
    def get(self, request):
        context = {
            "Bcategory": BookCategory.objects.all(),
            "books": Book.objects.all(),
            "VCategory": VideoCategory.objects.all(),
            "videos": Video.objects.all(),
        }
        return render(request, 'index.html', context)