"""Numpy sucks so I made my own functions to do what I need"""

import re


def get_sum(list:list):
    """Get sum of list

    Args:
        list (list): List

    Returns:
        float: Sum of list
    """
    sum = 0
    if len(list) == 0:
        return 0
    else:
        for i in list:
            sum += float(i)
        return sum

def get_multsum(list1:list, list2:list):
    """Get sum of two lists

    Args:
        list1 (list): List 1
        list2 (list): List 2

    Returns:
        float: Sum of list 1 and list 2
    """
    sum = 0
    for i, j in zip(list1, list2):
        sum += float(i) * float(j)
    return sum

def get_average(list:list):
    """Get average of list

    Args:
        list (list): List

    Returns:
        float: Average of list
    """
    average = get_sum(list) / len(list)
    return average

def get_ects_per_stuff(string:str):
    """Get ECTS from string

    Args:
        string (str): String

    Returns:
        ects_vo (list): ECTS for VO
        ects_ue (list): ECTS for UE
        ects_pue (list): ECTS for PUE
        ects_vu (list): ECTS for VU
        ects_lp (list): ECTS for LP
        ects_modulpruefung (list): ECTS for Modulprüfung
        ects_se (list): ECTS for SE
        
    """
        
    # Teilen Sie den Text in Zeilen auf
    # Listen zum Speichern der ECTS-Punkte
    single_line_text = string.replace("\n", " ")
    # Listen zum Speichern der ECTS-Punkte
    ects_vo = []
    ects_ue = []
    ects_pue = []
    ects_vu = []
    ects_lp = []
    ects_modulpruefung = []
    ects_se = [] 

    # Suchen Sie nach ECTS-Punkten für VO
    match_vo = re.findall(r'VO .*? (\d+\.\d+) ECTS', single_line_text)
    if match_vo:
        ects_vo.extend([float(ects) for ects in match_vo])

    # Suchen Sie nach ECTS-Punkten für PUE
    match_pue = re.findall(r'PUE .*? (\d+\.\d+) ECTS', single_line_text)
    if match_pue:
        ects_pue.extend([float(ects) for ects in match_pue])

    # Suchen Sie nach ECTS-Punkten für UE
    match_ue = re.findall(r'UE .*? (\d+\.\d+) ECTS', single_line_text)
    if match_ue:
        ects_ue.extend([float(ects) for ects in match_ue])

    # Suchen Sie nach ECTS-Punkten für VU
    match_vu = re.findall(r'VU .*? (\d+\.\d+) ECTS', single_line_text)
    if match_vu:
        ects_vu.extend([float(ects) for ects in match_vu])

    # Suchen Sie nach ECTS-Punkten für LP
    match_lp = re.findall(r'LP .*? (\d+\.\d+) ECTS', single_line_text)
    if match_lp:
        ects_lp.extend([float(ects) for ects in match_lp])

    # Suchen Sie nach ECTS-Punkten für Modulprüfung
    match_modulpruefung = re.findall(r'Modulprüfung .*? (\d+\.\d+) ECTS', single_line_text)
    if match_modulpruefung:
        ects_modulpruefung.extend([float(ects) for ects in match_modulpruefung])

    # Suchen Sie nach ECTS-Punkten für SE
    match_se = re.findall(r'SE .*? (\d+\.\d+) ECTS', single_line_text)
    if match_se:
        ects_se.extend([float(ects) for ects in match_se])

    return ects_vo, ects_ue, ects_pue, ects_vu, ects_lp, ects_modulpruefung, ects_se

def extract_ects_per_semester(text):
    """
    Extracts the ECTS points per semester from a given text.

    The text should contain lines that either contain a semester (WiSe YYYY or SoSe YYYY) or a number of ECTS points.

    Args:
        text (str): The text from which the ECTS points should be extracted.

    Returns:
        dict: A dictionary containing a list of associated ECTS points for each found semester.
    """

    # Split the text into lines
    lines = text.split('\n')

    # Initialize the dictionary that will store the ECTS points per semester
    ects_per_semester = {}
    current_semester = None

    for line in lines:
        # Check if the line contains a semester
        semester_match = re.search(r"(WiSe \d{4}|SoSe \d{4})", line)
        if semester_match:
            current_semester = semester_match.group(0)
            if current_semester not in ects_per_semester:
                ects_per_semester[current_semester] = []
        else:
            # Check if the line contains ECTS points (after the semester has been found, then you check from line to line if there are ECTS points if you find a new semester you change the semester)
            ects_match = re.search(r"(\d+(\.\d{1,2})?) ECTS", line)
            if ects_match and current_semester is not None:
                ects = float(ects_match.group(1))
                ects_per_semester[current_semester].append(ects)

    return ects_per_semester
def get_semesters(string, semesters):
    """Get semesters from string

    Args:
        string (str): String

    Returns:
        list: Semesters
    """
    # Teilen Sie den Text in Zeilen auf
    lines = string.split("\n")
    # Listen zum Speichern der Semester
    WiSes = []
    SoSes = []
    # Suchen Sie nach Semestern
    for line in lines:
        match = re.findall(r'WiSe (\d{4})', line)
        if match:
            WiSes.extend(match)
        match = re.findall(r'SoSe (\d{4})', line)
        if match:
            SoSes.extend(match)
    # Create a list of semesters
    for semester in WiSes:
        semesters.append(f'WiSe {semester}')
    for semester in SoSes:
        semesters.append(f'SoSe {semester}')
    return semesters
