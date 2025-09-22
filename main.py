import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
agent_role = "Sos un docente de proyecto para estudiantes de secundario de 15 a 16 años."
prompt = "Decir hola"


response = client.responses.create(
    model="gpt-5",
    instructions=agent_role,
    input=prompt,
)

print(response.output_text)