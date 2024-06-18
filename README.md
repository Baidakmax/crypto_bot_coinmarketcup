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
   

## File Descriptions

- **bot.py:** The main entry point of the bot. It starts the bot and sets up handlers.
- **config.py:** Configuration file for environment variables.
- **database.py:** Contains functions for database operations (add, remove, get subscribers).
- **handlers.py:** Contains handlers for various bot commands and callbacks.
- **state.py:** Manages bot states.
- **tasks.py:** Contains periodic task functions, such as sending daily updates.
- **keyboards.py:** Defines inline and reply keyboards for user interaction.
- **parse.py:** Fetches and parses cryptocurrency data from CoinMarketCap.


### Usage

The bot supports the following commands:

- **/start or /help:** Display a welcome message and list available commands.
- **/prices:** Get the current prices of the top 10 cryptocurrencies.
- **/top5:** Display a menu with buttons for the top 5 cryptocurrencies.
- **/search_10:** Prompt the user to enter the name of a cryptocurrency to search within the top 10.
- **/search_100:** Prompt the user to enter the name of a cryptocurrency to search within the top 100.
- **/subscribe:** Subscribe to daily cryptocurrency updates.
- **/unsubscribe:** Unsubscribe from daily cryptocurrency updates.

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
