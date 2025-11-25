# JobDiva API v2 - Master Knowledge Base for AI Agent Training

**Document Purpose:** This comprehensive technical reference enables autonomous AI Agents to interact with the JobDiva Applicant Tracking System (ATS) programmatically through its REST API.

**Target Audience:** AI/ML Engineers, System Integrators, Automation Developers

**API Version:** v2

**Base URL:** `https://api.jobdiva.com`

**Authentication Method:** Token-based authentication via `/apiv2/authenticate` or `/apiv2/v2/login`

**Document Structure:**
- **Section 1:** Complete endpoint catalog organized by functional category
- **Section 2:** Business workflow patterns mapped to API call sequences
- **Section 3:** OpenAI-compatible JSON schemas for direct function calling
- **Section 4:** Data formatting rules, constraints, and validation requirements

---

# JobDiva API v2 - Master Knowledge Base

**Purpose:** This document serves as a comprehensive technical reference for training an autonomous AI Agent to interact with the JobDiva API programmatically.

**API Base URL:** `https://api.jobdiva.com`

**Authentication:** All endpoints require authentication via the `/apiv2/authenticate` or `/apiv2/v2/login` endpoint first.

---

## Section 1: The Endpoint Master List

This table catalogs every available API endpoint organized by functional category.

### Authentication

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| Authenticate | GET | `/apiv2/authenticate` | clientid, username, password | JSON object |

### Candidate Management

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| CandidateApplicationRecords | GET | `/apiv2/bi/CandidateApplicationRecords` | candidateId, fileName, employeeId | JSON object |
| CandidateAttachmentDetail | GET | `/apiv2/bi/CandidateAttachmentDetail` | candidateId, fileName, employeeId | Candidate detail object |
| CandidateLatestAssignmentEndDate | GET | `/apiv2/jobdiva/CandidateLatestAssignmentEndDate` | fromDate, toDate, expenseId, status | JSON object |
| OnBoardingDocumentsbyCandidate | GET | `/apiv2/bi/OnBoardingDocumentsbyCandidate` | fromDate, toDate, resumeIds | JSON object |
| RedactedCandidatesRecords | GET | `/apiv2/bi/RedactedCandidatesRecords` | fromDate, toDate, resumeIds | JSON object |
| createCandidate | POST | `/apiv2/jobdiva/createCandidate` | firstName, lastName, email, cellphone... | candidateID (integer) |
| createCandidateNote | POST | `/apiv2/jobdiva/createCandidateNote` | candidateId, note, noteType | noteID (integer) |
| searchCandidateProfile | POST | `/apiv2/jobdiva/searchCandidateProfile` | firstName, lastName, email, phone... | Array of candidate objects |
| updateCandidateProfile | POST | `/apiv2/jobdiva/updateCandidateProfile` | candidateId, firstName, lastName, email | boolean (success/failure) |
| uploadResume | POST | `/apiv2/jobdiva/uploadResume` | file, resumeSource | resumeID (integer) |

