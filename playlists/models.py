from core.models import *
from accounts.models import *
from django.utils.translation import gettext_lazy as _


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")

    title = models.CharField(_('title'), max_length=255)
    
    description = models.TextField(
        _('description'), null=True, blank=True)

    items = models.ManyToManyField("files.File", through='PlaylistItem', related_name="plaslist_items")

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    def __str__(self):
        return f"{self.pk}"

    def get_videos(self):
        return self.playlistitems.filter().all()


class PlaylistItem(models.Model):
    file = models.ForeignKey("files.File", on_delete=models.CASCADE, related_name="playlistitem_files")
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="playlistitems")
    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    class Meta:
        verbose_name = _('PlaylistItem')
        verbose_name_plural = _('PlaylistItems')
