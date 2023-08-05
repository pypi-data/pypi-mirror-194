"""Additional bot utility for using Sheet-based commands."""
import gspread


def retrieve_sheet(gc, sheet_id):
    """Retrieve sheet data from a Google Sheet."""
    # Open the google sheet according to its ID
    sheet_handler = gc.open_by_key(sheet_id)
    # Retrieve the grabbed values from the sheet as a list of lists
    return sheet_handler.sheet1.get_all_values()[3:]


def search_sheet(sheet_data, search_phrase):
    """Search sheet data for rows containing terms from search phrase."""
    search_hits = []
    for row in sheet_data:
        for item in row:
            if item.lower() in search_phrase.lower():
                search_hits.append(row)
                # Below break required to ensure each item is only added as a hit once
                break
    return search_hits


def get_command_or_id(sheet_row):
    """Execute a command or navigate to a new sheet."""
    # If the final entry in a row isn't blank (i.e., the row leads to a Sheet ID)
    if sheet_row[-1] != 'N/A':
        return sheet_row[-1], "id"
    # If the final entry IS blank (i.e., the row terminates in a command)
    else:
        return sheet_row[-2], "cmd"


def strip_student_id(id_message):
    """Strip extra characters from student-provided ID."""
    message_components = id_message.split(" ")
    student_id = message_components[1]
    return student_id


def write_data_pair(gc, sheet_id, left_value, right_value):
    """Write data pair to Google Sheet."""
    sheet_handler = gc.open_by_key(sheet_id)
    original_end_cell = sheet_handler.sheet1.find("sheet_end")
    end_row = original_end_cell.row
    cell_update_start_range = f"A{end_row}"
    cell_update_end_range = f"B{end_row+1}"
    sheet_handler.sheet1.update(f"{cell_update_start_range}:{cell_update_end_range}",
        [[left_value, right_value], ["sheet_end", "end_sheet"]])
    

def retrieve_student_id(gc, sheet_id, discord_id):
    sheet_handler = gc.open_by_key(sheet_id)
    student_id_roster = sheet_handler.sheet1.get_all_values()
    for student in student_id_roster:
        if discord_id == student[0]:
            return student[1]
    student = "not found"
    return student


def retrieve_itemized_grade_from_gradebook(gc, sheet_id, student_id):
    sheet_handler = gc.open_by_key(sheet_id)
    gradebook = sheet_handler.sheet1.get_all_values()
    headers = gradebook[1][2:-1]
    for student_grades in gradebook:
        if student_id in student_grades:
            grades = student_grades[2:-1]
            total_grade = student_grades[-1]
            student = student_grades[0]
            return student, headers, grades, total_grade
    student = "not found"
    grades = "not found"
    total_grade = "not found"
    return student, headers, grades, total_grade


def format_grade_report(headers, grades):
    formatted_report = ""
    index = 0
    for header in headers:
        if grades[index] != "":
            formatted_report += f"{header}:  {grades[index]}\n"
        else:
            formatted_report += f"{header}:  Not Reported Yet\n"
        index += 1
    return formatted_report


def get_grade_report_color(total_grade):
    emergency_color = 0xED1A13
    warning_color = 0xFAC720
    comfortable_color = 0x04B021
    if int(total_grade) >= 80:
        chosen_color = comfortable_color
    elif int(total_grade) < 80 and int(total_grade) >= 70:
        chosen_color = warning_color
    else:
        chosen_color = emergency_color
    return chosen_color

def get_command_list(gc, sheet_id):
    command_list = []
    sheet_handler = gc.open_by_key(sheet_id)
    sheet = sheet_handler.sheet1.get_all_values()
    for course in sheet[3:]:
        command_list.append(course[0])
    return command_list