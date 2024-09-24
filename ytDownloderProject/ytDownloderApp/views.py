from django.shortcuts import render, redirect
import yt_dlp
from django.contrib import messages
from urllib.parse import urlparse, parse_qs

def home(request):
    return render(request, 'home.html')

def clean_youtube_url(url):
    parsed_url = urlparse(url)
    print(f"Parsed URL: {parsed_url}")
    
    if 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path[1:]
        cleaned_url = f"https://www.youtube.com/watch?v={video_id}"
    else:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
        cleaned_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else url
    
    print(f"Cleaned URL: {cleaned_url}")
    return cleaned_url

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')

        if not video_url:
            messages.error(request, "Please provide a YouTube video URL.")
            return redirect('home')

        video_url = clean_youtube_url(video_url)

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info without downloading
                info_dict = ydl.extract_info(video_url, download=False)  # Use download=False to avoid downloading
                video_title = info_dict.get('title', None)
                video_thumbnail = info_dict.get('thumbnail', None)
                video_duration = info_dict.get('duration', None)
                
                # Display video info but don't download yet
                context = {
                    'video_title': video_title,
                    'video_thumbnail': video_thumbnail,
                    'video_duration': video_duration,
                    'video_url': video_url,
                }
                return render(request, 'home.html', context)

        except yt_dlp.utils.DownloadError:
            messages.error(request, "Invalid YouTube URL or video details not found.")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('home')

    return render(request, 'home.html')

def start_download(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')

        if not video_url:
            messages.error(request, "Please provide a YouTube video URL.")
            return redirect('home')

        video_url = clean_youtube_url(video_url)

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)  # Download the video
                video_title = info_dict.get('title', None)
                
            messages.success(request, f"Video '{video_title}' downloaded successfully!")
            return redirect('home')

        except yt_dlp.utils.DownloadError:
            messages.error(request, "Invalid YouTube URL or download failed.")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('home')
