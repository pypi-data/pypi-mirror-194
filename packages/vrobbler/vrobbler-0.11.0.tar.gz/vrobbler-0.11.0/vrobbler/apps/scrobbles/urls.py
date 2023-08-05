from django.urls import path
from scrobbles import views

app_name = 'scrobbles'

urlpatterns = [
    path(
        'manual/imdb/',
        views.ManualScrobbleView.as_view(),
        name='imdb-manual-scrobble',
    ),
    path(
        'manual/audioscrobbler/',
        views.AudioScrobblerImportCreateView.as_view(),
        name='audioscrobbler-file-upload',
    ),
    path(
        'manual/koreader/',
        views.KoReaderImportCreateView.as_view(),
        name='koreader-file-upload',
    ),
    path('finish/<slug:uuid>', views.scrobble_finish, name='finish'),
    path('cancel/<slug:uuid>', views.scrobble_cancel, name='cancel'),
    path(
        'upload/',
        views.AudioScrobblerImportCreateView.as_view(),
        name='audioscrobbler-file-upload',
    ),
    path(
        'lastfm-import/',
        views.lastfm_import,
        name='lastfm-import',
    ),
    path(
        'webhook/jellyfin/',
        views.jellyfin_webhook,
        name='jellyfin-webhook',
    ),
    path(
        'webhook/mopidy/',
        views.mopidy_webhook,
        name='mopidy-webhook',
    ),
    path('export/', views.export, name='export'),
    path(
        'charts/',
        views.ChartRecordView.as_view(),
        name='charts-home',
    ),
]
