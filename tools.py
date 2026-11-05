
import requests


# ==========================================
# TOOL 1: WEATHER
# ==========================================

def get_weather(city: str):

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=15
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {"error": f"City '{city}' not found."}

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "precipitation,"
                    "wind_speed_10m"
                )
            },
            timeout=15
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        return {
            "city": location["name"],
            "country": location.get("country", "Unknown"),
            "current_weather": weather_data["current"]
        }

    except requests.RequestException as error:
        return {"error": f"Weather API error: {error}"}

    except (KeyError, IndexError) as error:
        return {"error": f"Weather data error: {error}"}


# ==========================================
# TOOL 2: EMI CALCULATOR
# ==========================================

def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    months: int
):

    principal = float(principal)
    annual_interest_rate = float(annual_interest_rate)
    months = int(months)

    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if months <= 0:
        raise ValueError("Duration must be greater than zero.")

    monthly_rate = annual_interest_rate / 12 / 100

    if monthly_rate == 0:
        emi = principal / months

    else:
        emi = (
            principal * monthly_rate * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "loan_amount": principal,
        "annual_interest_rate": annual_interest_rate,
        "duration_months": months,
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }


# ==========================================
# JSON SCHEMAS FOR GEMINI
# ==========================================

TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get live weather information for a city.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "city": {
                    "type": "STRING",
                    "description": "Name of the city."
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate_emi",
        "description": "Calculate monthly EMI, total payment and total interest for a loan.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "principal": {
                    "type": "NUMBER",
                    "description": "Total loan amount."
                },
                "annual_interest_rate": {
                    "type": "NUMBER",
                    "description": "Annual interest rate in percentage."
                },
                "months": {
                    "type": "INTEGER",
                    "description": "Loan duration in months."
                }
            },
            "required": [
                "principal",
                "annual_interest_rate",
                "months"
            ]
        }
    }
]


# ==========================================
# TOOL EXECUTION FUNCTION
# ==========================================

def execute_tool(function_name, arguments):

    try:

        if function_name == "get_weather":
            return get_weather(**arguments)

        elif function_name == "calculate_emi":
            return calculate_emi(**arguments)

        else:
            return {"error": f"Unknown tool: {function_name}"}

    except (TypeError, ValueError) as error:
        return {"error": str(error)}

    except Exception as error:
        return {"error": f"Tool execution failed: {error}"}
