import os
from openai import OpenAI
from dotenv import load_dotenv
from src.functions import tools, get_student_tracking_data, get_role_description, get_student_project
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

student_id = 2
data_folder = "data/V1"

# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": f"Sugerir la siguiente tarea semanal para el estudiante con ID {student_id}"}
]

# 2. Prompt the model with tools defined
response = client.responses.create(
    model="gpt-5",
    tools=tools,
    input=input_list,
)

# Allow the model to call functions at max 2 times
amount_of_function_calls = 2
input_list += response.output
while amount_of_function_calls > 0 and any(item.type == "function_call" for item in response.output):
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_student_tracking_data":
                # 3. Execute the function logic for get_student_tracking_data
                student_tracking_data = get_student_tracking_data(json.loads(item.arguments)["student_id"], data_folder)
                
                # 4. Provide function call results to the model
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(student_tracking_data)
                })
            elif item.name == "get_role_description":
                # 3. Execute the function logic for get_role_description
                role_description = get_role_description(json.loads(item.arguments)["role"])
                
                # 4. Provide function call results to the model
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                      "description": role_description
                    })
                })
            elif item.name == "get_student_project":
                # 3. Execute the function logic for get_student_project
                student_project = get_student_project(json.loads(item.arguments)["project_id"], data_folder)
                
                # 4. Provide function call results to the model
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(student_project)
                })
    response = client.responses.create(
        model="gpt-5",
        tools=tools,
        input=input_list,
    )
    input_list += response.output
    amount_of_function_calls -= 1


print("Final input:")
print(input_list)

agent_role = "Sos un docente de proyecto para estudiantes de secundario de 15 a 16 años."

response = client.responses.create(
    model="gpt-5",
    instructions=agent_role,
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
print("Final output:")
print(response.model_dump_json(indent=2))
print("\n" + response.output_text)