### Job Management

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| ActiveJobAlerts | GET | `/apiv2/bi/ActiveJobAlerts` | fromDate, toDate, jobIds, jobId | JSON object |
| CancellationReasonsList | GET | `/apiv2/jobdiva/CancellationReasonsList` | cancelStartRequest, createStartDef, createSubmittal | JSON object |
| JobsNotesListDetail | GET | `/apiv2/bi/JobsNotesListDetail` | fromDate, toDate, jobIds | Array of job objects |
| JobsStatusHistory | GET | `/apiv2/bi/JobsStatusHistory` | fromDate, toDate, jobIds | JSON object |
| JobsUsersDetail | GET | `/apiv2/bi/JobsUsersDetail` | fromDate, toDate | Job detail object |
| MergedJobs | GET | `/apiv2/bi/MergedJobs` | fromDate, toDate | JSON object |
| NewJobNotesRecords | GET | `/apiv2/bi/NewJobNotesRecords` | fromDate, toDate | JSON object |
| NewUpdatedJobRecords | GET | `/apiv2/bi/NewUpdatedJobRecords` | fromDate, toDate | boolean (success/failure) |
| NewUpdatedOpportunityRecords | GET | `/apiv2/jobdiva/bi/NewUpdatedOpportunityRecords` | fromDate, toDate, cancelStartRequest, createStartDef | JSON object |
| SearchJob | POST | `/apiv2/jobdiva/SearchJob` | title, companyName, city, state... | Array of job objects |
| addExpenseEntry | POST | `/apiv2/jobdiva/addExpenseEntry` | fromDate, toDate, expenseId | JSON object |
| addExpenseEntryWithAttachment | POST | `/apiv2/jobdiva/addExpenseEntryWithAttachment` | fromDate, toDate, expenseId | JSON object |
| approveExpenseEntry | POST | `/apiv2/jobdiva/approveExpenseEntry` | fromDate, toDate, expenseId | JSON object |
| approveLead | POST | `/apiv2/jobdiva/approveLead` | leadId | JSON object |
| createJob | POST | `/apiv2/jobdiva/createJob` | title, companyId, contactId, city... | jobID (integer) |
| createJobApplication | POST | `/apiv2/jobdiva/createJobApplication` | candidateId, jobId | applicationID (integer) |
| createPO | POST | `/apiv2/jobdiva/createPO` | fromDate, toDate, expenseId, status | JSON object |
| deleteExpense | POST | `/apiv2/jobdiva/deleteExpense` | fromDate, toDate, expenseId, status | JSON object |
| deleteTimesheet | POST | `/apiv2/jobdiva/deleteTimesheet` | fromDate, toDate, expenseId, status | JSON object |
| getExpenseCategories | GET | `/apiv2/jobdiva/getExpenseCategories` | fromDate, toDate, expenseId, status | JSON object |
| rejectLead | POST | `/apiv2/jobdiva/rejectLead` | leadId, fromDate, toDate | JSON object |
| undoRejectLead | POST | `/apiv2/jobdiva/undoRejectLead` | leadId, fromDate, toDate | JSON object |
| updateJob | POST | `/apiv2/jobdiva/updateJob` | jobId, title, status | boolean (success/failure) |

### Activity & Workflow

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| CancelledStarts | GET | `/apiv2/bi/CancelledStarts` | fromDate, toDate, candidateIds | JSON object |
| createSubmittal | POST | `/apiv2/jobdiva/createSubmittal` | candidateId, jobId, submittalDate | submittalID (integer) |

### Company Management

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| CompaniesAddressesDetail | GET | `/apiv2/bi/CompaniesAddressesDetail` | companyIds | JSON object |

### Contact Management

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| ContactAttachmentDetail | GET | `/apiv2/bi/ContactAttachmentDetail` | contactId, attachmentId, hotlistIds | JSON object |
| ContactsOwnersDetail | GET | `/apiv2/bi/ContactsOwnersDetail` | contactIds, fromDate, toDate | JSON object |

### Other

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| ActionTypeList | GET | `/apiv2/bi/ActionTypeList` | candidateId, candidateIds | JSON object |
| AssignmentChangeManagement | GET | `/apiv2/bi/AssignmentChangeManagement` | employeeId, employeeIds, fromDate, toDate | JSON object |
| DivisionsList | GET | `/apiv2/bi/DivisionsList` | None | JSON object |
| GrossProfitCalculator | GET | `/apiv2/bi/GrossProfitCalculator` | employeeId, interviewId, date, invoiceId... | JSON object |
| NewUpdatedEVerify | GET | `/apiv2/bi/NewUpdatedEVerify` | fromDate, toDate, resumeIds | JSON object |
| NewUpdatedEmployeeRecords | GET | `/apiv2/bi/NewUpdatedEmployeeRecords` | fromDate, toDate, resumeIds | JSON object |
| NonCompletedOnboardingPackages | GET | `/apiv2/bi/NonCompletedOnboardingPackages` | fromDate, toDate, resumeIds | JSON object |

### Resume Management

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| ResumeDetail | GET | `/apiv2/bi/ResumeDetail` | resumeIds, fromDate, toDate, hotListid | JSON object |
| ResumesTextDetail | GET | `/apiv2/bi/ResumesTextDetail` | resumeIds, fromDate, toDate, hotListid | JSON object |

