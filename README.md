# Gig Backend API

Base URL: `http://127.0.0.1:8000`

## Authentication

- JWT Bearer token is required for protected endpoints.
- Header format:
  - `Authorization: Bearer <access_token>`

## API Endpoints

### 1. Register / Create Account

- Method: `POST`
- Endpoint: `/api/register/`
- Auth: Not required

#### Dummy Request Body

```json
{
  "email": "john@example.com",
  "mobile_number": "9876543210",
  "first_name": "John",
  "last_name": "Doe",
  "username": "john_doe",
  "display_name": "John D.",
  "user_type": 1,
  "is_online": false,
  "location": "Mumbai",
  "portfolio_urls": ["https://portfolio.example.com/john"],
  "password": "StrongPass@123"
}
```

#### Dummy Success Response (201)

```json
{
  "access_token": "<jwt_access_token>",
  "refresh_token": "<jwt_refresh_token>",
  "user": {
    "id": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
    "email": "john@example.com",
    "mobile_number": "9876543210",
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_doe",
    "display_name": "John D.",
    "full_name": "John Doe",
    "user_type": 1,
    "is_online": false,
    "is_verified": false,
    "location": "Mumbai",
    "portfolio_urls": ["https://portfolio.example.com/john"],
    "is_active": true,
    "is_staff": false,
    "created_at": "2026-03-09T10:00:00Z",
    "updated_at": "2026-03-09T10:00:00Z"
  }
}
```

### 2. Login

- Method: `POST`
- Endpoint: `/api/login/`
- Auth: Not required
- Use either `email` or `mobile_number` with `password`.

#### Dummy Request Body (email login)

```json
{
  "email": "john@example.com",
  "password": "StrongPass@123"
}
```

#### Dummy Request Body (mobile login)

```json
{
  "mobile_number": "9876543210",
  "password": "StrongPass@123"
}
```

#### Dummy Success Response (200)

```json
{
  "access_token": "<jwt_access_token>",
  "refresh_token": "<jwt_refresh_token>",
  "user": {
    "id": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
    "email": "john@example.com",
    "mobile_number": "9876543210",
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_doe",
    "display_name": "John D.",
    "full_name": "John Doe",
    "user_type": 1,
    "is_online": false,
    "is_verified": false,
    "location": "Mumbai",
    "portfolio_urls": ["https://portfolio.example.com/john"],
    "is_active": true,
    "is_staff": false,
    "created_at": "2026-03-09T10:00:00Z",
    "updated_at": "2026-03-09T10:00:00Z"
  }
}
```

### 3. Forgot Password

- Method: `POST`
- Endpoint: `/api/forgot-password/`
- Auth: Not required
- Send either `email` or `mobile_number`.

#### Dummy Request Body

```json
{
  "email": "john@example.com"
}
```

#### Dummy Success Response (200)

```json
{
  "detail": "Password reset token generated.",
  "uid": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
  "reset_token": "<reset_token>"
}
```

### 4. Get Logged-in User Profile

- Method: `GET`
- Endpoint: `/api/me/`
- Auth: Required (`Bearer <access_token>`)

#### Dummy Success Response (200)

```json
{
  "id": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
  "email": "john@example.com",
  "mobile_number": "9876543210",
  "first_name": "John",
  "last_name": "Doe",
  "username": "john_doe",
  "display_name": "John D.",
  "full_name": "John Doe",
  "user_type": 1,
  "is_online": false,
  "is_verified": false,
  "location": "Mumbai",
  "portfolio_urls": ["https://portfolio.example.com/john"],
  "is_active": true,
  "is_staff": false,
  "created_at": "2026-03-09T10:00:00Z",
  "updated_at": "2026-03-09T10:00:00Z"
}
```

### 5. Create Job

- Method: `POST`
- Endpoint: `/api/jobs/`
- Auth: Required (`Bearer <access_token>`)
- Only Normal Users (Clients) can create jobs.

#### Dummy Request Body

```json
{
  "title": "Build a landing page",
  "description": "Need a responsive marketing landing page with 4 sections.",
  "category": "Web Development",
  "location": "Remote",
  "budget": "500.00",
  "deadline": "2026-04-01",
  "status": "OPEN"
}
```

#### Dummy Success Response (201)

```json
{
  "id": 1,
  "created_by": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
  "title": "Build a landing page",
  "description": "Need a responsive marketing landing page with 4 sections.",
  "category": "Web Development",
  "location": "Remote",
  "budget": "500.00",
  "deadline": "2026-04-01",
  "status": "OPEN",
  "created_at": "2026-03-10T10:00:00Z",
  "updated_at": "2026-03-10T10:00:00Z"
}
```

