import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueOut, IssueUpdate
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get("/", response_model=list[IssueOut])
def get_issues():
    """Retrieve all issues from storage."""
    return load_data()


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """Create a new issue with a unique ID."""
    issues = load_data()
    
    new_issue = { 
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority.value,
        "status": "open",
    }
    
    issues.append(new_issue)
    save_data(issues)
    return new_issue


@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    """Get a single issue by its unique ID."""
    issues = load_data()
    
    for issue in issues:
        # Check if the entry is a dict before accessing 'id'
        if isinstance(issue, dict) and issue.get("id") == issue_id:
            return issue
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Issue not found"
    )


@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    """Update an existing issue by ID."""
    issues = load_data()

    for issue in issues:
        if isinstance(issue, dict) and issue.get("id") == issue_id:
            # Update only fields that were provided in the request body
            if payload.title is not None:
                issue["title"] = payload.title
            if payload.description is not None:
                issue["description"] = payload.description
            if payload.priority is not None:
                issue["priority"] = payload.priority.value
            if payload.status is not None:
                issue["status"] = payload.status.value

            save_data(issues)
            return issue

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue not found"
    )


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str):
    """Delete an issue by ID."""
    issues = load_data()

    for i, issue in enumerate(issues):
        if isinstance(issue, dict) and issue.get("id") == issue_id:            
            issues.pop(i)
            save_data(issues)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue not found"
    )