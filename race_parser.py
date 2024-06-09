from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='race_info.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_race_csv(file_path: str) -> Tuple[List[int], List[int]]:
    """
    Reads a CSV file with race distance and time in hh:mm:ss format.
    Returns two lists: one for goal race and one for recent race information.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Tuple[List[int], List[int]]: Two lists each containing race_distance, hours, minutes, and seconds.
    """
    def parse_time(time_str: str) -> Tuple[int, int, int]:
        """Parses a time string in hh:mm:ss format into hours, minutes, and seconds."""
        try:
            parts = time_str.split(':')
            assert len(parts) == 3, "Time format should be hh:mm:ss"
            hours, minutes, seconds = map(int, parts)
            return hours, minutes, seconds
        except Exception as e:
            logging.error(f"Error parsing time: {time_str} - {str(e)}")
            raise
    
    race_info = []
    
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    assert len(row) == 2, "Each row must have exactly two columns"
                    race_distance = int(row[0])
                    hours, minutes, seconds = parse_time(row[1])
                    race_info.append([race_distance, hours, minutes, seconds])
                except AssertionError as ae:
                    logging.error(f"Assertion error: {str(ae)}")
                    raise
                except ValueError as ve:
                    logging.error(f"Value error: {str(ve)}")
                    raise
                except Exception as e:
                    logging.error(f"Unexpected error: {str(e)}")
                    raise
        
        assert len(race_info) == 2, "CSV file must contain exactly two lines of race information"
        
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while reading the CSV file: {str(e)}")
        raise
    
    return race_info[0], race_info[1]

# Example usage (assuming 'race_info.csv' exists in the same directory):
# goal_race, recent_race = read_race_csv('race_info.csv')
# print(goal_race)
# print(recent_race)
