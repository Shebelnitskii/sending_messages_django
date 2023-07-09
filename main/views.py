from django.core.checks import messages
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from main.forms import MessageForm, MailingForm
from main.models import Message, Mailing


# Create your views here.

def index(request):
    return render(request, 'main/main.html')


class MessageListView(generic.ListView):
    model = Message
    template_name = 'main/massage_list'
    context_object_name = 'message_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        return context


class MessageCreateView(generic.CreateView):
    model = Message
    fields = ('client', 'letter_subject', 'letter_body')

    def form_valid(self, form):
        # Сохранение формы сообщения и получение созданного объекта сообщения
        message = form.save()
        mailing = message.mailing if hasattr(message, 'mailing') else None
        # Создание формы рассылки и заполнение данными из запроса
        mailing_form = MailingForm(self.request.POST, instance=mailing)

        if mailing_form.is_valid():
            # Сохранение формы рассылки и связывание с объектом сообщения
            mailing = mailing_form.save(commit=False)
            mailing.message = message
            mailing.save()

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm()
        context['title'] = 'Добавить рассылку'
        return context

    def get_success_url(self):
        return reverse('main:message_list')


class MessageUpdateView(generic.UpdateView):
    model = Message
    fields = ('client', 'letter_subject', 'letter_body')
    extra_context = {'extra_context': 'Изменить рассылку'}

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MailingFormSet = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)

        if self.request.method == 'POST':
            context['formset'] = MailingFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = MailingFormSet(instance=self.object)

        return context

    def get_success_url(self):
        return reverse('main:message_list')


class MessagDetailView(generic.DetailView):
    model = Message
    template_name = 'main/message_detail.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"О рассылке {self.object.client}"
        context['mailing'] = self.object.mailing if hasattr(self.object, 'mailing') else None

        return context


class MessageDeleteView(generic.DeleteView):
    model = Message
    template_name = 'main/message_confirm_delete.html'
    permission_required = 'main.delete_message'
    extra_context = {'title': 'Подтвердить удаление'}

    def get_success_url(self):
        return reverse('main:message_list')
