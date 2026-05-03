# API Reference

Complete API documentation for SampleProject.

## Metadata

- **name**: APIReference
- **version**: `1.0.0`
- **base_url**: `/api/v1`

## Endpoints

### Users

- `GET /api/v1/users` - List all users
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/{id}` - Get user details

### Data Processing

- `POST /api/v1/process` - Submit data for processing
- `GET /api/v1/process/{job_id}` - Check job status

## Authentication

```python
# auth.py
from fastapi import HTTPException

def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=401)
    return {"user_id": 123}
```

## Error Handling

Standard error responses:

- `400` Bad Request
- `401` Unauthorized
- `404` Not Found
- `500` Internal Server Error

## Related Documents

- Back to [Project Overview](project_overview.md)
- See [Deployment Guide](deployment.md)
