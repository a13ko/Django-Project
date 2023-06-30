from django.shortcuts import render,redirect    
from .models import *
from tv_series.models import Serie
from users.models import MyUser
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import ExtractYear
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse


User = get_user_model()

# Create your views here.
def show_home(request):
    trends=Movie.objects.annotate(user_count=Count('wishlist')).order_by('-user_count')[:20]
    imdb = Movie.objects.order_by('-imdb')
    movies=Movie.objects.all()
    new_movies=Movie.objects.order_by('-created_at')[:4]
    series=Serie.objects.all()
    new_series = Serie.objects.order_by('-created_at')[:6]
    users=User.objects.all()
    coming_movies = ComingMovie.objects.order_by('-release_date')[:6]

    search1=request.GET.get('search')
    if search1:
        movies = Movie.objects.filter(title__icontains=search1)

    

    context = {
        'coming_movies':coming_movies,
        'movies':movies,
        'new_movies' : new_movies,
        'series':series,
        'new_series': new_series,
        'trends':trends,
        'users':users,
        'imdb': imdb,
        
        
    }

    return render(request, 'movies/home.html',context)



def show_list(request):
    genres = request.GET.getlist('genre', None)
    language = request.GET.getlist('language', None)
    years = request.GET.get('years', None)
    imdb = request.GET.get('imdb', None)
    


    coming_movies = ComingMovie.objects.order_by('-release_date')[:6]
    movies = Movie.objects.all()
    if genres:
        movies = movies.filter(genres__in=genres).distinct()
    if language:
        movies = movies.filter(language__in=language).distinct()
    
    if years:
        start_year, end_year = years.split(',')
        movies = movies.filter(release_date__year__range=(start_year, end_year))

    




    if imdb:
        imdb_start, imdb_end = imdb.split(',')
        movies = movies.filter(imdb__range=(float(imdb_start), float(imdb_end)))
    
    search1=request.GET.get('search')
    if search1:
        movies = Movie.objects.filter(title__icontains=search1)
        
    

    paginator = Paginator(movies, 2)
    page = request.GET.get('page', 1)
    movies_list = paginator.get_page(page)
    context = {
        'coming_movies':coming_movies,
        'movies': movies_list,
        'genres': Genre.objects.all(),
        'language': Language.objects.all(),
        
    }
    return render(request, 'movies/movie_list.html', context)



def premium_user(view_func):
    def wrap(request, *args, **kwargs):
        slug = kwargs.get('slug')
        movie = get_object_or_404(Movie, slug=slug)

        if movie.account != 'Premium' and (not request.user.is_authenticated or request.user.account != 'Premium'):
            return view_func(request, *args, **kwargs)

        elif movie.account == 'Premium' and (not request.user.is_authenticated or request.user.account != 'Premium'):
            if request.user.is_authenticated:
                messages.warning(request, 'Bu filmə baxmaq üçün premium hesabınız olmalıdır!')
                return redirect('users:plan')
            else:
                login_url = reverse('users:login')
                redirect_url = login_url + '?next=' + request.path
                return redirect(redirect_url)

        else:
            return view_func(request, *args, **kwargs)

    return wrap

@premium_user
def movie_details(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    session_key = 'viewed_movie_{}'.format(movie.id)
    if not request.session.get(session_key, False):
        movie.watched_count += 1
        movie.save()
        request.session[session_key] = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            return redirect('movies:movies-detail', slug=slug)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(movie=movie).order_by('-created_at')
    trends=Movie.objects.annotate(user_count=Count('wishlist')).order_by('-user_count')[:20]
    
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'form': form, 'comments': comments,'trends': trends})




@login_required
@require_POST
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'success': True})



def movie_wish_view(request):
    data = {}
    movie = get_object_or_404(Movie, id=int(request.POST.get("id")))
    

    if request.user in movie.wishlist.all():
        movie.wishlist.remove(request.user)
        data["success"] = False
    else:
        movie.wishlist.add(request.user)
        data["success"] = True
    
    return JsonResponse(data)



def wishlist_view(request):
    coming_movies = ComingMovie.objects.order_by('-release_date')[:6]
    movies = Movie.objects.filter(
        wishlist__in=[request.user] ).order_by('-created_at')

    series = Serie.objects.filter(
        wishlist__in=[request.user] ).order_by('-created_at')

    
    

    context = {
        'series': series,
        'movies' : movies,
        'coming_movies':coming_movies,
    }

    return render(request, 'movies/wishlist.html',context)




def movie_serie(request):
    movies = Movie.objects.all()
    series = Serie.objects.all()
    coming_movies = ComingMovie.objects.order_by('-release_date')[:6]

    search = request.GET.get('search')
    if search:
        movies = Movie.objects.filter(title__icontains=search)
        series = Serie.objects.filter(title__icontains=search)
        

   
    context = {
        'coming_movies' : coming_movies,
        'series': series,
        'movies' : movies,
    }
    return render(request, 'movies/search.html', context)


