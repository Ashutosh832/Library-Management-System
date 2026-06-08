def issue_serializer(issue) -> dict:
    return {
        "id": str(issue["_id"]),
        "user_id": issue["user_id"],
        "user" : issue["user"],
        "book_id": issue["book_id"],
        "book_name" : issue["book_name"],
        "issue_date": issue["issue_date"],
        "return_date": issue["return_date"],
        "status": issue["status"]
    }

def issues_serializer(issues) -> list:
    return [issue_serializer(issue) for issue in issues]

