import os
from strands import Agent, tool
from strands.models import BedrockModel
from bedrock_agentcore import BedrockAgentCoreApp


MODEL_ID = "us.amazon.nova-lite-v1:0"
REGION = "us-east-1"

app = BedrockAgentCoreApp()


@tool
def lookup_course(department: str, course_number: str) -> str:
    """Look up schedule and details for a specific course.

    Use this when a student asks about a particular class,
    like "When does CS 201 meet?" or "Who teaches BIO 101?"

    Args:
        department: The department code (e.g., "CS", "BIO", "ENG").
        course_number: The course number (e.g., "101", "201").

    Returns:
        Course details including schedule, instructor, and location.
    """
    # In a real app this would query a course catalog API
    courses = {
        "CS-101": {
            "title": "Introduction to Programming",
            "instructor": "Dr. Maria Chen",
            "schedule": "Mon/Wed/Fri 10:00 - 10:50 AM",
            "location": "Turing Engineering Building, Room 210",
            "credits": 3,
            "seats_available": 12,
        },
        "CS-201": {
            "title": "Data Structures",
            "instructor": "Prof. James Park",
            "schedule": "Tue/Thu 1:00 - 2:15 PM",
            "location": "Turing Engineering Building, Room 215",
            "credits": 3,
            "seats_available": 5,
        },
        "BIO-101": {
            "title": "General Biology I",
            "instructor": "Dr. Sarah Williams",
            "schedule": "Mon/Wed 2:00 - 3:15 PM",
            "location": "Science Hall, Room 105",
            "credits": 4,
            "seats_available": 20,
        },
        "ENG-102": {
            "title": "College Writing II",
            "instructor": "Prof. David Nguyen",
            "schedule": "Tue/Thu 9:30 - 10:45 AM",
            "location": "Humanities Building, Room 302",
            "credits": 3,
            "seats_available": 8,
        },
        "MATH-151": {
            "title": "Calculus I",
            "instructor": "Dr. Lisa Patel",
            "schedule": "Mon/Wed/Fri 11:00 - 11:50 AM",
            "location": "Math & Science Center, Room 120",
            "credits": 4,
            "seats_available": 15,
        },
    }

    key = f"{department.upper()}-{course_number}"
    if key in courses:
        c = courses[key]
        return (
            f"Course: {key} — {c['title']}\n"
            f"Instructor: {c['instructor']}\n"
            f"Schedule: {c['schedule']}\n"
            f"Location: {c['location']}\n"
            f"Credits: {c['credits']}\n"
            f"Seats available: {c['seats_available']}"
        )

    return f"No course found for {key}. Check the department code and course number."



def create_university_agent():
    """
    Lookup course information based on the course code.
    """
    system_prompt = """You are the University virtual assistant.
    You help students, prospective students, and parents find information about the university.

    Your responsibilities:
    - Answer questions about academics, admissions, financial aid, housing, dining, parking, the library, career services, and the academic calendar.
    - Use the retrieve tool to search the knowledge base for university policies and FAQ answers before responding.
    - Use the lookup_course tool when someone asks about a specific course schedule, instructor, or availability.
    - Cite your sources when referencing specific policies or dates.

    Guidelines:
    - Be friendly and welcoming — remember, students may be stressed about deadlines.
    - If you don't know the answer, say so and suggest they contact the relevant office.
    - Keep answers concise and helpful."""
    print("Creating the University virtual assistant agent...")
    # create a agent with the system prompt
    model = BedrockModel(model_id=MODEL_ID, region=REGION)
    agent = Agent(model=model, system_prompt=system_prompt, tools=[lookup_course])
    # returning the agent
    print("University virtual assistant agent created successfully.")
    return agent


# main function to run the agent
@app.entrypoint
def student_query():

    # Start the agent's interaction loop
    agent = create_university_agent()
    # run agent on user input until the user types "exit"
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting the University virtual assistant. Goodbye!")
            break
        response = agent(user_input)
        print(f"Assistant: {response}")


if __name__ == "__main__":
   app.run()
   #student_query()