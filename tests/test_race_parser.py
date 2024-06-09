import pytest
from race_info import read_race_csv

def test_valid_csv(tmp_path):
    # Create a temporary CSV file with valid data
    valid_csv = tmp_path / "race_info.csv"
    valid_csv.write_text("10,00:50:30\n5,00:25:15")
    
    expected_goal_race = [10, 0, 50, 30]
    expected_recent_race = [5, 0, 25, 15]
    
    goal_race, recent_race = read_race_csv(valid_csv)
    assert goal_race == expected_goal_race
    assert recent_race == expected_recent_race

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        read_race_csv('non_existent_file.csv')

def test_invalid_format(tmp_path):
    # Create a temporary CSV file with invalid time format
    invalid_csv = tmp_path / "invalid_race_info.csv"
    invalid_csv.write_text("10,00:50\n5,00:25:15")
    
    with pytest.raises(AssertionError):
        read_race_csv(invalid_csv)

def test_additional_lines(tmp_path):
    # Create a temporary CSV file with more than two lines
    extra_csv = tmp_path / "extra_race_info.csv"
    extra_csv.write_text("10,00:50:30\n5,00:25:15\n7,00:35:20")
    
    with pytest.raises(AssertionError):
        read_race_csv(extra_csv)

if __name__ == "__main__":
    pytest.main()

