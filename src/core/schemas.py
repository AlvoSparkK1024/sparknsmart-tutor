from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Appliance(BaseModel):
    name: str
    power_watts: float
    daily_usage_hours: float
    power_factor: float = 1.0
    harmonics_thd: float = 0.0

class Tariff(BaseModel):
    region: str
    currency: str
    tiers: List[Dict[str, float]]  # e.g., [{"limit": 100, "rate": 5.0}, {"limit": 200, "rate": 7.0}]

class AnalysisResult(BaseModel):
    appliance_name: str
    monthly_kwh: float
    monthly_cost: float
    pf_penalty: float = 0.0
    suggestions: List[str] = []

class Lesson(BaseModel):
    topic: str
    content: str
    chart_path: Optional[str] = None
    actions: List[str] = []
    estimated_savings: str

class Message(BaseModel):
    content: str
    image_path: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
