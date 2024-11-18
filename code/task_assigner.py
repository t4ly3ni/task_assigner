import openai
import json
import os
from employees import employees

# Set your OpenAI API key using an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_task():
    # Task template integrated directly into the code
    task = {
        "task_name": "Implement Feature X",
        "task_description": "Develop and integrate Feature X into the existing system. The feature should allow users to do Y and Z.",
        "required_skills": ["Python", "REST API"],
        "additional_notes": "Please ensure the feature is scalable and includes unit tests."
    }
    return task

def generate_prompt(task, employees):
    employee_info = "\n".join([
        f"{emp['id']}: {emp['name']}, Skills: {', '.join(emp['skills'])}, Available: {emp['availability']}"
        for emp in employees if emp['availability']
    ])
    prompt = f"""
You are an AI assistant that assigns tasks to employees based on their skills.

Task Details:
Name: {task['task_name']}
Description: {task['task_description']}
Required Skills: {', '.join(task['required_skills'])}
Additional Notes: {task['additional_notes']}

Available Employees:
{employee_info}

Assign the two best-suited employees for this task. Estimate the weight (1-10), time in hours, and provide a deadline (YYYY-MM-DD). Return the result as a JSON with the following keys: task_name, assigned_employees (list of employee ids), estimated_weight, estimated_time, deadline.
"""
    return prompt

def get_assignment(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You help assign tasks to employees based on their skills."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            temperature=0.7,
        )
        result = response['choices'][0]['message']['content']
        return result
    except Exception as e:
        print(f"An error occurred during the API call: {e}")
        return None

def main():
    task = load_task()
    prompt = generate_prompt(task, employees)
    print("Generated Prompt:")
    print(prompt)
    assignment = get_assignment(prompt)
    if assignment:
        print("Assignment Result:")
        print(assignment)

if __name__ == "__main__":
    main()