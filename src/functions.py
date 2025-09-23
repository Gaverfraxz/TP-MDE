import os
import json

tools = [
    {
        "type": "function",
        "name": "get_student_tracking_data",
        "description": "Get tracking data for a specific student.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "The ID of the student to retrieve tracking data for."
                }
            },
            "required": ["student_id"],
        },
    },
    {
        "type": "function",
        "name": "get_role_description",
        "description": "Get the description of a specific role.",
        "parameters": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "description": "The role to retrieve the description for."
                }
            },
            "required": ["role"],
        },
    },
    {
        "type": "function",
        "name": "get_student_project",
        "description": "Get project data for a specific project ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "The ID of the project to retrieve data for."
                }
            },
            "required": ["project_id"],
        },
    },
]


def get_student_tracking_data(student_id: str, data_folder: str) -> dict:
    with open(os.path.join(data_folder, f"tracking.json")) as f:
        tracking = json.load(f)
    try:
        student_id = int(student_id)
        student_tracking_data = next(filter(
            lambda t: t["ID"] == student_id, tracking
        ))
    except (ValueError, StopIteration):
        student_tracking_data = {}
    return student_tracking_data

def get_role_description(role: str) -> str:
    with open("data/roles.json") as f:
        roles = json.load(f)
    role_description = roles[role]
    if role == "Fullstack":
        role_description += " " + roles["Frontend"] + " " + roles["Backend"]
    return role_description


def get_student_project(project_id: str, data_folder: str) -> dict:
    with open(os.path.join(data_folder, f"projects.json")) as f:
        projects = json.load(f)
    try:
        project_id = int(project_id)
        student_project = next(filter(
            lambda p: p["Id Proyecto"] == project_id, projects
        ))
    except (ValueError, StopIteration):
        student_project = {}
    return student_project