### 6. List Jobs

- Method: `GET`
- Endpoint: `/api/jobs/`
- Auth: Required (`Bearer <access_token>`)
- Returns only `OPEN` jobs, newest first.
- Supports filtering:
  - `?category=cleaning`
  - `?location=Ahmedabad`
  - `?min_budget=500`
  - `?max_budget=5000`

#### Dummy Success Response (200)

```json
[
  {
    "id": 1,
    "created_by": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
    "title": "Build a landing page",
    "description": "Need a responsive marketing landing page with 4 sections.",
    "category": "Web Development",
    "location": "Remote",
    "budget": "500.00",
    "deadline": "2026-04-01",
    "status": "OPEN",
    "created_at": "2026-03-10T10:00:00Z",
    "updated_at": "2026-03-10T10:00:00Z"
  }
]
```

### 7. Job Detail

- Method: `GET`
- Endpoint: `/api/jobs/{id}/`
- Auth: Required (`Bearer <access_token>`)

#### Dummy Success Response (200)

```json
{
  "id": 1,
  "created_by": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
  "title": "Build a landing page",
  "description": "Need a responsive marketing landing page with 4 sections.",
  "category": "Web Development",
  "location": "Remote",
  "budget": "500.00",
  "deadline": "2026-04-01",
  "status": "OPEN",
  "created_at": "2026-03-10T10:00:00Z",
  "updated_at": "2026-03-10T10:00:00Z"
}
```

### 8. Place Bid (Worker)

- Method: `POST`
- Endpoint: `/api/jobs/{job_id}/bid/`
- Auth: Required (`Bearer <access_token>`)
- Only Workers can place bids.

#### Dummy Request Body

```json
{
  "bid_price": "1500.00",
  "proposal_message": "I can complete this job quickly.",
  "estimated_days": 2
}
```

#### Dummy Success Response (201)

```json
{
  "id": 10,
  "job": 1,
  "worker": {
    "id": "ab8b1c5a-76b3-4e5c-8b84-2e1a1f122222",
    "username": "worker_1",
    "display_name": "Worker One",
    "first_name": "Worker",
    "last_name": "One",
    "email": "worker@example.com"
  },
  "bid_price": "1500.00",
  "proposal_message": "I can complete this job quickly.",
  "estimated_days": 2,
  "status": "PENDING",
  "created_at": "2026-03-10T10:30:00Z"
}
```

### 9. View Bids for Job (Client)

- Method: `GET`
- Endpoint: `/api/jobs/{job_id}/bids/`
- Auth: Required (`Bearer <access_token>`)
- Only the job creator can view bids.

#### Dummy Success Response (200)

```json
[
  {
    "id": 10,
    "job": 1,
    "worker": {
      "id": "ab8b1c5a-76b3-4e5c-8b84-2e1a1f122222",
      "username": "worker_1",
      "display_name": "Worker One",
      "first_name": "Worker",
      "last_name": "One",
      "email": "worker@example.com"
    },
    "bid_price": "1500.00",
    "proposal_message": "I can complete this job quickly.",
    "estimated_days": 2,
    "status": "PENDING",
    "created_at": "2026-03-10T10:30:00Z"
  }
]
```

### 10. Worker Bids

- Method: `GET`
- Endpoint: `/api/worker/bids/`
- Auth: Required (`Bearer <access_token>`)
- Workers can see all bids they placed.

#### Dummy Success Response (200)

```json
[
  {
    "id": 10,
    "job": {
      "id": 1,
      "created_by": "f8c61eca-2b96-4e01-b29a-367f5fdb7f56",
      "title": "Build a landing page",
      "description": "Need a responsive marketing landing page with 4 sections.",
      "category": "Web Development",
      "location": "Remote",
      "budget": "500.00",
      "deadline": "2026-04-01",
      "status": "OPEN",
      "created_at": "2026-03-10T10:00:00Z",
      "updated_at": "2026-03-10T10:00:00Z"
    },
    "worker": "ab8b1c5a-76b3-4e5c-8b84-2e1a1f122222",
    "bid_price": "1500.00",
    "proposal_message": "I can complete this job quickly.",
    "estimated_days": 2,
    "status": "PENDING",
    "created_at": "2026-03-10T10:30:00Z"
  }
]
```

## Notes

- `user_type` values:
  - `1` = Normal User
  - `2` = Gig Worker
- `is_verified` is read-only in register API.
- UUID is used as primary key in all main tables.
