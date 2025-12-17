"""
Request models for API endpoints
"""

from typing import List
from pydantic import BaseModel, Field, field_validator


class CustomerData(BaseModel):
    """Input data for customer churn prediction"""

    gender: str = Field(..., description="Customer gender (Male/Female)")
    SeniorCitizen: int = Field(
        ..., description="Whether customer is senior citizen (0/1)"
    )
    Partner: str = Field(..., description="Whether customer has partner (Yes/No)")
    Dependents: str = Field(..., description="Whether customer has dependents (Yes/No)")
    tenure: int = Field(..., description="Number of months customer has stayed", ge=0)
    PhoneService: str = Field(
        ..., description="Whether customer has phone service (Yes/No)"
    )
    MultipleLines: str = Field(
        ..., description="Whether customer has multiple lines (Yes/No/No phone service)"
    )
    InternetService: str = Field(
        ..., description="Customer's internet service provider (DSL/Fiber optic/No)"
    )
    OnlineSecurity: str = Field(
        ...,
        description="Whether customer has online security (Yes/No/No internet service)",
    )
    OnlineBackup: str = Field(
        ...,
        description="Whether customer has online backup (Yes/No/No internet service)",
    )
    DeviceProtection: str = Field(
        ...,
        description="Whether customer has device protection (Yes/No/No internet service)",
    )
    TechSupport: str = Field(
        ...,
        description="Whether customer has tech support (Yes/No/No internet service)",
    )
    StreamingTV: str = Field(
        ...,
        description="Whether customer has streaming TV (Yes/No/No internet service)",
    )
    StreamingMovies: str = Field(
        ...,
        description="Whether customer has streaming movies (Yes/No/No internet service)",
    )
    Contract: str = Field(
        ..., description="Contract term (Month-to-month/One year/Two year)"
    )
    PaperlessBilling: str = Field(
        ..., description="Whether customer has paperless billing (Yes/No)"
    )
    PaymentMethod: str = Field(
        ...,
        description="Payment method (Electronic check/Mailed check/Bank transfer (automatic)/Credit card (automatic))",
    )
    MonthlyCharges: float = Field(..., description="Monthly charges amount", ge=0)
    TotalCharges: float = Field(..., description="Total charges amount", ge=0)

    @field_validator('gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', mode='before')
    @classmethod
    def strip_strings(cls, v):
        """Strip whitespace from string fields"""
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator('MonthlyCharges', 'TotalCharges', mode='before')
    @classmethod
    def parse_charges(cls, v):
        """Convert empty/whitespace strings to 0.0"""
        if isinstance(v, str):
            v = v.strip()
            if v == '':
                return 0.0
            try:
                return float(v)
            except ValueError:
                raise ValueError(f"Invalid float value: {v}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Male",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 12,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "Yes",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 85.50,
                "TotalCharges": 1026.00,
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request model for batch prediction"""

    customers: List[CustomerData]
