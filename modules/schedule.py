from datetime import datetime
import csv
from os import getenv
import re

from dotenv import load_dotenv
from telebot import TeleBot, types


load_dotenv("lang.env")

WEEKDAYS = list(map(lambda day: day.replace("_", " "), getenv("WEEKDAYS").split()))
NOT_FOUND = getenv("NO_SCHEDULE")


class Schedule:
    def check_group(self, group: str) -> bool:
        with open("schedule.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Group'] == group: return True
        return False

    def set_schedule(self, message: types.Message, group: str) -> bool:
        schedule_entry = message.text.split("\n")

        # Check if the schedule entry matches the required format
        entry_pattern = re.compile(r'^\d, \d{2}:\d{2}-\d{2}:\d{2}, [0-9a-zA-Zа-яА-Я]+, [0-9a-zA-Zа-яА-Я]+')
        for line in schedule_entry:
            if not entry_pattern.match(line):
                return False
            components = line.split(', ')
            day = int(components[0])
            time = components[1]
            subject = components[2]
            room = components[3]

            if not 1 <= day <= 7 or not subject or not room:
                return False

        with open("schedule.csv", 'a', newline='', encoding='utf-8') as csvfile:
            csvfile.write("\n")
            for line in schedule_entry:
                # Split the schedule entry into components
                components = line.split(', ')
                day = int(components[0])
                time = components[1]
                subject = components[2]
                room = components[3]

                # If all checks pass, append the schedule to the CSV file
                writer = csv.writer(csvfile)
                writer.writerow([group, day, time, subject, room])
        
        return True

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
        return getenv("IN_DEVELOPING")
