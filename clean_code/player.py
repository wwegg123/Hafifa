from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *
pygame.init()

class Playlist:
    def __init__(self):
        self.songs:list = []
        self.current_song:int = 0

    def add_songs(self, songs):
        self.songs.extend(songs)

    def get_current(self):
        return self.songs[self.current_song]
    
    def get_all(self):
        return self.songs
    
    def get_next_song(self):
        if self.current_song + 1 < len(self.songs):
            self.current_song += 1
        else:
            self.current_song = 0
        return self.current_song
    
    def get_previous_song(self):
        if self.current_song - 1 >= 0:
            self.current_song -= 1
        else:
            self.current_song = len(self.songs) - 1
        return self.current_song
    
class Player:
    def __init__(self):
        self.paused: bool = False
        self.song_end: int = pygame.USEREVENT + 1

    def play(self,file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_endevent(self.song_end)
        self.paused = False

    def pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def get_end(self):
        return self.song_end
    
class FrameApp(Frame):
    def __init__(self,master):
        super(FrameApp, self).__init__(master)
        self.grid()

        self.playlist = Playlist()
        self.player = Player()

        self._build_ui()

        self.after(100, self.poll_music)
        
    def _build_ui(self):
        self.play_btn: Button = Button(self, text="PLAY SONG",command=self.play_song,bg='AntiqueWhite1',width=40)
        self.play_btn.grid(row=2,column=0)
        
        self.previous_btn: Button = Button(self, text="PREVIOUS SONG",command=self.previous_song,bg='AntiqueWhite1',width=40)
        self.previous_btn.grid(row=4,column=0)
        
        self.pause_btn: Button = Button(self, text="PAUSE/UNPAUSE",command=self.player.pause,bg='AntiqueWhite1',width=40)
        self.pause_btn.grid(row=3,column=0)
        
        self.next_btn: Button = Button(self, text="NEXT SONG",command=self.next_song,bg='AntiqueWhite1',width=40)
        self.next_btn.grid(row=5,column=0)
        
        self.add_btn: Button = Button(self, text="ADD TO LIST",command=self.add_songs,bg='AntiqueWhite1',width=40)
        self.add_btn.grid(row=1,column=0)
        
        self.currently_playing = Label(self, fg='Black',font=('Helvetica 12 bold italic',10),bg='ivory2')
        self.currently_playing.grid(row=6,column=0)
        
        self.playlist_songs = Text(self,wrap=WORD,width=60)
        self.playlist_songs.grid(row=8,column=0)
        
    #################################################################################
    def add_songs(self):
        files = askopenfilenames()
        self.playlist.add_songs(files)
        self.render_playlist()

    def render_playlist(self):
        self.playlist_songs.delete("1.0", END)
        for key, song_path in enumerate(self.playlist.get_all()):
            song = EasyID3(song_path)
            song_data = (str(key + 1) + ' : ' + song['title'][0] + ' - ' +
                song['artist'][0])
            self.playlist_songs.insert(END, song_data + '\n')
    #################################################################################
    def song_data(self):
        try:
            song = EasyID3(self.songs[self.current_song])
            song_data = "Now playing: Nr:" + str(self.current_song + 1) + " " + \
                        str(song['title']) + " - " + str(song['artist'])
            return song_data
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def play_song(self):
        path = self.playlist.get_current()
        self.player.play(path)
        self.update_currently_playing()
    #################################################################################
    def next_song(self):
        self.playlist.get_next_song()
        self.play_song()
    #################################################################################
    def previous_song(self):
        self.playlist.get_previous_song()
        self.play_song()
    #################################################################################
    def update_currently_playing(self):
            song = EasyID3(self.playlist.get_current())
            text = f"Now playing: {song['title'][0]} - {song['artist'][0]}"
            self.currently_playing.config(text=text)
    #################################################################################
    def poll_music(self):
        for event in pygame.event.get():
            if event.type == self.player.get_end():
                self.next_song()

        self.after(100, self.poll_music)
#################################################################################
window = Tk()
window.geometry("500x500")
window.title("MP3 Music Player")
#################################################################################
app = FrameApp(window)
#################################################################################
window.mainloop()