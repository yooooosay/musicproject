from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.mail import EmailMessage

from .models import MusicPost
from .forms import MusicPostForm, ContactForm

class MusicListView(ListView):
    model = MusicPost
    template_name = 'index.html'
    context_object_name = 'musics'
    paginate_by = 9
    ordering = ['-posted_at']

class IndexView(MusicListView):
    pass

class CategoryView(MusicListView):
    def get_queryset(self):
        category_id = self.kwargs['category']
        return MusicPost.objects.filter(category=category_id).order_by('-posted_at')

class UserView(MusicListView):
    def get_queryset(self):
        user_id = self.kwargs['user']
        return MusicPost.objects.filter(user=user_id).order_by('-posted_at')

@method_decorator(login_required, name='dispatch')
class CreateMusicView(CreateView):
    form_class = MusicPostForm
    template_name = "music_post.html"
    success_url = reverse_lazy('music:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)

class MusicSuccessView(TemplateView):
    template_name = 'music_success.html'

class MusicDetailView(DetailView):
    template_name = 'detail.html'
    model = MusicPost

class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 3

    def get_queryset(self):
        return MusicPost.objects.filter(user=self.request.user).order_by('-posted_at')

class MusicDeleteView(DeleteView):
    model = MusicPost
    template_name = 'music_delete.html'
    success_url = reverse_lazy('music:mypage')

    def dispatch(self, request, *args, **kwargs):
        music = self.get_object()
        if music.user != request.user:
            return HttpResponseForbidden("この投稿は削除できません。")
        return super().dispatch(request, *args, **kwargs)

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('music:contact_done')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message_text = form.cleaned_data['message']
        subject = f'お問い合わせ: {title}'
        msg_body = f'送信者名: {name}\nメールアドレス: {email}\n件名: {title}\nメッセージ:\n{message_text}'
        from_email = 'tdn2532044@stu.o-hara.ac.jp'
        to_list = ['tdn2532044@stu.o-hara.ac.jp']
        email_message = EmailMessage(subject=subject, body=msg_body, from_email=from_email, to=to_list)
        email_message.send()
        return super().form_valid(form)

class ContactDoneView(TemplateView):
    template_name = 'contact_done.html'
