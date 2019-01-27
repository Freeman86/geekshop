from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from adminapp.forms import AdminShopUserRegisterForm, AdminShopUserChangeForm, AdminProductCategoryEditForm, AdminProductEditForm
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


""""@user_passes_test(lambda x: x.is_superuser)
def index(request):
    object_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'админка/пользователи',
        'object_list': object_list
    }
    return render(request, 'adminapp/users.html', context)"""

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context

def user_create(request):
    if request.method == 'POST':
        form = AdminShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        form = AdminShopUserRegisterForm()

    context = {
        'title': 'пользователи/создание',
        'form': form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = AdminShopUserChangeForm(request.POST, request.FILES, instance=edit_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                kwargs={
                                                    'pk': edit_user.pk,
                                                }))
    else:
        form = AdminShopUserChangeForm(instance=edit_user)

    content = {
        'title': 'пользователи/редактирование',
        'form': form
    }

    return render(request, 'adminapp/user_update.html', content)


def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    # user.is_active = False
    # user.save()
    # return HttpResponseRedirect(reverse('admin:index'))
    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': user
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all()

    context = {
        'title': 'админка/категории',
        'object_list': categories_list
    }

    return render(request, 'adminapp/categories.html', context)

"""def category_create(request):
    if request.method == 'POST':
        form = AdminProductCategoryEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        form = AdminProductCategoryEditForm()

    content = {
        'title': 'категории/создание',
        'form': form
    }
    return render(request, 'adminapp/category_update.html', content)"""


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')
    form_class = AdminProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    #fields = ('__all__')


"""def category_update(request, pk):
    edit_obj = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = AdminProductCategoryEditForm(request.POST, request.FILES, instance=edit_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:category_update',
                                                kwargs={
                                                    'pk': edit_obj.pk,
                                                }))
    else:
        form = AdminProductCategoryEditForm(instance=edit_obj)

    content = {
        'title': 'категории/редактирование',
        'form': form
    }

    return render(request, 'adminapp/category_update.html', content)"""


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')
    form_class = AdminProductCategoryEditForm
    template_name = 'adminapp/category_update.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')
    template_name = 'adminapp/category_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.product_set.all().update(is_active=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': 'админка/продукт',
        'category': category,
        'object_list': object_list,
    }

    return render(request, 'adminapp/products.html', content)

"""def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': 'продукт/подробнее',
        'object': product,
    }

    return render(request, 'adminapp/product_read.html', context)"""

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        form = AdminProductEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        # задаем начальное значение категории в форме
        form = AdminProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'form': form,
        'category': category
    }

    return render(request, 'adminapp/product_update.html', context)


def product_update(request, pk):
    title = 'продукт/создание'
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = AdminProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:products',
                                                kwargs={
                                                    'pk': product.category.pk
                                                }))
    else:
        form = AdminProductEditForm(instance=product)

    context = {
        'title': title,
        'form': form,
        'category': product.category,
    }

    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        item.is_active = False
        item.save()
        return HttpResponseRedirect(reverse('admin:products',
                                            kwargs={
                                                'pk': item.category.pk
                                            }))

    context = {
        'title': 'продукты/удаление',
        'object': item
    }

    return render(request, 'adminapp/product_delete.html', context)
