from pytube import YouTube, Playlist, request
from pytube.cli import on_progress
import os
import subprocess

request.default_range_size = 1048576

#download all videos of a playlist in mp3 format
def downloadPlaylist(link,outputPath):
    playlist = Playlist(link)
    counter = 0
    playlistLength = playlist.length
    print("Starting downloading playlist : "+ playlist.title)
    
    #for each video in the playlist download it
    for video in playlist.videos:
        downloadVideo(video,outputPath)
        counter+=1
        print("Completed "+str(counter)+"/"+str(playlistLength)+"\n")

#download a youtube video : youtube object passed as a parameter
def downloadVideo(yt_video,outputPath):

    videoTitle = yt_video.title
    yt_video.register_on_progress_callback(on_progress)

    print("Getting audio stream of "+videoTitle)
    yt_streams = yt_video.streams.get_by_itag(251)
    defaultVideoTitle = yt_streams.default_filename 
    print("Downloading "+videoTitle)
    yt_streams.download(output_path=outputPath)
    print("Track downloaded successfully")
    print("Converting to mp3")
    webmToMp3(outputPath,defaultVideoTitle)

#download a single youtube video : link passed as a parameter
def downloadSingleVideo(yt_video_link,outputPath):
    yt_video = YouTube(yt_video_link)
    downloadVideo(yt_video,outputPath)
    
#As the livrary download videos in .webm format, we convert 
#them right after in .mp3 320K
def webmToMp3(path,file):
        webmFile = os.path.join(path, file)
        mp3File = os.path.join(path, file).replace(
            "webm", "mp3")

        command = f"ffmpeg -i \'{webmFile}\' -vn -ab 320k -ar 44100 -y \'{mp3File}\'"
        subprocess.call(command, shell=True,stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT) 
        os.remove(webmFile)
    

downloadPlaylist("https://www.youtube.com/playlist?list=PL7E8bUldShsebebk0ByXYzGuPYMtPVb6H","playlist_output")
