
# Mastodon Retro Game Poster

This Python script fetches random Game Boy games using the [RAWG API](https://rawg.io/apidocs) and automatically posts the game information and cover image to Mastodon. The script can be scheduled to run periodically using `cron`, making it a perfect tool for sharing random retro games on your Mastodon account. My account is available at [Elytra15](https://elytra15.com/@retrogame)

## Features

- Fetches a random retro game from the RAWG API.
- Posts the game title, release date, and platforms to Mastodon.
- Automatically resizes and compresses the game cover image if needed.
- Generates hashtags based on the game and platforms.
- Easy setup and can be scheduled via `cron` for regular posts.
- Generate ALT text

## Requirements

- Python 3.7+
- Mastodon account and API keys
- RAWG API key

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Elytra15/mastodon-retrogame.git
   cd mastodon-retrogame
   ```

2. **Install the dependencies:**

   Ensure you have `pip` installed. If not, you can install it using:

   ```bash
   sudo apt-get install python3-pip
   ```

   Then, install the required dependencies using using `pip:

   ```bash
   pip install Mastodon.py requests pillow
   ```

3. **Get API Keys:**

   - [Create a RAWG API key](https://rawg.io/apidocs) to fetch game data.
   - [Create a Mastodon API application](https://docs.joinmastodon.org/client/intro/) to get the client ID, client secret, and access token.

4. **Configure the API Keys:**

   In the script, replace the following placeholders with your actual keys:

   ```python
   RAWG_API_KEY = 'YOUR-RAWG-API-KEY'
   MASTODON_CLIENT_KEY = 'YOUR-MASTODON-CLIENT-KEY'
   MASTODON_CLIENT_SECRET = 'YOUR-MASTODON-CLIENT-SECRET'
   MASTODON_ACCESS_TOKEN = 'YOUR-MASTODON-ACCESS-TOKEN'
   ```

## Usage

Run the script directly to post a random Game Boy game to your Mastodon account:

```bash
python3 gamebot.py
```

This will fetch a random Game Boy game, retrieve its details, and post them along with a cover image to your Mastodon feed.

## Scheduling the Script with `cron`

To schedule the script to run at regular intervals (e.g., daily), you can set up a cron job.

1. Open your crontab file:

   ```bash
   crontab -e
   ```

2. Add the following line to schedule the script (this example runs it every day at 9:00 AM):

   ```bash
   0 9 * * * /path/to/your/venv/bin/python /path/to/mastodon-retrogame/gamebot.py
   ```

   Replace `/path/to/your/venv/bin/python` with the full path to the Python binary in your virtual environment, and `/path/to/mastodon-retrogame/post_random_game.py` with the full path to the script.

3. Save and exit the crontab editor.

Now, the script will automatically run at the specified time, posting a random game to your Mastodon account.

## Customization

- **Adjusting game platforms:**  
  The script currently fetches Game Boy, Game Boy Color, NES, Sega Game Gear and Sega Master System. You can modify the `RAWG_GAMEBOY_PLATFORM_IDS` list to include different platform IDs from RAWG API.

- **Image compression settings:**  
  The `compress_image` function reduces the size of the game cover image to fit Mastodon's file size limits (20KB). You can adjust this limit and image quality by modifying the `max_size_kb` and `min_quality` parameters.

## License

Free to use.

---