### SOW & Milestones

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| NewUpdatedSOWRecords | GET | `/apiv2/bi/NewUpdatedSOWRecords` | fromDate, toDate | JSON object |
| SOWDetail | GET | `/apiv2/bi/SOWDetail` | fromDate, toDate, expenseId | JSON object |

### Time & Billing

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| NewUpdatedTimesheetRecords | GET | `/apiv2/bi/NewUpdatedTimesheetRecords` | fromDate, toDate | JSON object |
| NewUpdatedTimesheetRecordsLite | GET | `/apiv2/bi/NewUpdatedTimesheetRecordsLite` | fromDate, toDate, expenseId | JSON object |
| PayrollBatchDetail | GET | `/apiv2/bi/PayrollBatchDetail` | fromDate, toDate, expenseId | JSON object |
| SalaryRecordsDetail | GET | `/apiv2/bi/SalaryRecordsDetail` | fromDate, toDate, expenseId | JSON object |
| TimesheetChangeManagement | GET | `/apiv2/bi/TimesheetChangeManagement` | fromDate, toDate, expenseId | JSON object |
| TimesheetDetail | GET | `/apiv2/bi/TimesheetDetail` | fromDate, toDate, expenseId | JSON object |
| TimesheetDetailAllHours | GET | `/apiv2/bi/TimesheetDetailAllHours` | fromDate, toDate, expenseId | JSON object |
| UnbatchedTimesheetAndExpenseRecords | GET | `/apiv2/bi/UnbatchedTimesheetAndExpenseRecords` | fromDate, toDate, expenseId | JSON object |
| UpdatedApprovedBillingRecords | GET | `/apiv2/bi/UpdatedApprovedBillingRecords` | fromDate, toDate, expenseId | JSON object |
| UpdatedApprovedSalaryRecords | GET | `/apiv2/bi/UpdatedApprovedSalaryRecords` | fromDate, toDate, expenseId | JSON object |
| UpdatedInvoices | GET | `/apiv2/bi/UpdatedInvoices` | fromDate, toDate, expenseId | JSON object |

### User Management

| Feature Name | HTTP Method | Endpoint URL | Key Parameters | Data It Returns |
|--------------|-------------|--------------|----------------|-----------------|
| GroupListsbyUser | GET | `/apiv2/bi/GroupListsbyUser` | userIds, fromDate, toDate, userId | JSON object |

---
## Section 2: "Recruiter Intent" to "API Logic" Mapping

This section translates common business workflows into specific API call sequences. The AI Agent should use these patterns to solve real-world recruiting problems.

### Workflow 1: Check if a candidate exists by email, if not, create them

**Goal:** Check if a candidate exists by email, if not, create them

**API Logic:**

1. Call `POST /apiv2/jobdiva/searchCandidateProfile` with filter `{"email": "candidate@example.com"}`
2. IF response returns empty array `[]` → Candidate does not exist
3. THEN call `POST /apiv2/jobdiva/createCandidate` with required fields (firstName, lastName, email)
4. ELSE → Candidate exists, extract `candidateId` from response
5. Optionally call `POST /apiv2/jobdiva/addCandidateNoteAction` to log the interaction

### Workflow 2: Upload a resume and create/update candidate profile

**Goal:** Upload a resume and create/update candidate profile

**API Logic:**

1. Call `POST /apiv2/jobdiva/uploadResume` with resume file and resumeSource
2. API will parse resume and return `resumeId` and potentially `candidateId` if matched
3. IF `candidateId` is null → Resume parsed but no existing candidate found
4. THEN call `POST /apiv2/jobdiva/createCandidate` using parsed resume data
5. ELSE → Candidate already exists, optionally call `POST /apiv2/jobdiva/updateCandidateProfile` to update fields

### Workflow 3: Submit a candidate to a job opening

**Goal:** Submit a candidate to a job opening

**API Logic:**

