"""Numpy sucks so I made my own functions to do what I need"""
import fitz
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
    """Get sum of list1 * list2

    Args:
        list1 (list): List 1
        list2 (list): List 2

    Returns:
        float: Sum of list1 * list2
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

def extract_ects_per_semester(text:str):
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
    accepted_years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]

    for i in range(len(lines)):
        line = lines[i]

        # Check if the line contains a year (WiSe YYYY or SoSe YYYY)
        year_match = re.search(r"\b\d{4}\b", line)
        ects_match = re.search(r"(\d+(\.\d{1,2})?) ECTS", line)

        # Check if the year is in the accepted years
        current_year = None
        ects_search = False
        if year_match:
            current_year = year_match.group(0)

        if ects_match: # If the line contains ECTS points
            ects_search = True 


        if not ects_search and current_year not in accepted_years:
            continue

        if year_match or ects_search: # If the line contains a year or ECTS points
            if year_match:
                year = year_match.group(0)
                # Check if the line contains a semester
                semester_match = False
                semester_match = re.search(r"(WiSe|SoSe)", line)
                if semester_match: # If the line contains a semester
                    current_semester = semester_match.group(0) + " " + year # Get the semester
                    if current_semester not in ects_per_semester: # If the semester is not in the ects_per_semester dictionary
                        ects_per_semester[current_semester] = [] # Add the semester to the ects_per_semester dictionary
                else: # If the line does not contain a semester
                    semester_match = re.search(r"(WiSe|SoSe)", lines[i - 1]) # Check the previous line for a semester
                    if semester_match:
                        current_semester = semester_match.group(0) + " " + year # Get the semester
                        if current_semester not in ects_per_semester: # If the semester is not in the ects_per_semester dictionary
                            ects_per_semester[current_semester] = [] # Add the semester to the ects_per_semester dictionary
            elif ects_search:
                # Check if the line contains ECTS points
                ects_match = re.search(r"(\d+(\.\d{1,2})?) ECTS", line) # Search for ECTS points
                if ects_match and current_semester is not None:
                    ects = float(ects_match.group(1)) # Get the ECTS points
                    ects_per_semester[current_semester].append(ects) # Add the ECTS points to the ects_per_semester dictionary

    return ects_per_semester

def get_semesters(string:str, semesters:list):
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
    
    # Kombinieren Sie alle Zeilen in einer einzigen Zeichenkette und ersetzen Sie Zeilenumbrüche durch Leerzeichen
    text = ' '.join(lines)

    # Suchen Sie nach Semestern
    match = re.findall(r'WiSe\s*(\d{4})', text)
    if match:
        WiSes.extend(match)
    match = re.findall(r'SoSe\s*(\d{4})', text)
    if match:
        SoSes.extend(match)
    # Create a list of semesters
    for semester in WiSes:
        semesters.append(f'WiSe {semester}')
    for semester in SoSes:
        semesters.append(f'SoSe {semester}')
    print(semesters)
    print("lol")
    return semesters

def extract_relevant_ects_per_semester(text:str):
    """ Extracts the relevant ECTS points per semester from a given text.

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
    accepted_years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]
    keywords = ["VO", "UE", "PUE", "LP", "SE", "Modulprüfung", "VU"]

    for i in range(len(lines)):
        line = lines[i]
        # Check if the line contains a semester
        semester_match = re.search(r"(WiSe|SoSe)", line)
        if semester_match:
            year_match = re.search(r"\b\d{4}\b", line)
            current_year = False 
            if year_match: # When the year is found
                current_year = year_match.group(0) # Get the year
            if current_year not in accepted_years and current_year: # If the year is not in the accepted years, then continue
                continue

            if year_match: # If the year is found
                current_semester = semester_match.group(0) + " " + year_match.group(0)
                modulprüfung_match = re.search(r"(Modulprüfung)", line) # Check if the line contains Modulprüfung
                line_words = line.split() # Split the line into words
                other_lv_match = None # Initialize the other_lv_match variable

                for word in line_words: # Check if the line contains other LV types
                    if word in keywords:
                        other_lv_match = word
                        break

                if modulprüfung_match:
                    current_lv = "Modulprüfung" # If the line contains Modulprüfung, then set the current_lv to Modulprüfung

                elif other_lv_match:
                    current_lv = other_lv_match


                elif not modulprüfung_match and not other_lv_match: # If the line does not contain Modulprüfung and other LV types
                    # Check the previous line for the LV type
                    previous_line = lines[lines.index(line) - 1]
                    line_words = previous_line.split()
                    other_lv_match = None

                    for word in line_words:
                        if word in keywords:
                            other_lv_match = word
                            break

                    if other_lv_match:
                        current_lv = other_lv_match

                
                if current_semester not in ects_per_semester:
                    ects_per_semester[current_semester] = []
            else: # If the year is not found
                line = lines[i + 1] # Get the next line
                year_match = re.search(r"\b\d{4}\b", line) # Check if the line contains a year
                current_year = None  # Initialize the current_year variable
                if year_match:
                    current_year = year_match.group(0)
                if current_year not in accepted_years: # If the year is not in the accepted years, then continue
                    continue

                if year_match: # If the year is found
                    line = lines[i]
                    current_semester = semester_match.group(0) + " " + year_match.group(0) # Get the semester
                    modulprüfung_match = re.search(r"(Modulprüfung)", line) # Check if the line contains Modulprüfung
                    line_words = line.split() # Split the line into words
                    other_lv_match = None # Initialize the other_lv_match variable

                    # Search for other LV types
                    for word in line_words: 
                        if word in keywords:
                            other_lv_match = word
                            break

                    # Set the current_lv to the other_lv_match
                    if modulprüfung_match:
                        current_lv = "Modulprüfung"

                    # Set the current_lv to the other_lv_match
                    elif other_lv_match:
                        current_lv = other_lv_match


                    # If the line does not contain Modulprüfung and other LV types
                    elif not modulprüfung_match and not other_lv_match:
                        # Check the previous line for the LV type
                        previous_line = lines[lines.index(line) - 1]
                        line_words = line.split()
                        other_lv_match = None

                        for word in line_words: # Search for other LV types
                            if word in keywords: 
                                other_lv_match = word # Get the other LV type
                                break

                        if other_lv_match: # If the line contains other LV types
                            current_lv = other_lv_match # Set the current_lv to the other_lv_match
                    
                    if current_semester not in ects_per_semester:
                        ects_per_semester[current_semester] = [] # Add the semester to the ects_per_semester dictionary


        else:
            # Check if the line contains ECTS points (after the semester has been found, then you check from line to line if there are ECTS points if you find a new semester you change the semester)
            ects_match = re.search(r"(\d+(\.\d{1,2})?) ECTS", line)
            if ects_match and current_semester is not None:
                ects = float(ects_match.group(1))
                ects_per_semester[current_semester].append(ects)
                ects_per_semester[current_semester].append(current_lv)

    return ects_per_semester

