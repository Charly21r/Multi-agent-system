### Multi-Agent System with OpenAI Agents SDK

This project demonstrates how to build a simple **multi-agent system** using the OpenAI Agents SDK. The assistant helps users plan their travels by:
- Checking for flights.
- Checking the weather for a destination.
- Generating a personalized tourist plan based on current conditions.

This project is designed to be small, modular, and educational — perfect for learning how to implement collaborating AI agents with tools.

---

## 🧠 Architecture Overview

The system includes:

### Agents
- **Weather Agent**: Uses a custom tool to fetch weather information for a destination.
- **Flight Agent**: Uses a custom tool to fetch flight information for a destination on a given date.
- **Planning Agent**: Creates a custom itinerary based on weather, location, and preferences.

### Tools
- **WeatherTool**: Queries the OpenWeatherMap API to retrieve real-time weather data.
- **FlightTool**: Queries Amadeus API to retrieve real-time flights data.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-agent-travel-assistant.git
cd multi-agent-travel-assistant
streamlit run src/main.py