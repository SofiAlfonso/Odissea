from django.shortcuts import render, redirect
from .forms import AudioFileForm

def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('audio_success')
    else:
        form = AudioFileForm()
    return render(request, 'upload_audio.html', {'form': form})

def upload_success(request):
    return render(request, 'audio_success.html')
