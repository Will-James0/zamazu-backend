from django.urls import path, include
from apps.music.views import (AlbumCreateView, AlbumListView, AlbumDetailView, AlbumDeleteView, AlbumUpdateView,
                              ClipCreateView, ClipListView, ClipDetailView, ClipDeleteView, ClipUpdateView,
                              TrackCreateView, TrackListView, TrackDetailView, TrackDeleteView, TrackUpdateView,
                              ToggleLikeView, RecordViewView)


urlpatterns = [
    
    # Album URLs
    path('albums/', include([
        path('list/', AlbumListView.as_view(), name='album-list'),
        path('create/', AlbumCreateView.as_view(), name='album-create'),
        path('detail/<uuid:code>/', AlbumDetailView.as_view(), name='album-detail'),
        path('update/<uuid:code>/', AlbumUpdateView.as_view(), name='album-update'),
        path('delete/<uuid:code>/', AlbumDeleteView.as_view(), name='album-delete'),
    ])),
    
    # Track URLs
    path('tracks/', include([
        path('list/', TrackListView.as_view(), name='track-list'),
        path('create/', TrackCreateView.as_view(), name='track-create'),
        path('detail/<uuid:code>/', TrackDetailView.as_view(), name='track-detail'),
        path('update/<uuid:code>/', TrackUpdateView.as_view(), name='track-update'),
        path('delete/<uuid:code>/', TrackDeleteView.as_view(), name='track-delete'),
    ])),
    
    # Clip URLs
    path('clips/', include([
        path('list/', ClipListView.as_view(), name='clip-list'),
        path('create/', ClipCreateView.as_view(), name='clip-create'),
        path('detail/<uuid:code>/', ClipDetailView.as_view(), name='clip-detail'),
        path('update/<uuid:code>/', ClipUpdateView.as_view(), name='clip-update'),
        path('delete/<uuid:code>/', ClipDeleteView.as_view(), name='clip-delete'),
    ])),
    
    path('like/<str:content_type>/<uuid:code>/', ToggleLikeView.as_view(), name='toggle-like'),
    path('view/<str:content_type>/<uuid:code>/', RecordViewView.as_view(), name='record-view'),
]