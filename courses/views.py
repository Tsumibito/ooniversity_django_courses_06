from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from courses.models import Course, Lesson
from courses.forms import CourseModelForm, LessonModelForm
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django import forms


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        rg = self.request.GET
        queryset = super().get_queryset()
        cours_id = rg.get('pk', None)
        if cours_id:
            queryset = queryset.filter(courses=cours_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(course=self.object.pk)
        context['course'] = Course.objects.get(id=self.object.pk)
        context['title'] = 'Курс: %s' %context['course']
        return context


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'courses/add.html'
    success_url = reverse_lazy('index')
    context_object_name = 'course'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Course %s has been successfully added.' %self.object.name)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового курса'
        return context


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'courses/edit.html'
    context_object_name = 'course'

    def get_success_url(self):
        return reverse('courses:edit', args=(self.object.pk,))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'The changes have been saved.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование данных курса'
        return context


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/remove.html'
    success_url = reverse_lazy('index')
    context_object_name = 'course'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Course %s has been deleted.' %self.object.name)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление Курса'
        return context


def add_lesson(request, pk):
    context = {'error': False}
    if request.method == 'POST':
        form = LessonModelForm(request.POST)
        if form.is_valid():
            instance = form.save()
            context['form'] = instance
            messages.success(request, "Lesson %s has been successfully added." %instance.subject)
            return redirect('courses:detail', pk)
    else:
        form = LessonModelForm(initial={'course':pk})
    context['form'] = form
    return render(request, 'courses/add_lesson.html', context)