def get_relevant_ects_per_semester(doc_path:str):
    """Get the relevant ECTS points per semester

    Args:
        doc_path (str): Path to the PDF file

    Returns:
        dict: Relevant ECTS points per semester
    """

    # Load the PDF file fitz 
    doc = fitz.open(doc_path)
    text_all = ""
    for i in range(doc.page_count):
        page = doc.load_page(i) 
        text = page.get_text()
        text_all += text

    ects_per_semester = extract_relevant_ects_per_semester(text_all)
    # print(ects_per_semester)

    ects_per_semester_sorted = {}

    for key, value in ects_per_semester.items():
        for i in range(len(value)):
            if value[i] == "VO":
                ects_per_semester_sorted[key, "VO"] = ects_per_semester_sorted.get((key, "VO"), 0) + value[i-1]
            elif value[i] == "UE":
                ects_per_semester_sorted[key, "UE"] = ects_per_semester_sorted.get((key, "UE"), 0) + value[i-1]
            elif value[i] == "PUE":
                ects_per_semester_sorted[key, "PUE"] = ects_per_semester_sorted.get((key, "PUE"), 0) + value[i-1]
            elif value[i] == "LP":
                ects_per_semester_sorted[key, "LP"] = ects_per_semester_sorted.get((key, "LP"), 0) + value[i-1]
            elif value[i] == "Modulprüfung":
                ects_per_semester_sorted[key, "Modulprüfung"] = ects_per_semester_sorted.get((key, "Modulprüfung"), 0) + value[i-1]
            elif value[i] == "SE":
                ects_per_semester_sorted[key, "SE"] = ects_per_semester_sorted.get((key, "SE"), 0) + value[i-1]
            elif value[i] == "VU":
                ects_per_semester_sorted[key, "VU"] = ects_per_semester_sorted.get((key, "VU"), 0) + value[i-1]

    return ects_per_semester_sorted

def get_sum_ects2(ects_per_semester_sorted:str):
    """Get the sum of ECTS points per semester
    
    Args:
        ects_per_semester_sorted (dict): ECTS points per semester
        
    Returns:
        dict: Sum of ECTS points per semester
    """
    ects_list = []
    for key, value in ects_per_semester_sorted.items():
        # Get the semester and the LV type
        semester, lv = key
        # Get the ECTS points
        ects = value
        ects_list.append((semester, lv, ects))

    # Create a dict per semester
    ects_per_semester = {}
    for semester, lv, ects in ects_list:
        if semester not in ects_per_semester:
            ects_per_semester[semester] = {}
        ects_per_semester[semester][lv] = ects

    

    # get the sum of ects per semester and subtract the ects from the pue
    ects_per_semester_sum = {}
    for semester, lv in ects_per_semester.items():
        ects_per_semester_sum[semester] = sum(lv.values()) - lv.get("PUE", 0)

    return ects_per_semester_sum

def get_semester_ects(ects_per_semester_sorted:str):
    """Get the ECTS points per semester, per LV type

    Args:
        ects_per_semester_sorted (dict): ECTS points per semester

    Returns:
        dict: ECTS points per semester, per LV type
    """
    ects_list = []
    for key, value in ects_per_semester_sorted.items():
        # Get the semester and the LV type
        semester, lv = key
        # Get the ECTS points
        ects = value
        ects_list.append((semester, lv, ects))

    # Create a dict per semester
    ects_per_semester = {}
    for semester, lv, ects in ects_list:
        if semester not in ects_per_semester:
            ects_per_semester[semester] = {}
        ects_per_semester[semester][lv] = ects

    return ects_per_semester
