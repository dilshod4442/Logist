import mimetypes
import os
import re
from urllib.parse import urlparse, parse_qs

from django.conf import settings
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Material, Video

CHUNK_SIZE = 1024 * 1024
VIDEO_MIME = {".mp4": "video/mp4", ".webm": "video/webm"}

def _range_response(request, field, *, mime_type=None, inline=False, filename=None):
    """Stream one requested byte range at a time; never buffer a full media file."""
    if not field:
        raise Http404
    try:
        file_obj = field.open("rb")
        size = field.size
    except (OSError, ValueError):
        raise Http404
    content_type = mime_type or mimetypes.guess_type(filename or field.name)[0] or "application/octet-stream"
    range_header = request.headers.get("Range", "")
    status = 200
    start, end = 0, size - 1
    if range_header:
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
        if not match or (not match.group(1) and not match.group(2)) or size <= 0:
            file_obj.close()
            response = HttpResponse(status=416)
            response["Content-Range"] = f"bytes */{size}"
            response["Accept-Ranges"] = "bytes"
            return response
        if match.group(1):
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else size - 1
        else:
            suffix = int(match.group(2))
            start = max(0, size - suffix)
        if start >= size or end < start:
            file_obj.close()
            response = HttpResponse(status=416)
            response["Content-Range"] = f"bytes */{size}"
            response["Accept-Ranges"] = "bytes"
            return response
        end = min(end, size - 1)
        status = 206
    length = max(0, end - start + 1)
    file_obj.seek(start)
    def chunks():
        remaining = length
        try:
            while remaining:
                block = file_obj.read(min(CHUNK_SIZE, remaining))
                if not block:
                    break
                remaining -= len(block)
                yield block
        finally:
            file_obj.close()
    response = StreamingHttpResponse(chunks(), status=status, content_type=content_type)
    response["Accept-Ranges"] = "bytes"
    response["Content-Length"] = str(length)
    response["X-Content-Type-Options"] = "nosniff"
    response["Content-Disposition"] = f'{"inline" if inline else "attachment"}; filename="{os.path.basename(filename or field.name)}"'
    if status == 206:
        response["Content-Range"] = f"bytes {start}-{end}/{size}"
    return response

def _embed_url(url):
    parsed = urlparse(url or "")
    host = (parsed.hostname or "").lower()
    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
        return f"https://www.youtube-nocookie.com/embed/{video_id}" if video_id else ""
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"}:
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        if parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
        if parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
        return f"https://www.youtube-nocookie.com/embed/{video_id}" if re.fullmatch(r"[A-Za-z0-9_-]{6,20}", video_id) else ""
    if host in {"vimeo.com", "www.vimeo.com"}:
        video_id = parsed.path.strip("/").split("/")[0]
        return f"https://player.vimeo.com/video/{video_id}" if video_id.isdigit() and len(video_id) <= 12 else ""
    return ""

def material_list(request):
    items = Material.objects.filter(status="published").select_related("topic")
    if not request.user.is_authenticated:
        items = items.filter(is_public=True)
    videos = Video.objects.filter(status="published").select_related("topic")
    video_cards = []
    for video in videos:
        ext = os.path.splitext(video.video_file.name)[1].lower() if video.video_file else ""
        video_cards.append({"video": video, "embed_url": _embed_url(video.external_url), "supported_file": ext in VIDEO_MIME, "mime_type": VIDEO_MIME.get(ext, "")})
    documents, video_files = [], []
    for item in items:
        ext = os.path.splitext(item.file.name)[1].lower()
        if ext in VIDEO_MIME:
            video_files.append({"item": item, "mime_type": VIDEO_MIME[ext]})
        else:
            documents.append(item)
    return render(request, "materials/list.html", {"materials": documents, "videos": video_cards, "video_files": video_files})

def download(request, pk):
    item = get_object_or_404(Material, pk=pk, status="published")
    if not item.is_public and not request.user.is_authenticated:
        raise Http404
    filename = os.path.basename(item.file.name)
    ext = os.path.splitext(filename)[1].lower()
    mime_type = "application/pdf" if ext == ".pdf" else VIDEO_MIME.get(ext)
    inline = request.GET.get("inline") == "1" and (mime_type == "application/pdf" or ext in VIDEO_MIME)
    return _range_response(request, item.file, mime_type=mime_type, inline=inline, filename=filename)

def stream_video(request, pk):
    video = get_object_or_404(Video, pk=pk, status="published")
    filename = os.path.basename(video.video_file.name)
    ext = os.path.splitext(filename)[1].lower()
    mime_type = VIDEO_MIME.get(ext)
    if not mime_type:
        raise Http404("Unsupported video format")
    return _range_response(request, video.video_file, mime_type=mime_type, inline=True, filename=filename)

def stream_material_video(request, pk):
    item = get_object_or_404(Material, pk=pk, status="published")
    if not item.is_public and not request.user.is_authenticated:
        raise Http404
    filename = os.path.basename(item.file.name)
    ext = os.path.splitext(filename)[1].lower()
    mime_type = VIDEO_MIME.get(ext)
    if not mime_type:
        raise Http404("Unsupported video format")
    return _range_response(request, item.file, mime_type=mime_type, inline=True, filename=filename)
