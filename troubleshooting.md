# Week 5 – Troubleshooting Log
## AI Agents & Tool Use – GenAI Smart Assistant

**Project:** GenAI Smart Assistant  
**Internship:** GenAI Engineering – Uzair AI Studio  
**Week:** 5  
**Date:** November 2026

---

## 1. Gemini API Model Availability Error

**Problem:**

The application initially returned a 503 error while using the `gemini-3.8-flash` model.

**Cause:**

The selected model was unavailable or temporarily overloaded.

**Solution:**

Tested another model using a separate Python script and changed the model name in `agent.py` to:

```python
MODEL_NAME = "gemini-3.6-flash"
```

**Result:** Gemini API successfully generated responses.

---

## 2. Function Calling Role Error

**Problem:**

The application returned the following error:

```text
400 INVALID_ARGUMENT
Role 'tool' not supported
```

**Cause:**

The Gemini API rejected the `tool` role used in the conversation history.

**Solution:**

Changed the role to `user` when appending the function response:

```python
history.append(
    types.Content(
        role="user",
        parts=[tool_response]
    )
)
```

**Result:** Function responses were successfully sent back to Gemini.

---

## 3. Function Calling and Tool Schema Integration

**Problem:**

The AI agent needed to identify the correct Python function and provide its required arguments.

**Cause:**

Function calling requires correctly defined function names, descriptions, parameter types, and argument structures.

**Solution:**

Created JSON schemas in `tools.py` for:

- `get_weather(city)`
- `calculate_emi(principal, annual_interest_rate, months)`

Registered these schemas with Gemini using `types.FunctionDeclaration`.

**Result:** Gemini successfully identified the correct tool and supplied the required arguments.

---

## 4. Tool Execution and Agentic Loop

**Problem:**

The agent needed to execute Python functions and return their results to Gemini instead of generating calculations or weather information independently.

**Solution:**

Implemented an agentic loop in `agent.py` that:

1. Sends the user's question to Gemini.
2. Detects function-call requests.
3. Extracts the function name and arguments.
4. Executes the requested Python function.
5. Sends the raw result back to Gemini.
6. Generates a final natural-language response.

Added a maximum of five tool-call rounds to prevent endless execution.

```python
MAX_TOOL_ROUNDS = 5
```

**Result:** The agent successfully executed both weather and EMI tools.

---

## 5. Currency Formatting Issue

**Problem:**

Gemini initially displayed EMI amounts using the Indian Rupee symbol instead of the Pakistani Rupee format.

**Solution:**

Added an instruction to the system prompt:

```python
"All financial amounts must be displayed in Pakistani Rupees (Rs.), "
"not Indian Rupees (₹). "
```

**Result:** Financial amounts were displayed in Pakistani Rupees.

---

## 6. Streamlit Integration

**Problem:**

The Python agent needed to be integrated into a user-friendly web interface with visible tool activity.

**Solution:**

Updated `app.py` to:

- Integrate `run_agent()` with Streamlit.
- Maintain conversation history using `st.session_state`.
- Display a thinking indicator.
- Display tool-call status messages through `status_callback`.
- Display the final AI response.
- Provide a Clear Chat button.

**Result:** The Streamlit application successfully displayed weather reports, EMI calculations, and normal conversational responses.

---

## 7. Final Testing Results

| Test Case | Expected Result | Status |
|---|---|---|
| Weather in Mardan | Current weather information | Passed |
| EMI for Rs. 800,000 at 15% for 36 months | Correct EMI calculation | Passed |
| Normal conversation | Natural-language response | Passed |
| Pakistani currency formatting | Amounts displayed in Rs. | Passed |
| Conversation interface | Messages displayed in chat | Passed |

### EMI Test Output

- Loan Amount: Rs. 800,000
- Annual Interest Rate: 15%
- Loan Duration: 36 months
- Monthly EMI: Rs. 27,732.26
- Total Interest: Rs. 198,361.46
- Total Payment: Rs. 998,361.46

---

## Conclusion

During Week 5, a GenAI Smart Assistant was developed using Gemini function calling and Python tools. The assistant can retrieve weather information through a public API and calculate loan EMIs using a mathematical formula.

An agentic loop was implemented to allow Gemini to select and execute the appropriate Python functions. The tools were integrated into a Streamlit interface with conversation history and tool-use status indicators.

The application successfully passed the local functional tests for weather information, EMI calculations, and normal conversation.