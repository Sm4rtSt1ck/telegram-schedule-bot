# University Schedule Telegram Bot

This is a simple Telegram bot that allows students to view their university schedule by selecting their group from a list. The bot reads the schedule from a CSV file and displays it in a user-friendly format.

## Features

- **Group Selection:** Users can select their group to view the schedule.
- **Schedule Display:** The schedule is displayed with formatted text for better readability.
- **Back Button:** Users can navigate back to the group selection menu.

## Setup

### Prerequisites

- Python 3.7+
- `python-telegram-bot` library
- `python-dotenv` library

### Installation

1. **Clone the repository:**
```sh
git clone https://github.com/Sm4rtSt1ck/telegram-schedule-bot.git
```

2. **Install the required libraries:**

```sh
pip install python-telegram-bot python-dotenv
```

3. **Create a `.env` file and add your Telegram bot token:**

```plaintext
TOKEN=YOUR:TOKEN
```

4. **Prepare your schedule CSV file:**

The CSV file should be named `schedule.csv` and have the following structure:

```csv
Group,Day,Time,Subject,Room
Group1,1,08:00-09:30,Math,Room 101
Group1,2,09:45-11:15,Physics,Room 102
...
```
where `Day` is the number of the day in the week (1-7)

## Usage

1. **Run the bot:**

```sh
python main.py
```

2. **Interact with the bot:**

    - Start the bot by sending the `/start` command.
    - Select your group from the list to view the schedule.
    - Use the "Back" button to return to the group selection menu.

## Code Overview

### Files

- **main.py:** The main script that runs the bot.
- **.env:** File containing the bot token and other settings (not included in the repository for security reasons).
- **schedule.csv:** CSV file containing the schedule (needs to be edited by the user).

### Functions

- **read_token:** Reads the bot token from `.env`.
- **start:** Sends a welcome message and prompts the user to select a group.
- **load_groups:** Loads the list of groups from the schedule CSV file.
- **load_schedule:** Loads the schedule for a specific group from the CSV file.
- **button:** Handles button clicks (group selection and back navigation).
- **send_group_selection:** Sends the group selection menu to the user.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project doesn't have a license because I'm a oboltus

