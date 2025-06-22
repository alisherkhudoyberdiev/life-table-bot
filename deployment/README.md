# Life Table Bot

This is a Telegram bot that sends you a personalized "Life in Weeks" chart every week, showing your life's progress one square at a time.

![Example Image](https://i.imgur.com/7A5zZtS.png)

## Features

- Set your birthday to get a personalized chart.
- Receive an updated chart automatically every week.
- Request your chart at any time with a command.

## How to Run

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file**
    Create a file named `.env` in the project root and add your Telegram Bot Token.

    ```
    TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
    ```

5.  **Add Font File**
    The bot uses the Arial font to generate the image. Please download `arial.ttf` and place it in the same directory as `bot.py` and `life_table.py`. You can usually find this font on your system or download it from various font websites.

6.  **Run the bot**
    ```bash
    python3 bot.py
    ```

## How to Use the Bot

1.  Start a conversation with your bot on Telegram.
2.  Use the `/start` command.
3.  Set your birthday using the `/set_birthday YYYY-MM-DD` command.
4.  You will receive your first chart immediately. After that, you will get an updated one every 7 days.
5.  Use the `/table` command to get your chart at any time.

---
*This bot was created with the help of an AI assistant.* 