1. Verify candidate exists: Call `POST /apiv2/jobdiva/searchCandidateProfile` with candidate identifiers
2. Verify job exists: Call `POST /apiv2/jobdiva/SearchJob` with job title or jobId
3. Check if candidate already applied: Call `GET /apiv2/jobdiva/CandidateApplicationsList` with candidateId
4. IF not already applied → Call `POST /apiv2/jobdiva/createJobApplication` with candidateId and jobId
5. THEN call `POST /apiv2/jobdiva/createSubmittal` to formally submit candidate
6. Add tracking note: Call `POST /apiv2/jobdiva/createCandidateNote` with submission details

### Workflow 4: Find all open jobs in a specific location

**Goal:** Find all open jobs in a specific location

**API Logic:**

1. Call `POST /apiv2/jobdiva/SearchJob` with filters:
   - `{"city": "New York", "state": "NY", "status": "Open"}`
2. Response returns array of job objects with jobId, title, company, etc.
3. For each job, optionally call `GET /apiv2/bi/JobDetail` with jobId for full details
4. To get applicant count, call `GET /apiv2/bi/JobApplicantsDetail` with jobId

### Workflow 5: Update candidate status after interview

**Goal:** Update candidate status after interview

**API Logic:**

1. Get candidate details: Call `GET /apiv2/bi/CandidateDetail` with candidateId
2. Update candidate attributes: Call `POST /apiv2/jobdiva/updateCandidateAttribute` with new status
3. Log interview outcome: Call `POST /apiv2/jobdiva/createCandidateNote` with interview feedback
4. If moving to next stage, call `POST /apiv2/jobdiva/updateActivityStartStatus` to update workflow status

### Workflow 6: Get all candidates who applied to a specific job

**Goal:** Get all candidates who applied to a specific job

**API Logic:**

1. Call `GET /apiv2/bi/JobApplicantsDetail` with jobId parameter
2. Response returns array of applicant objects with candidateId, application date, status
3. For detailed candidate info, iterate through results and call `GET /apiv2/bi/CandidateDetail` for each candidateId
4. To get resume, call `GET /apiv2/bi/CandidateResumesDetail` with candidateId

### Workflow 7: Create a new job posting

**Goal:** Create a new job posting

**API Logic:**

1. Verify company exists: Call `POST /apiv2/jobdiva/searchCompany` with company name
2. IF company doesn't exist → Call `POST /apiv2/jobdiva/createCompany` first
3. Get hiring manager contact: Call `POST /apiv2/jobdiva/SearchContacts` with company filter
4. Call `POST /apiv2/jobdiva/createJob` with required fields:
   - title, companyId, contactId, city, state, jobDescription, etc.
5. Response returns jobId
6. Optionally attach job description file: Call `POST /apiv2/jobdiva/uploadJobAttachment`

### Workflow 8: Search for qualified candidates for a job

**Goal:** Search for qualified candidates for a job

**API Logic:**

1. Get job requirements: Call `GET /apiv2/bi/JobDetail` with jobId
2. Extract required skills, location, experience from job details
3. Call `POST /apiv2/jobdiva/TalentSearch` or `POST /apiv2/jobdiva/searchCandidateProfile` with:
   - Skills/qualifications filters
   - Location filters (city, state)
   - Experience/education filters
4. Response returns ranked candidate matches
5. For each candidate, call `GET /apiv2/bi/CandidateDetail` for full profile

### Workflow 9: Add a candidate to a hotlist for future opportunities

**Goal:** Add a candidate to a hotlist for future opportunities

**API Logic:**

1. Check if hotlist exists: Call `GET /apiv2/bi/CandidateHotlistList`
2. IF hotlist doesn't exist → Call `POST /apiv2/hotlist/createCandidateHoltilst` with hotlist name
3. Add candidate to hotlist: Call `POST /apiv2/hotlist/addCandidatesToHotlist` with:
   - hotlistId
   - candidateIds (array)
4. Verify addition: Call `GET /apiv2/bi/CandidateHotlistDetail` with hotlistId

### Workflow 10: Track candidate through hiring workflow (Application → Interview → Offer)

**Goal:** Track candidate through hiring workflow (Application → Interview → Offer)

