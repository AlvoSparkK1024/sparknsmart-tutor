# SPARKnSMART (SNS) - Appliance-Level Energy Tutor

## Project Overview
A messaging-first, multi-agent tutor that teaches appliance-level energy concepts and actionable savings. Built with Google Antigravity and the Agent Development Kit (ADK).

## Tracks
- **Primary**: Agents for Good
- **Secondary**: Concierge

## Architecture
The system uses a multi-agent architecture with the following agents:
- **AdvisorAgent**: Generates educational content using Gemini.
- **AnalyzerAgent**: Analyzes appliance data for cost and power factor issues.
- **ReporterAgent**: Creates visual charts of energy usage.
- **NotifierAgent**: Formats and sends messages via Matrix.
- **SessionAgent**: Manages user session state.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd energy_tutor
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file with the following:
    ```env
    GEMINI_API_KEY=your_gemini_key
    MATRIX_USER=@your_user:matrix.org
    MATRIX_PASSWORD=your_password
    MATRIX_ROOM_ID=!your_room_id:matrix.org
    ```

4.  **Run the Demo**:
    ```bash
    python demo_push.py
    ```

## Evaluation
The system includes offline scenarios to verify functionality.
- **Scenarios**: `src/data/samples/` contains `appliances.json` and `tariff_telangana.json`.
- **Metrics**: Latency, bill estimates, and action counts are logged.

## Deployment
Build and run with Docker:
```bash
docker build -t energy-tutor .
docker run --env-file .env energy-tutor
```
