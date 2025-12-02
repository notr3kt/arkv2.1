"""Core JobDiva client for S1NGULARITY.

Wraps key JobDiva endpoints with token management, duplication checks, and
Pydantic request models to ensure correct casing.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from jobdiva_auth import JobDivaAuth, get_auth


class SearchCandidateRequest(BaseModel):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    maxreturned: Optional[int] = None
    offset: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class CreateCandidateRequest(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str
    cellphone: Optional[str] = None
    homephone: Optional[str] = None
    workphone: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    countryid: Optional[str] = None
    currentsalary: Optional[float] = None
    currentsalaryunit: Optional[str] = None
    preferredsalary: Optional[float] = None
    preferredsalaryunit: Optional[str] = None
    narrative: Optional[str] = None
    resumeSource: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class UploadResumeRequest(BaseModel):
    file: str
    fileName: str
    resumeSource: str
    parseResume: bool = True


class SearchJobRequest(BaseModel):
    title: Optional[str] = None
    companyName: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    maxreturned: Optional[int] = None


class CreateCandidateNoteRequest(BaseModel):
    candidateId: int
    note: str
    noteType: Optional[str] = None
    pinned: Optional[bool] = None


class JobDivaClient:
    """Wrapper around JobDiva endpoints with auth and retry support."""

    def __init__(self, auth: Optional[JobDivaAuth] = None) -> None:
        self.auth = auth or get_auth()
        self.base_url = os.getenv("JOBDIVA_BASE_URL", "https://api.jobdiva.com")
        self.session = requests.Session()

    def _request(self, method: str, path: str, *, json: Optional[dict] = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = self.auth.authorized_headers()
        response = self.session.request(method, url, headers=headers, json=json, timeout=30)
        if response.status_code == 401:
            # refresh and retry once
            self.auth.get_token(force_refresh=True)
            headers = self.auth.authorized_headers()
            response = self.session.request(method, url, headers=headers, json=json, timeout=30)
        response.raise_for_status()
        return response

    def search_candidate_profile(self, payload: SearchCandidateRequest) -> List[Dict[str, Any]]:
        data = payload.model_dump(by_alias=True, exclude_none=True)
        response = self._request("POST", "/apiv2/jobdiva/searchCandidateProfile", json=data)
        try:
            return response.json()
        except ValueError:
            return []

    def create_candidate(self, payload: CreateCandidateRequest) -> int:
        existing = []
        if payload.email:
            search_payload = SearchCandidateRequest(email=payload.email)
            existing = self.search_candidate_profile(search_payload)
        if existing:
            candidate_id = existing[0].get("candidateId") or existing[0].get("candidateid")
            if candidate_id is not None:
                return int(candidate_id)

        data = payload.model_dump(by_alias=True, exclude_none=True)
        response = self._request("POST", "/apiv2/jobdiva/createCandidate", json=data)
        body = response.json()
        candidate_id = body.get("candidateID") or body.get("candidateId") or body.get("id")
        if candidate_id is None:
            raise ValueError("createCandidate response missing candidate ID")
        return int(candidate_id)

    def upload_resume(self, payload: UploadResumeRequest) -> dict:
        data = payload.model_dump(exclude_none=True)
        response = self._request("POST", "/apiv2/jobdiva/uploadResume", json=data)
        return response.json()

    def search_job(self, payload: SearchJobRequest) -> List[Dict[str, Any]]:
        data = payload.model_dump(exclude_none=True)
        response = self._request("POST", "/apiv2/jobdiva/SearchJob", json=data)
        return response.json()

    def create_candidate_note(self, payload: CreateCandidateNoteRequest) -> dict:
        data = payload.model_dump(exclude_none=True)
        response = self._request("POST", "/apiv2/jobdiva/createCandidateNote", json=data)
        return response.json()


__all__ = [
    "JobDivaClient",
    "CreateCandidateNoteRequest",
    "CreateCandidateRequest",
    "SearchCandidateRequest",
    "SearchJobRequest",
    "UploadResumeRequest",
]
