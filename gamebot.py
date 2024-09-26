from mastodon import Mastodon
import requests
import random
from io import BytesIO
from PIL import Image

RAWG_API_KEY = 'd98a8d3efd7d4c62b46897e7c38a46d2'

MASTODON_CLIENT_KEY = 'TXdEgi13tR6S59s-5RmeT8zU8LDso6fuO2DCoOCL36Y'
MASTODON_CLIENT_SECRET = 'C759zcUuZZ5Efoo4RuCb4_C8w1Fz_BG9lSni7vXxHmA'
MASTODON_ACCESS_TOKEN = 'iYPS2WOwXcGjEc_ZdjImfq_UFwPRV5nWTsgX25fMss8'
MASTODON_API_BASE_URL = 'https://elytra15.com'  

RAWG_GAMEBOY_PLATFORM_IDS = [26, 49, 43, 77, 74]  


mastodon = Mastodon(
    client_id=MASTODON_CLIENT_KEY,
    client_secret=MASTODON_CLIENT_SECRET,
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url=MASTODON_API_BASE_URL
)


def get_random_gameboy_game():
    url = f"https://api.rawg.io/api/games"

    params = {
        'key': RAWG_API_KEY,
        'platforms': ','.join(map(str, RAWG_GAMEBOY_PLATFORM_IDS)),  
        'page_size': 1,
        'page': random.randint(1, 2030)  
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        game_data = response.json()
        if game_data['results']:
            game = game_data['results'][0]

            
            gameboy_platforms = []
            other_platforms = []

            for platform in game.get('platforms', []):
                platform_id = platform['platform']['id']
                platform_name = platform['platform']['name']

                if platform_id in RAWG_GAMEBOY_PLATFORM_IDS:
                    gameboy_platforms.append(platform_name)
                else:
                    other_platforms.append(platform_name)

            return {
                'name': game['name'],
                'released': game.get('released', 'N/A'),
                'background_image': game.get('background_image', ''),
                'gameboy_platforms': ', '.join(gameboy_platforms),  
                'other_platforms': ', '.join(other_platforms)  
            }
    else:
        print(f"Error fetching game data: {response.status_code} - {response.text}")

    return None


def compress_image(image_data, max_size_kb=20, min_quality=10):
    img = Image.open(BytesIO(image_data))
    
    
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')

    
    if len(img_byte_arr.getvalue()) > max_size_kb * 1024:
        quality = 85  
        while len(img_byte_arr.getvalue()) > max_size_kb * 1024 and quality >= min_quality:
            img_byte_arr = BytesIO()  
            img.save(img_byte_arr, format='JPEG', quality=quality)
            
            if len(img_byte_arr.getvalue()) > max_size_kb * 1024:
                
                width, height = img.size
                img = img.resize((int(width * 0.9), int(height * 0.9)))
            
            quality -= 5  
            
        return img_byte_arr.getvalue()

    return image_data


def post_to_mastodon(game):
    if not game:
        print("No game data found!")
        return

    
    hashtags = ' '.join([f"#{game['name'].replace(' ', '')}"] + [f"#{platform.replace(' ', '')}" for platform in game['gameboy_platforms'].split(', ')])

    
    post_content = (f"🎮 Random Retro Game:\n\n"
                    f"Title: {game['name']}\n"
                    f"Released: {game['released']}\n"
                    f"Platforms: {game['gameboy_platforms']}\n")

    if game['other_platforms']:
        post_content += f"Also released on: {game['other_platforms']}\n\n"

    post_content += f"\n{hashtags}"
    
    if game['background_image']:
        
        img_data = requests.get(game['background_image']).content
        
        if len(img_data) > 20 * 1024:  
            img_data = compress_image(img_data, max_size_kb=20)
        
        with open('game_image.jpg', 'wb') as handler:
            handler.write(img_data)

        media = mastodon.media_post('game_image.jpg', description=f"Cover image of {game['name']}")

        mastodon.status_post(post_content, media_ids=[media])
    else:
        
        mastodon.status_post(post_content)


if __name__ == "__main__":
    random_game = get_random_gameboy_game()
    post_to_mastodon(random_game)
