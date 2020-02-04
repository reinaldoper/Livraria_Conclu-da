from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Author, BookInstance, Genero, Empresta
from django.views import generic
import datetime
from django.contrib.auth.decorators import permission_required, login_required
from .forms import RenewBookForm, AuthorForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_generes = Genero.objects.count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'num_generes': num_generes,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'book_list.html'


class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    template_name = 'author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='p').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin , CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_form.html'
    success_url = reverse_lazy('index')


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_Update.html'
    success_url = reverse_lazy('index')


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    template_name = 'delete_author.html'
    success_url = reverse_lazy('index')


class BookCreate(PermissionRequiredMixin , CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    template_name = 'book_form.html'
    success_url = reverse_lazy('index')


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    template_name = 'delete_book.html'
    success_url = reverse_lazy('index')


class CreateEmprestimo(PermissionRequiredMixin , CreateView):
    model = BookInstance
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('index')
# Create your views here.
