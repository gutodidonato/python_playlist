import os
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, Text, END
import yt_dlp
import time

def select_folder():
    folder = filedialog.askdirectory()
    output_folder_var.set(folder)

def download_playlist():
    playlist_url = url_var.get()
    output_folder = output_folder_var.get()

    if not playlist_url or not output_folder:
        log_text.insert(END, "Por favor, insira uma URL válida e selecione uma pasta de saída.\n")
        return

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "progress_hooks": [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            log_text.insert(END, f"Processando playlist: {playlist_url}\n")
            try:
                ydl.download([playlist_url])
            except yt_dlp.utils.DownloadError as e:
                if "This video has been removed for violating YouTube's Terms of Service" in str(e):
                    log_text.insert(END, "Vídeo removido por violar os Termos de Serviço do YouTube. Pulando...\n")
                elif "Connection to" in str(e) and "timed out" in str(e):
                    log_text.insert(END, "Erro de conexão. Tentando novamente...\n")
                    time.sleep(5)  # Espera 5 segundos antes de tentar novamente
                    ydl.download([playlist_url])
                else:
                    log_text.insert(END, f"Erro ao processar a playlist: {e}\n")
                    return
    except Exception as e:
        log_text.insert(END, f"Erro ao processar a playlist: {e}\n")
        return

    log_text.insert(END, "Download e conversão concluídos.\n")

def progress_hook(d):
    if d["status"] == "downloading":
        log_text.insert(END, f"Baixando: {d['_percent_str']} concluído\n")
        log_text.see(END)
    elif d["status"] == "finished":
        log_text.insert(END, "Download concluído. Convertendo...\n")
        log_text.see(END)

# Interface gráfica usando Tkinter
app = Tk()
app.title("Downloader de Playlist do YouTube com yt-dlp")
app.geometry("600x400")

# URL da playlist
Label(app, text="URL da Playlist:").pack(pady=5)
url_var = StringVar()
Entry(app, textvariable=url_var, width=70).pack(pady=5)

# Pasta de saída
Label(app, text="Pasta de Saída:").pack(pady=5)
output_folder_var = StringVar()
Entry(app, textvariable=output_folder_var, width=50).pack(side="left", padx=10)
Button(app, text="Selecionar Pasta", command=select_folder).pack(side="left", padx=5)

# Botão para iniciar o download
Button(app, text="Baixar Playlist", command=download_playlist).pack(pady=20)

# Log de mensagens
Label(app, text="Log:").pack(pady=5)
log_text = Text(app, height=10, width=70)
log_text.pack(pady=5)

# Inicia a interface
app.mainloop()