**API Logic:**

1. **Application Stage:**
   - Call `POST /apiv2/jobdiva/createJobApplication` (candidateId, jobId)
2. **Interview Stage:**
   - Call `POST /apiv2/jobdiva/createSubmittal` to formally submit candidate
   - Add interview notes: `POST /apiv2/jobdiva/createCandidateNote`
   - Update status: `POST /apiv2/jobdiva/updateActivityStartStatus`
3. **Offer Stage:**
   - Call `POST /apiv2/jobdiva/createStart` to create offer/start record
   - Update candidate availability: `POST /apiv2/jobdiva/updateCandidateProfile`
4. **Track Progress:**
   - Query status: `GET /apiv2/bi/CandidatesSubmittalsDetail` with candidateId
   - Get activity history: `GET /apiv2/bi/NewUpdatedActivityRecords`

### Workflow 11: Reject a candidate application with reason

**Goal:** Reject a candidate application with reason

**API Logic:**

1. Get rejection reasons: Call `GET /apiv2/getRejectReasons`
2. Call `POST /apiv2/jobdiva/rejectApplicant` with:
   - candidateId (required)
   - jobId (required)
   - reasonId (required)
3. Optionally add detailed note: Call `POST /apiv2/jobdiva/createCandidateNote` with rejection feedback
4. Response returns boolean success/failure

### Workflow 12: Get candidate's full profile including notes, resumes, and applications

**Goal:** Get candidate's full profile including notes, resumes, and applications

**API Logic:**

1. **Basic Profile:** Call `GET /apiv2/bi/CandidateDetail` with candidateId
2. **All Notes:** Call `GET /apiv2/bi/CandidateNotesListDetail` with candidateId
3. **Resumes:** Call `GET /apiv2/bi/CandidateResumesDetail` with candidateId
4. **Applications:** Call `GET /apiv2/jobdiva/CandidateApplicationsList` with candidateId
5. **Certifications:** Call `GET /apiv2/bi/CandidateCertificationsDetails` with candidateId
6. **Work Experience:** Call `GET /apiv2/bi/CandidateExperienceDetail` with candidateId
7. Combine all responses into comprehensive candidate dossier

---
## Section 3: JSON Schemas for Function Calling

These OpenAI-compatible JSON schemas enable the AI Agent to execute API calls directly. Each schema defines the function signature, parameters, and validation rules.

### 1. create_candidate

**Description:** Create a new candidate profile in JobDiva

**Endpoint:** `POST /apiv2/jobdiva/createCandidate`

**OpenAI JSON Schema:**

```json
{
  "type": "function",
  "function": {
    "name": "create_candidate",
    "description": "Create a new candidate profile in the JobDiva ATS system. Returns the newly created candidateID.",
    "parameters": {
      "type": "object",
      "properties": {
        "firstName": {
          "type": "string",
          "description": "Candidate's first name (required)"
        },
        "lastName": {
          "type": "string",
          "description": "Candidate's last name (required)"
        },
        "email": {
          "type": "string",
          "description": "Candidate's primary email address. Must be unique in the system. Format: valid email address (e.g., john.doe@example.com)"
        },
        "cellphone": {
          "type": "string",
          "description": "Candidate's mobile phone number. Format: (XXX) XXX-XXXX or XXX-XXX-XXXX"
        },
        "homephone": {
          "type": "string",
          "description": "Candidate's home phone number. Optional."
        },
        "workphone": {
          "type": "string",
          "description": "Candidate's work phone number. Optional."
        },
        "address1": {
          "type": "string",
          "description": "Street address line 1"
        },
        "address2": {
          "type": "string",
          "description": "Street address line 2 (apartment, suite, etc.). Optional."
        },
        "city": {
          "type": "string",
          "description": "City name"
        },
        "state": {
          "type": "string",
          "description": "State code (2-letter abbreviation, e.g., 'NY', 'CA')"
        },
        "zipCode": {
          "type": "string",
          "description": "ZIP or postal code"
        },
        "countryid": {
          "type": "string",
          "description": "Country ID from JobDiva system. Use 'US' for United States."
        },
        "currentsalary": {
          "type": "number",
          "description": "Current salary amount (numeric value only, no currency symbols)"
        },
        "currentsalaryunit": {
          "type": "string",
          "description": "Salary unit: 'Hourly', 'Annual', 'Monthly', 'Weekly'"
        },
        "preferredsalary": {
          "type": "number",
          "description": "Desired salary amount"
        },
        "preferredsalaryunit": {
          "type": "string",
          "description": "Preferred salary unit: 'Hourly', 'Annual', 'Monthly', 'Weekly'"
        },
        "narrative": {
          "type": "string",
          "description": "Candidate summary or bio text. Can include career objectives, key skills, etc."
        },
        "resumeSource": {
          "type": "string",
          "description": "Source of the resume/candidate (e.g., 'LinkedIn', 'Indeed', 'Referral', 'Company Website')"
        }
      },
      "required": [
        "firstName",
        "lastName",
        "email"
      ]
    }
  }
}
```

