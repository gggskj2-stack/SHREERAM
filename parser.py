def parse_courses(file_path):
    courses = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Format: title|description|type|path
                    parts = line.split('|')
                    if len(parts) == 4:
                        courses.append({
                            'title': parts[0].strip(),
                            'description': parts[1].strip(),
                            'type': parts[2].strip(),
                            'path': parts[3].strip()
                        })
    except FileNotFoundError:
        raise Exception("courses.txt file not found")
    return courses
