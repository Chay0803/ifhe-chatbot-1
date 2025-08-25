

def match_courses(candidate):
    stream = candidate.get("stream", "").lower()
    interest = candidate.get("interest", "").lower()
    english = candidate.get("english", "").lower()

    courses = []

    if english not in ["yes", "good", "fluent"]:
        return ["English proficiency is mandatory. Please improve English skills."]

    if "science" in stream:
        if "tech" in interest or "computer" in interest:
            courses += [
            "B.Tech CSE Artificial Intelligence",
            "B.Tech CSE Artificial Intelligence & Data Science",
            "B.Tech CSE Artificial Intelligence & Machine Learning",
            "B.Tech Computer Science Engineering",
            "B.Tech Electronics & Communication Engineering",
            "B.Tech Mechanical Engineering"
            ]
        if "management" in interest:
            courses += ["BBA", "BBA (AI & Data Science)", "BBA (Cloud & Cyber Security)"]

    elif "commerce" in stream:
        if "management" in interest:
            courses += ["BBA", "BBA (AI & Data Science)", "BBA (Cloud & Cyber Security)"]
        if "law" in interest:
            courses += ["BBA-LLB (Hons.)"]

    elif "arts" in stream:
        if "law" in interest:
            courses += ["BA-LLB (Hons.)", "BAJ-LLB (Hons.)"]
        if "economics" in interest:
            courses += ["BA (Economics)"]

    if not courses:
        courses.append("No direct matches found. Consider general programs like BBA or BCA.")

    return courses



