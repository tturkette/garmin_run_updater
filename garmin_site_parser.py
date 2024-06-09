from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv


# Access the login email and password key from the environment variable
load_dotenv()
email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")

# Define function to find element by id and send keys
def find_element_by_id_and_send_keys(element_id, keys):
    element = driver.find_element_by_id(element_id)
    element.send_keys(keys)

# Define function to find element by id and click
def find_element_by_id_and_click(element_id):
    element = driver.find_element_by_id(element_id)
    element.click()
    
# Create a new instance of the Firefox browser
driver = webdriver.Firefox()

# Navigate to the website
driver.get("https://connect.garmin.com/signin")

# Wait for a few seconds
time.sleep(5)

# Find email field and send keys
find_element_by_id_and_send_keys("email", email)

# Find password field and send keys
find_element_by_id_and_send_keys("password", password)

# Find and send return key to password field
find_element_by_id_and_send_keys("password", Keys.RETURN)

# Wait for a few seconds
time.sleep(5)

# Navigate to the workouts page
driver.get("https://connect.garmin.com/modern/workouts")

# Wait for a few seconds
time.sleep(5)

# Select workout type dropdown and select Run
find_element_by_id_and_send_keys("workoutType", "Run")

# Find Create Workout button and click
find_element_by_id_and_click("createWorkout")

# Wait for a few seconds
time.sleep(5)

# Find edit workout button and click
find_element_by_id_and_click("inline-edit-trigger")

# Find workout name field and enter workout name
find_element_by_id_and_send_keys("inline-edit-target", "Test Workout")

# Find save workout name button and click
find_element_by_id_and_click("inline-edit-save")

# Define edit step function
def edit_step(current_step_type, current_step_duration_type, current_step_duration,
              current_distance_unit=None, current_pace_from=None,
              current_pace_to=None, current_step_target_type=None):
    
    # Find and click the edit button for the current step type
    edit_button = driver.find_element(By.CSS_SELECTOR, "span.editable-step-title[title='%s'] + button.editable-step-edit-button" %current_step_type)
    edit_button.click()

    # Find step duration type dropdown and select current step duration type
    find_element_by_id_and_send_keys("select-step-duration", current_step_duration_type)

    if current_step_duration_type == "Time":
        # Enter current step duration in duration time input field in hh:mm:ss format
        find_element_by_id_and_send_keys("stepDurationTime", current_step_duration)
            
    if current_step_duration_type == "Distance":
        # Enter current step duration in duration distance input field
        find_element_by_id_and_send_keys("stepDurationDistance", current_step_duration)
        # Select distance unit dropdown
        find_element_by_id_and_send_keys("stepDurationDistanceUnit", current_distance_unit)
    
    # Select the step target dropdown
   find_element_by_id_and_send_keys("select-step-target", current_step_target_type)

    if current_step_target_type=="Pace":
        #Enter pace from
        find_element_by_id_and_send_keys("target-pace-from", current_pace_from)
        
        #Enter pace to
        find_element_by_id_and_send_keys("target-pace-to", current_pace_to)

    # Click the done button
    find_element_by_id_and_click("Done")
    



# Create a class to represent a workout composed of multiple workout steps
class Workout:
    def __init__(self, workout_name, workout_steps):
        self.workout_name = workout_name
        self.workout_steps = workout_steps

    # Define a function to create a workout from a file containing multiple workout steps
    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            workout_name = lines[0].strip()
            workout_steps = []
            for line in lines[1:]:
                step_type, step_duration_type, step_duration, distance_unit, pace_from, pace_to, step_target_type = line.split(',')
                workout_step = WorkoutStep(step_type, step_duration_type, step_duration, distance_unit, pace_from, pace_to, step_target_type)
                workout_steps.append(workout_step)
            return cls(workout_name, workout_steps)

    # Define a function to create the workout on the Garmin Connect website
    def create_on_garmin_connect(self):
        # Navigate to the workouts page
        driver.get("https://connect.garmin.com/modern/workouts")
        time.sleep(5)

        # Select workout type dropdown and select Run
        find_element_by_id_and_send_keys("workoutType", "Run")

        # Find Create Workout button and click
        find_element_by_id_and_click("createWorkout")

        # Wait for a few seconds
        time.sleep(5)

        # Find edit workout button and click
        find_element_by_id_and_click("inline-edit-trigger")

        # Find workout name field and enter workout name
        find_element_by_id_and_send_keys("inline-edit-target", self.workout_name)

        # Find save workout name button and click
        find_element_by_id_and_click("inline-edit-save")

        # Wait for a few seconds
        time.sleep(5)

        # Loop through the workout steps and edit each step
        for workout_step in self.workout_steps:
            edit_step(workout_step.step_type, workout_step.step_duration_type, workout_step.step_duration,
                      workout_step.distance_unit, workout_step.pace_from,
                      workout_step.pace_to, workout_step.step_target_type)
            time.sleep(5)





