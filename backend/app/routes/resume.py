from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import os

from app.services.resume_parser import extract_text_from_pdf

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

# Upload folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Skills that we can detect
SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "react",
    "sql",
    "git",
    "data structures",
    "mongodb",
    "mysql",
    "c++",
    "c",
    "node.js",
    "express.js"
]


# Skills required for different job roles
ROLE_SKILLS = {
    "software developer": [
        "python",
        "java",
        "javascript",
        "sql",
        "git",
        "data structures"
    ],

    "web developer": [
        "html",
        "css",
        "javascript",
        "react",
        "sql",
        "git"
    ],

    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git"
    ],

    "backend developer": [
        "python",
        "java",
        "sql",
        "git",
        "node.js",
        "express.js"
    ],

    "full stack developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "sql",
        "git"
    ]
}


def detect_skills(resume_text):
    """
    Detect technical skills from extracted resume text.
    """

    text = resume_text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_score(found_skills):
    """
    Calculate resume score based on detected skills.
    """

    if not found_skills:
        return 0

    # Maximum score based on 10 important skills
    important_skills = [
        "python",
        "java",
        "javascript",
        "html",
        "css",
        "react",
        "sql",
        "git",
        "data structures",
        "mysql"
    ]

    matched = 0

    for skill in important_skills:
        if skill in found_skills:
            matched += 1

    score = int((matched / len(important_skills)) * 100)

    return score


def get_strengths(found_skills):
    """
    Generate strengths based on detected skills.
    """

    strengths = []

    if len(found_skills) >= 5:
        strengths.append(
            "Good technical skill coverage."
        )

    if "python" in found_skills:
        strengths.append(
            "Python knowledge is useful for software development and AI-related projects."
        )

    if "java" in found_skills:
        strengths.append(
            "Java knowledge provides a strong foundation for application development."
        )

    if "javascript" in found_skills:
        strengths.append(
            "JavaScript knowledge is useful for building interactive web applications."
        )

    if "react" in found_skills:
        strengths.append(
            "React experience is valuable for modern frontend development."
        )

    if "git" in found_skills:
        strengths.append(
            "Git knowledge demonstrates familiarity with version control."
        )

    if not strengths:
        strengths.append(
            "Resume text was successfully extracted and analyzed."
        )

    return strengths


def get_suggestions(found_skills, missing_skills):
    """
    Generate suggestions for improving the resume.
    """

    suggestions = []

    if "data structures" not in found_skills:
        suggestions.append(
            "Add Data Structures and Algorithms skills if you have learned them."
        )

    if "git" not in found_skills:
        suggestions.append(
            "Add Git/GitHub experience and include project links."
        )

    if len(found_skills) < 5:
        suggestions.append(
            "Add more relevant technical skills to match your target role."
        )

    suggestions.append(
        "Add measurable achievements to your projects."
    )

    suggestions.append(
        "Include GitHub links for your important projects."
    )

    suggestions.append(
        "Keep the resume concise and preferably one page."
    )

    return suggestions


def calculate_job_match(job_role, found_skills):
    """
    Calculate how well the resume matches the selected job role.
    """

    role = job_role.lower().strip()

    # Default role
    if role not in ROLE_SKILLS:
        role = "software developer"

    required_skills = ROLE_SKILLS[role]

    matching_skills = [
        skill for skill in required_skills
        if skill in found_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    if len(required_skills) > 0:
        match_percentage = int(
            (len(matching_skills) / len(required_skills)) * 100
        )
    else:
        match_percentage = 0

    return {
        "match_percentage": match_percentage,
        "matching_skills": matching_skills,
        "skills_to_learn": missing_skills
    }


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_role: str = Form("Software Developer")
):
    """
    Upload PDF resume, extract text and analyze the resume.
    """

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a resume file."
        )

    # Only PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Save file
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    try:

        # Read uploaded file
        file_content = await file.read()

        # Save PDF
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Extract text
        resume_text = extract_text_from_pdf(file_path)

        # Check extracted text
        if not resume_text or not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF. Please upload a text-based PDF."
            )

        # Detect skills
        skills_found = detect_skills(resume_text)

        # Calculate overall resume score
        score = calculate_score(skills_found)

        # Calculate role match
        job_match = calculate_job_match(
            job_role,
            skills_found
        )

        # Strengths
        strengths = get_strengths(
            skills_found
        )

        # Suggestions
        suggestions = get_suggestions(
            skills_found,
            job_match["skills_to_learn"]
        )

        # Return complete analysis
        return {
            "message": "Resume analyzed successfully",

            "filename": file.filename,

            "resume_text": resume_text[:5000],

            "score": score,

            "skills_found": skills_found,

            "missing_skills": job_match["skills_to_learn"],

            "strengths": strengths,

            "suggestions": suggestions,

            "job_role": job_role,

            "job_role_match": job_match["match_percentage"],

            "matching_skills": job_match["matching_skills"],

            "skills_to_learn": job_match["skills_to_learn"]
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Resume analysis error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing resume: {str(e)}"
        )