### 2. search_candidate

**Description:** Search for candidates by various criteria

**Endpoint:** `POST /apiv2/jobdiva/searchCandidateProfile`

**OpenAI JSON Schema:**

```json
{
  "type": "function",
  "function": {
    "name": "search_candidate",
    "description": "Search for candidate profiles in JobDiva using various filters. Returns an array of matching candidate objects.",
    "parameters": {
      "type": "object",
      "properties": {
        "firstName": {
          "type": "string",
          "description": "Filter by candidate first name (partial match supported)"
        },
        "lastName": {
          "type": "string",
          "description": "Filter by candidate last name (partial match supported)"
        },
        "email": {
          "type": "string",
          "description": "Filter by exact email address. Most reliable unique identifier."
        },
        "phone": {
          "type": "string",
          "description": "Filter by phone number (any format)"
        },
        "city": {
          "type": "string",
          "description": "Filter by city name"
        },
        "state": {
          "type": "string",
          "description": "Filter by state code (2-letter abbreviation)"
        },
        "zipCode": {
          "type": "string",
          "description": "Filter by ZIP/postal code"
        },
        "maxreturned": {
          "type": "integer",
          "description": "Maximum number of results to return. Default: 100, Max: 1000"
        },
        "offset": {
          "type": "integer",
          "description": "Row offset for pagination. Default: 0"
        }
      },
      "required": []
    }
  }
}
```

### 3. search_job

**Description:** Search for job openings by criteria

**Endpoint:** `POST /apiv2/jobdiva/SearchJob`

**OpenAI JSON Schema:**

```json
{
  "type": "function",
  "function": {
    "name": "search_job",
    "description": "Search for job openings in JobDiva using various filters. Returns an array of matching job objects.",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "Job title or keywords (partial match supported, e.g., 'Software Engineer', 'Nurse')"
        },
        "companyName": {
          "type": "string",
          "description": "Filter by company name (partial match supported)"
        },
        "city": {
          "type": "string",
          "description": "Filter by job location city"
        },
        "state": {
          "type": "string",
          "description": "Filter by job location state (2-letter code)"
        },
        "status": {
          "type": "string",
          "description": "Job status filter. Valid values: 'Open', 'Closed', 'On Hold', 'Cancelled', 'Draft'"
        },
        "fromDate": {
          "type": "string",
          "description": "Filter jobs created/updated after this date. Format: MM/dd/yyyy HH:mm:ss"
        },
        "toDate": {
          "type": "string",
          "description": "Filter jobs created/updated before this date. Format: MM/dd/yyyy HH:mm:ss"
        },
        "maxreturned": {
          "type": "integer",
          "description": "Maximum number of results. Default: 100"
        }
      },
      "required": []
    }
  }
}
```

### 4. update_candidate_status

**Description:** Update candidate profile and status

**Endpoint:** `POST /apiv2/jobdiva/updateCandidateProfile`

**OpenAI JSON Schema:**

