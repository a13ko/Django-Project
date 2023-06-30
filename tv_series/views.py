from django.shortcuts import render,redirect    
from tv_series.models import Comment,Serie,Episode,EpisodeGallery,SerieGallery,Season,Genre,Country,Actor,Language,CommentEpisode
from users.models import MyUser
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import ExtractYear
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from tv_series.forms import CommentForm,CommentEpisodeForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse


User = get_user_model()

def show_list_series(request):
    genres = request.GET.getlist('genre', None)
    language = request.GET.getlist('language', None)
    years = request.GET.get('years', None)
    imdb = request.GET.get('imdb', None)


    series=Serie.objects.all()

    if genres:
        series = series.filter(genres__in=genres).distinct()

    if language:
        series = series.filter(language__in=language).distinct()
    
    if years:
        start_year, end_year = years.split(',')
        series = series.filter(release_date__year__range=(start_year, end_year))

    if imdb:
        imdb_start, imdb_end = imdb.split(',')
        series = series.filter(imdb__range=(float(imdb_start), float(imdb_end)))
    



    
    paginator = Paginator(series, 5)
    page = request.GET.get('page', 1)
    series_list = paginator.get_page(page)
    context = {
        'genres': Genre.objects.all(),
        'series':series_list,
        'language': Language.objects.all(),
    }

    return render(request, 'series/serie_list.html',context)



def serie_wish_view(request):
    data = {}
    serie = get_object_or_404(Serie, id=int(request.POST.get("id")))
    
    
    

    if request.user in serie.wishlist.all():
        serie.wishlist.remove(request.user)
        data["success"] = False
    else:
        serie.wishlist.add(request.user)
        data["success"] = True
    
    return JsonResponse(data)


def premium_user(view_func):
    def wrap(request, *args, **kwargs):
        slug = kwargs.get('slug')
        serie = get_object_or_404(Serie, slug=slug)

        if serie.account != 'Premium' and (not request.user.is_authenticated or request.user.account != 'Premium'):
            return view_func(request, *args, **kwargs)

        elif serie.account == 'Premium' and (not request.user.is_authenticated or request.user.account != 'Premium'):
            if request.user.is_authenticated:
                messages.warning(request, 'Bu seriala baxmaq üçün premium hesabınız olmalıdır!')
                return redirect('users:plan')
            else:
                login_url = reverse('users:login')
                redirect_url = login_url + '?next=' + request.path
                return redirect(redirect_url)

        else:
            return view_func(request, *args, **kwargs)

    return wrap




@premium_user
def serie_detail(request, slug): 
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            serie = get_object_or_404(Serie, slug=slug)
            comment = form.save(commit=False)
            comment.serie = serie
            comment.user = request.user
            comment.save()
            return redirect('series:series-detail', slug=slug)
    else:
        form = CommentForm()
    serie = get_object_or_404(Serie, slug=slug)
    

	

    seasons = serie.seasons.all().order_by('number')
    episodes = Episode.objects.filter(serie=serie)
    comments = Comment.objects.filter(serie=serie).order_by('-created_at')
    return render(request, 'series/serie_detail.html', {'serie': serie, 'seasons': seasons,'episodes':episodes,'comments':comments, 'form': form})



def serie_episode(request):
    episode_title = request.GET.get('episode')
    episode = get_object_or_404(Episode, title=episode_title)
    session_key = 'viewed_episode_{}'.format(episode.id)
    if not request.session.get(session_key, False):
        episode.watched_count += 1
        episode.save()
        request.session[session_key] = True
    season = episode.season
    serie = episode.serie
    seasons = Season.objects.filter(serie=serie).order_by('number')
    episodes = Episode.objects.filter(serie=serie)
    comments = CommentEpisode.objects.filter(episode=episode).order_by('-created_at')

    if request.method == 'POST':
        form = CommentEpisodeForm(request.POST)
        if form.is_valid():
            commentepisode = form.save(commit=False)
            commentepisode.episode = episode
            commentepisode.user = request.user
            commentepisode.save()
            
    else:
        form = CommentEpisodeForm()

    return render(request, 'series/serial_bolum.html', {'episode': episode, 'serie': serie, 'seasons': seasons,'episodes': episodes,'form':form,'comments':comments})








@login_required
@require_POST
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def delete_comments(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(CommentEpisode, id=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'success': True})
