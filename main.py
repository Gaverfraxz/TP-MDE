import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

student_id = 2
data_folder = "data/V1"

with open("data/roles.json") as f:
    roles = json.load(f)
with open(os.path.join(data_folder, f"projects.json")) as f:
    projects = json.load(f)
with open(os.path.join(data_folder, f"tracking.json")) as f:
    tracking = json.load(f)

student_tracking_data = next(filter(
    lambda t: t["ID"] == student_id, tracking
))
student_project = next(filter(
    lambda p: p["Id Proyecto"] == student_tracking_data["# Proyecto"], projects
))
student_role = roles[student_tracking_data["Rol"]]
if student_tracking_data["Rol"] == "Fullstack":
    student_role += " " + roles["Frontend"] + " " + roles["Backend"]



agent_role = "Sos un docente de proyecto para estudiantes de secundario de 15 a 16 años."
prompt = f"Rol del estudiante: {student_tracking_data['Rol']} {student_role} - Anteproyecto: {student_project} - Tareas asignadas hasta ahora: {student_tracking_data}. Sugerir la siguiente tarea para el estudiante siguiendo el contexto."

response = client.responses.create(
    model="gpt-5",
    instructions=agent_role,
    input=prompt,

)

print(response.output_text)