
from tools import get_weather, calculate_emi

print("\n===== EMI CALCULATOR TEST =====")

emi_result = calculate_emi(
    principal=500000,
    annual_interest_rate=12,
    months=24
)

print(emi_result)

print("\n===== WEATHER TOOL TEST =====")

weather_result = get_weather("Islamabad")

print(weather_result)
