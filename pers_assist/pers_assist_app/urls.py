from django.urls import path
from . import views

app_name = 'pers_assist_app'

urlpatterns = [
    path('', views.main, name='main'),

    # contacts
    path('contacts/', views.contacts, name='contacts'),
    path('contact_create/', views.contact_create, name='contact_create'),
    path('contact/<int:contact_id>/detail', views.contact_detail, name='contact_detail'),
    path('contact/<int:contact_id>/delete', views.contact_delete, name='contact_delete'),
    path('contact/<int:contact_id>/edit', views.contact_edit, name='contact_edit'),
    path('search_birthdays/', views.search_birthdays, name='search_birthdays'),
    path('search_contacts/', views.search_contacts, name='search_contacts'),

    # notes
    path('notes/', views.notes, name='notes'),
    path('notes/tag/<slug:tag>/', views.notes, name='notes_by_tag'),
    path('notes/search/', views.search_note_by_query, name='notes_by_query'),
    path('note/create/', views.create_note, name='note_create'),
    path('note/<int:note_id>/delete/', views.delete_note, name='note_delete'),
    path('note/<int:note_id>/edit/', views.edit_note, name='note_edit'),

    # tags
    path('tag_create/', views.create_tag, name='tag_create'),

    # documents
    path('documents/', views.documents, name='documents'),
    path('upload_doc/', views.upload_document, name='upload_document'),
    path('download_doc/<int:document_id>/', views.document_download, name='document_download'),
    path('document/<int:document_id>/delete', views.document_delete, name='document_delete'),
]
