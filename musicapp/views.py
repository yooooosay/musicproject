from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import MusicPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import MusicPost


# ====== 投稿一覧の共通ベース ======
class MusicListView(ListView):
    model = MusicPost
    template_name = 'index.html'
    context_object_name = 'musics'
    paginate_by = 9
    ordering = ['-posted_at']


# ====== 各ビュー ======
class IndexView(MusicListView):
    """全投稿一覧"""
    pass


class CategoryView(MusicListView):
    """カテゴリ別投稿一覧"""
    def get_queryset(self):
        category_id = self.kwargs['category']
        return MusicPost.objects.filter(category=category_id).order_by('-posted_at')


class UserView(MusicListView):
    """ユーザー別投稿一覧"""
    def get_queryset(self):
        user_id = self.kwargs['user']
        return MusicPost.objects.filter(user=user_id).order_by('-posted_at')


@method_decorator(login_required, name='dispatch')
class CreateMusicView(CreateView):
    """音楽投稿フォーム"""
    form_class = MusicPostForm
    template_name = "music_post.html"
    success_url = reverse_lazy('music:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)


class MusicSuccessView(TemplateView):
    """投稿完了ページ"""
    template_name = 'music_success.html'


class MusicDetailView(DetailView):
    """投稿詳細ページ"""
    template_name = 'detail.html'
    model = MusicPost


class MypageView(ListView):
    """マイページ（自分の投稿一覧）"""
    template_name = 'mypage.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = MusicPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset       
    

class MusicDeleteView(DeleteView):
    """投稿削除ページ"""
    model = MusicPost
    template_name = 'music_delete.html'
    success_url = reverse_lazy('music:mypage')

    # 他人の投稿削除を禁止
    def dispatch(self, request, *args, **kwargs):
        music = self.get_object()
        if music.user != request.user:
            return HttpResponseForbidden("この投稿は削除できません。")
        return super().dispatch(request, *args, **kwargs)
