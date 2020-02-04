from django.contrib import admin
from django.contrib.auth.models import User

from .models import Author, Genero, Book, BookInstance, AuthorBookIntance, EmprestaInstance, Empresta

admin.site.register(Genero)


class EmprestaInlines(admin.TabularInline):
    model = EmprestaInstance


class EmprestaAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower')
    inlines = [EmprestaInlines]


admin.site.register(Empresta, EmprestaAdmin)


class AuthorInlines(admin.TabularInline):
    model = AuthorBookIntance


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [AuthorInlines]


class AuthorIntanceAdmin(admin.ModelAdmin):
    list_display = ('author', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('author', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
admin.site.register(AuthorBookIntance, AuthorIntanceAdmin)


# admin.site.register(Book)
# admin.site.register(BookInstance)

# Register the Admin classes for Book using the decorator
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


admin.site.register(Book, BookAdmin)


# Register the Admin classes for BookInstance using the decorator

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


admin.site.register(BookInstance, BookInstanceAdmin)
# Register your models here.