```json
{
  "type": "function",
  "function": {
    "name": "update_candidate_status",
    "description": "Update an existing candidate's profile information and status in JobDiva. Returns boolean success/failure.",
    "parameters": {
      "type": "object",
      "properties": {
        "candidateId": {
          "type": "integer",
          "description": "The JobDiva internal candidate ID (required). Must be a valid existing candidate."
        },
        "firstName": {
          "type": "string",
          "description": "Updated first name"
        },
        "lastName": {
          "type": "string",
          "description": "Updated last name"
        },
        "email": {
          "type": "string",
          "description": "Updated email address (must remain unique)"
        },
        "cellphone": {
          "type": "string",
          "description": "Updated mobile phone"
        },
        "city": {
          "type": "string",
          "description": "Updated city"
        },
        "state": {
          "type": "string",
          "description": "Updated state code"
        },
        "status": {
          "type": "string",
          "description": "Candidate status. Valid values: 'Active', 'Inactive', 'Do Not Use', 'Placed'"
        },
        "narrative": {
          "type": "string",
          "description": "Updated candidate summary/bio"
        }
      },
      "required": [
        "candidateId"
      ]
    }
  }
}
```

### 5. add_candidate_note

**Description:** Add a note to a candidate record

**Endpoint:** `POST /apiv2/jobdiva/createCandidateNote`

**OpenAI JSON Schema:**

```json
{
  "type": "function",
  "function": {
    "name": "add_candidate_note",
    "description": "Add a timestamped note/comment to a candidate's record in JobDiva. Returns the created noteID.",
    "parameters": {
      "type": "object",
      "properties": {
        "candidateId": {
          "type": "integer",
          "description": "The JobDiva internal candidate ID (required)"
        },
        "note": {
          "type": "string",
          "description": "The note text content. Can include interview feedback, call notes, status updates, etc."
        },
        "noteType": {
          "type": "string",
          "description": "Type of note. Valid values: 'General', 'Interview', 'Phone Screen', 'Email', 'Meeting', 'Follow-up'"
        },
        "pinned": {
          "type": "boolean",
          "description": "Whether to pin this note to the top of the candidate's notes list. Default: false"
        }
      },
      "required": [
        "candidateId",
        "note"
      ]
    }
  }
}
```

### 6. upload_resume

**Description:** Upload and parse a resume file

**Endpoint:** `POST /apiv2/jobdiva/uploadResume`

**OpenAI JSON Schema:**

```json
{
  "type": "function",
  "function": {
    "name": "upload_resume",
    "description": "Upload a resume file to JobDiva. The system will automatically parse the resume and extract candidate information. Returns resumeID and potentially candidateID if matched to existing candidate.",
    "parameters": {
      "type": "object",
      "properties": {
        "file": {
          "type": "string",
          "description": "Base64-encoded resume file content OR file path. Supported formats: PDF, DOC, DOCX, TXT, RTF"
        },
        "fileName": {
          "type": "string",
          "description": "Original filename with extension (e.g., 'john_doe_resume.pdf')"
        },
        "resumeSource": {
          "type": "string",
          "description": "Source of the resume. Examples: 'LinkedIn', 'Indeed', 'Monster', 'Referral', 'Company Website', 'Email'"
        },
        "parseResume": {
          "type": "boolean",
          "description": "Whether to automatically parse the resume to extract candidate data. Default: true"
        }
      },
      "required": [
        "file",
        "fileName",
        "resumeSource"
      ]
    }
  }
}
```

---
## Section 4: Data Dictionary & Constraints

This section outlines the critical data formatting rules, required fields, and value constraints the AI Agent must follow to avoid API errors.

### General Rules

- **Field Names:** All field names in request bodies are case-sensitive and should be in `camelCase`.
- **Required Fields:** Parameters marked as `required` in the documentation or schemas must not be null or empty.
- **Unique Identifiers:** `candidateId`, `jobId`, `contactId`, and `companyId` are the primary keys for their respective entities. Always use these IDs for lookups and updates when available.
- **Email Uniqueness:** The `email` field for a candidate must be unique across the entire JobDiva instance. Always check for an existing candidate by email before creating a new one.

### Data Formats

