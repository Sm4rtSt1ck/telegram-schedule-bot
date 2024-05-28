from datetime import datetime
import csv
from os import getenv

from dotenv import load_dotenv
from telebot import TeleBot, types


load_dotenv("lang2.env")

WEEKDAYS = list(map(lambda day: day.replace("_", " "), getenv("WEEKDAYS").split()))
NOT_FOUND = getenv("NO_SCHEDULE")


class Schedule:
    def get_day(self, group: str) -> str:
        schedule = []
        with open("schedule.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Group'] == group and row['Day'] == str(datetime.now().weekday()+1):
                    formatted_entry = f"`{row['Time']}`: {row['Subject']}, _{row['Room']}_"
                    schedule.append(formatted_entry)
        return f"*{WEEKDAYS[datetime.now().weekday()]}:*\n{'\n'.join(schedule)}" if schedule else NOT_FOUND


    def get_week(self, group: str) -> str:
        schedule: dict[str, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        with open("schedule.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Group'] == group:
                    formatted_entry = f"`{row['Time']}`: {row['Subject']}, _{row['Room']}_"
                    schedule[int(row['Day'])].append(formatted_entry)
        result = ""
        for day, day_schedule in schedule.items():
            result += f"*{WEEKDAYS[day-1]}:*\n"
            result += ("\n".join(day_schedule) if len(day_schedule) > 0 else NOT_FOUND) + "\n\n"
        return result if schedule else NOT_FOUND


    def get_session(self, group: str) -> str:
        return NOT_FOUND
