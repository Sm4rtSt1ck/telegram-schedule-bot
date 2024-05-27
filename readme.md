# University Schedule Telegram Bot

This is a simple Telegram bot that allows students to view their university schedule by selecting their group from a list. The bot reads the schedule from a CSV file and displays it in a user-friendly format.

## Features

- **Group Selection:** Users can select their group to view the schedule
- **Schedule Display:** The schedule is displayed with formatted text for better readability
- **Buttons:** Users can navigate through the functionality using buttons

## Setup

### Prerequisites

- Python 3.7+
- `telebot` library
- `python-dotenv` library

### Installation

1. **Clone the repository:**
```sh
git clone https://github.com/Sm4rtSt1ck/telegram-schedule-bot
```

2. **Install the required libraries:**

```sh
pip install telebot python-dotenv
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

    - Start the bot by sending the `/start` command
    - Send your group to view the options
    - Use the buttons to view the schedule

## Code Overview

### Files

- **main.py:** The main script that runs the bot
- **.env:** File containing the bot token and other settings (not included in the repository for security reasons)
- **schedule.csv:** CSV file containing the schedule (needs to be edited by the user)

### Functions

- **start:** Sends a welcome message and prompts the user to select a group
- **set_group:** Writes a user group to the dictionary
- **select_schedule:** Allows the user to select a schedule
- **button:** Handles button clicks (schedule selection and back navigation)
- **load_day_schedule:** Loads the user's schedule for the current day
- **load_week_schedule:** Loads the user's schedule for the week
- **load_session_schedule:** Loads the user's schedule for the sessions

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project doesn't have a license because I'm a oboltus