- **Dates & Timestamps:** Unless specified otherwise, all date and timestamp parameters must be in the format `MM/dd/yyyy HH:mm:ss`. For some newer endpoints, `yyyy-MM-dd'T'HH:mm:ss` is also accepted. Be consistent.
- **Phone Numbers:** While the API is flexible, it is best practice to standardize phone numbers to a consistent format, such as `(XXX) XXX-XXXX`.
- **State & Country:** Use standard 2-letter abbreviations for states (e.g., 'NY', 'CA', 'TX') and standard country codes (e.g., 'US', 'CA', 'UK').

### Enumerated Values (Enums)

- **Job Status:** When creating or updating jobs, the `status` field must exactly match one of the following: `["Open", "Closed", "On Hold", "Cancelled", "Draft"]`.
- **Candidate Status:** The `status` field for candidates should be one of: `["Active", "Inactive", "Do Not Use", "Placed"]`.
- **Salary Unit:** The `currentsalaryunit` and `preferredsalaryunit` fields must be one of: `["Hourly", "Annual", "Monthly", "Weekly"]`.
- **Note Type:** When creating notes, `noteType` should be one of: `["General", "Interview", "Phone Screen", "Email", "Meeting", "Follow-up"]`.
- **Rejection Reasons:** When rejecting an applicant, `reasonId` must be a valid integer ID retrieved from the `GET /apiv2/getRejectReasons` endpoint first.

### Field-Specific Constraints

- **Rate & Salary Fields:** Numeric fields like `currentsalary`, `preferredsalary`, `billrate`, and `payrate` cannot be null when part of a financial transaction (e.g., creating a start/placement). They should be provided as numbers (float or integer), not strings.
- **Boolean Values:** Boolean fields must be sent as `true` or `false` (lowercase), not `1` or `0`.
- **File Uploads:** When using `uploadResume` or `uploadJobAttachment`, the `file` parameter expects a Base64-encoded string of the file content.

### API Usage & Rate Limiting

- **Rate Limits:** The API has rate limits that are not explicitly defined in the document. The agent should avoid making rapid, high-volume requests in tight loops. Implement a small delay (e.g., 100-200ms) between consecutive calls in a batch process.
- **Pagination:** For endpoints that return lists (e.g., `searchCandidateProfile`, `SearchJob`), always use the `maxreturned` and `offset` parameters to paginate through results. Do not attempt to retrieve thousands of records in a single call.
- **Error Handling:** The agent must be prepared to handle `401` (Unauthorized), `403` (Forbidden), `404` (Not Found), and `500` (Server Error) responses. On a `401` error, the agent must re-authenticate.


---

## Appendix: Quick Reference

### Authentication Flow

```
1. POST /apiv2/authenticate
   Body: {
     "clientid": "your_client_id",
     "username": "your_username",
     "password": "your_password"
   }
   
2. Response: {
     "access_token": "eyJhbGc...",
     "token_type": "Bearer",
     "expires_in": 3600
   }
   
3. Use token in all subsequent requests:
   Header: Authorization: Bearer eyJhbGc...
```

### Common HTTP Status Codes

| Code | Meaning | Action Required |
|------|---------|-----------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 401 | Unauthorized | Re-authenticate and retry |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify resource ID exists |
| 500 | Server Error | Retry with exponential backoff |

### Best Practices for AI Agents

1. **Always validate before creating:** Search for existing records (by email, name, etc.) before creating new candidates or jobs to avoid duplicates.

2. **Use batch operations wisely:** When processing multiple records, implement pagination and rate limiting to avoid overwhelming the API.

3. **Log all interactions:** Maintain a detailed log of all API calls, responses, and errors for debugging and audit purposes.

4. **Handle errors gracefully:** Implement retry logic with exponential backoff for transient failures (5xx errors).

5. **Maintain data integrity:** Always validate data formats (dates, phone numbers, enums) before sending requests to minimize errors.

6. **Use IDs over names:** When possible, use internal IDs (candidateId, jobId) rather than names for lookups and updates, as IDs are guaranteed to be unique.

---

**Document Generated:** November 2025

**Source:** JobDiva API v2 Documentation (448 pages)

**Maintained By:** Manus AI

