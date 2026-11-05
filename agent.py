
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import TOOL_SCHEMAS, execute_tool


# ==========================================
# GEMINI CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"

MAX_TOOL_ROUNDS = 5


# ==========================================
# REGISTER FUNCTION SCHEMAS
# ==========================================

function_declarations = []

for schema in TOOL_SCHEMAS:

    declaration = types.FunctionDeclaration(
        name=schema["name"],
        description=schema["description"],
        parameters_json_schema=schema["parameters"]
    )

    function_declarations.append(declaration)


gemini_tool = types.Tool(
    function_declarations=function_declarations
)


# ==========================================
# AGENT FUNCTION
# ==========================================

def run_agent(user_message, status_callback=None):

    history = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_message)
            ]
        )
    ]

    config = types.GenerateContentConfig(
        tools=[gemini_tool],
        temperature=0.2,
       system_instruction=(
    "You are a helpful AI assistant. "
    "For weather questions, use get_weather. "
    "For loan EMI calculations, use calculate_emi. "
    "Always use the actual values supplied by the user. "
    "Do not invent loan amounts, interest rates or durations. "
    "If required information is missing, ask the user for it. "
    "All financial amounts must be displayed in Pakistani Rupees (Rs.), "
    "not Indian Rupees (₹). "
    "After receiving a tool result, explain it clearly."
),
        automatic_function_calling=(
            types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    # ======================================
    # AGENTIC LOOP
    # ======================================

    for round_number in range(MAX_TOOL_ROUNDS):

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=history,
            config=config
        )

        if not response.candidates:
            return "Gemini did not return a response."

        model_content = response.candidates[0].content

        if model_content is None:
            return response.text or "No response received."

        # Find function calls requested by Gemini
        function_calls = []

        for part in model_content.parts or []:

            if part.function_call:
                function_calls.append(part.function_call)

        # No function call means Gemini has a normal answer
        if not function_calls:
            return response.text or "I could not generate an answer."

        # Save Gemini's function-call message in conversation history
        history.append(model_content)

        # Execute every requested function
        for function_call in function_calls:

            function_name = function_call.name
            arguments = dict(function_call.args or {})

            message = (
                f"Gemini requested tool: {function_name} "
                f"with arguments: {arguments}"
            )

            print("\n[TOOL CALL]")
            print(message)

            if status_callback:
                status_callback(message)

            # Execute the Python function
            result = execute_tool(
                function_name,
                arguments
            )

            print("[TOOL RESULT]")
            print(result)

            if status_callback:
                status_callback(
                    f"{function_name} completed."
                )

            # Send the raw result back to Gemini
            tool_response = types.Part.from_function_response(
                name=function_name,
                response={
                    "result": result
                }
            )

            history.append(
    types.Content(
        role="user",
        parts=[tool_response]
    )
)

    return (
        "The agent reached its maximum tool-call limit. "
        "Please try a simpler question."
    )


# ==========================================
# TERMINAL CHAT INTERFACE
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("       GEMINI AI SMART ASSISTANT")
    print("=" * 50)

    print("Ask me about weather, EMI or anything else.")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ")

        if question.lower().strip() in [
            "exit", "quit", "bye"
        ]:

            print("\nAssistant: Goodbye!")
            break

        try:

            answer = run_agent(question)

            print("\nAssistant:")
            print(answer)

        except Exception as error:

            print("\nError:", str(error))
