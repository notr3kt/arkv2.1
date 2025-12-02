"""OpenAI function/tool schemas for JobDiva integration."""

from __future__ import annotations

TOOLS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "search_jobdiva_candidates",
            "description": "Search JobDiva candidates by filters such as name, email, city, state, and pagination controls.",
            "parameters": {
                "type": "object",
                "properties": {
                    "firstName": {"type": "string", "description": "Candidate first name (partial match supported)"},
                    "lastName": {"type": "string", "description": "Candidate last name (partial match supported)"},
                    "email": {"type": "string", "description": "Candidate email address for exact match"},
                    "phone": {"type": "string", "description": "Phone number"},
                    "city": {"type": "string", "description": "City filter"},
                    "state": {"type": "string", "description": "State filter (2-letter code)"},
                    "zipCode": {"type": "string", "description": "ZIP/postal code filter"},
                    "maxreturned": {"type": "integer", "description": "Maximum results to return"},
                    "offset": {"type": "integer", "description": "Pagination offset"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_jobdiva_candidate",
            "description": "Create a JobDiva candidate after checking for existing profiles by email to avoid duplicates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "firstName": {"type": "string", "description": "Candidate first name"},
                    "lastName": {"type": "string", "description": "Candidate last name"},
                    "email": {"type": "string", "description": "Unique candidate email"},
                    "cellphone": {"type": "string", "description": "Mobile phone"},
                    "homephone": {"type": "string", "description": "Home phone"},
                    "workphone": {"type": "string", "description": "Work phone"},
                    "address1": {"type": "string", "description": "Street address line 1"},
                    "address2": {"type": "string", "description": "Street address line 2"},
                    "city": {"type": "string", "description": "City"},
                    "state": {"type": "string", "description": "State code"},
                    "zipCode": {"type": "string", "description": "ZIP/postal code"},
                    "countryid": {"type": "string", "description": "Country identifier"},
                    "currentsalary": {"type": "number", "description": "Current salary"},
                    "currentsalaryunit": {"type": "string", "description": "Salary unit"},
                    "preferredsalary": {"type": "number", "description": "Preferred salary"},
                    "preferredsalaryunit": {"type": "string", "description": "Preferred salary unit"},
                    "narrative": {"type": "string", "description": "Candidate summary"},
                    "resumeSource": {"type": "string", "description": "Source of the resume/candidate"},
                },
                "required": ["firstName", "lastName", "email"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "parse_resume_to_jobdiva",
            "description": "Upload and parse a resume into JobDiva. Provide base64 file content, filename, and resumeSource.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Base64-encoded resume content"},
                    "fileName": {"type": "string", "description": "Filename with extension"},
                    "resumeSource": {"type": "string", "description": "Source of the resume"},
                    "parseResume": {"type": "boolean", "description": "Parse the resume after upload (default true)"},
                },
                "required": ["file", "fileName", "resumeSource"],
            },
        },
    },
]

__all__ = ["TOOLS_CONFIG"]
