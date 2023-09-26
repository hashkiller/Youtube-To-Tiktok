import pytube
import moviepy.editor as mp
from colorama import Fore
import os
import requests

def send_discord_webhook(url):
    discord_webhook_url = 'https://discord.com/api/webhooks/1156304785255968768/cjxy4ZTW8sWzDL4WI8Bm1Iw7BGuJfiPSpo7tEVabzs37i038_82ygIT0TLaFbXhnnvJY'  # Remplacez par votre URL de webhook Discord
    data = {'content': url}
    response = requests.post(discord_webhook_url, json=data)
    if response.status_code == 204:
        print(f"{Fore.GREEN}[+]{Fore.RESET} URL envoyée avec succès dans le webhook Discord.")
    else:
        print(f"{Fore.RED}[-]{Fore.RESET} Échec de l'envoi de l'URL dans le webhook Discord. Code d'état : {response.status_code}")

while True:
    video_url = input(f'{Fore.GREEN}[+]{Fore.RESET} URL de la vidéo YouTube : ')
    os.remove(video_filename)
    
    try:
        video_instance = pytube.YouTube(video_url)
        stream = video_instance.streams.get_highest_resolution()
        
        if stream:
            video_filename = 'video.mp4'
            stream.download(filename=video_filename)
            print(f"Vidéo téléchargée avec succès sous le nom '{video_instance.title}'")
    
            video_clip = mp.VideoFileClip(video_filename)
    
            part_duration = 75
        
            num_parts = int(video_clip.duration / part_duration)
            for part_num in range(num_parts):
                start_time = part_num * part_duration
                end_time = (part_num + 1) * part_duration
        
                part_clip = video_clip.subclip(start_time, end_time)
        
                target_resolution = (1080, 1920)
        
                blank_clip = mp.ColorClip(target_resolution, color=(0, 0, 0), duration=part_clip.duration)
                
                sat_filepath = os.path.join("misc", "sat.mp4")
                
                sat_clip = mp.VideoFileClip(sat_filepath)
    
                sat_clip = sat_clip.subclip(0, part_clip.duration)
                
                sat_clip = sat_clip.resize(height=1200, width=1080)
                
                final_clip = mp.CompositeVideoClip([blank_clip, part_clip.set_position(('center', 'top')), sat_clip.set_position(('center', 'bottom'))])
        
                final_filename = f'partie_{part_num + 1}.mp4'
        
                final_clip.write_videofile(final_filename, codec='libx264', threads=4)
        
                print(f"{Fore.GREEN}[+]{Fore.RESET} Partie {part_num + 1} générée avec succès {target_resolution[0]}x{target_resolution[1]}.")
                
                upload_url = 'https://tmpfiles.org/api/v1/upload'
                files = {'file': open(final_filename, 'rb')}
                response = requests.post(upload_url, files=files)
                if response.status_code == 200:
                    send_discord_webhook(response.json()['data']['url'])
                else:
                    print(f"{Fore.RED}[-]{Fore.RESET} Échec de l'envoi de la partie dans le webhook Discord. Code d'état : {response.status_code}")
                
        
        else:
            print(f"{Fore.RED}[-]{Fore.RESET} Aucun flux vidéo de la plus haute résolution trouvé pour cette vidéo.")
    
    except Exception as e:
        print(f"{Fore.RED}[-]{Fore.RESET} Une erreur s'est produite : {e}")
