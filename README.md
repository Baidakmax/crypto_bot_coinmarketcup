# Crypto Price Bot

Crypto Price Bot - is a Telegram bot for parsing data on cryptocurrency rates from the CoinMarketCap 
website and sending it to users. The bot also supports subscription to daily updates of cryptocurrency rates.

## Getting Started

Follow these instructions to set up and run the project on your local computer.

### Pre-requisites

- Python 3.10+
- Docker(to run in a container)
- Telegram account

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Baidakmax/crypto_bot_coinmarketcup.git
    cd crypto_price_bot
    ```
2. Create and activate the virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3. Set Dependencies:

    ```bash
    pip install -r requirements.txt
    ```
   
4. Initialise the database:

   ```python
    from database import init_db
    init_db()
    ```

5. Insert your bot token into the `bot.py` file:

   ```python
    API_TOKEN = 'YOUR_BOT_API_TOKEN'
    ```
   
6. Run the bot:

   ```bash
    python bot.py
    ```
   
### Use

The bot supports the following commands:

- `/start` - Welcome message.
- `/prices` - Receive current cryptocurrency rates.
- `/subscribe` - Subscribe to daily updates of cryptocurrency rates.
- `/unsubscribe` - Unsubscribe from daily updates of cryptocurrency rates.

### Running in Docker

1. Build Docker-image

   ```bash
    docker build -t telegram-crypto-bot .
    ```
   
2. Run container:

   ```bash
    docker run -d --name crypto-bot-container telegram-crypto-bot
    ```

### Contribution to the project

Your contributions are welcome! Please create `pull requests` or open `issues` to improve the project.

### Licence

This project is licensed under the MIT licence. For more information, see. [LICENCE](LICENSE).
