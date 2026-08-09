# W4 — Auth: Login & Protect (Backend AI Engineering)

A production-ready, secure FastAPI REST API implementing user authentication (Sign Up, Log In, Log Out) and Bearer JWT token protection powered by **Supabase Auth** as the Identity Provider (IdP).

---

## 🔒 The Trust Triangle & Security Architecture

```text
[ Client / Browser / Swagger UI ]
       │                      ▲
       │ 1. Email/Password     │ 2. Issues Bearer JWT
       ▼                      │
[ Supabase Auth (IdP) ] ──────┘
       │
       │ 3. Client attaches "Authorization: Bearer <JWT>"
       ▼
[ FastAPI Server ] ───▶ 4. Verifies Token via Dependency ───▶ Access Granted / 401 Unauthorized
```

### Key Security Practices
* **Identity Provider (IdP):** User accounts, password hashing, and token issuance are delegated to Supabase Auth. Raw passwords are never stored or logged by the application server.
* **Reusable Dependency Injection:** Token verification is decoupled into a reusable FastAPI `get_current_user` dependency function (`Depends(get_current_user)`).
* **Bearer JWT Security Scheme:** Integrated with OpenAPI `HTTPBearer` to enable interactive Bearer Token authorization inside Swagger UI (`/docs`).

---

## 🛠️ Environment Configuration (.env & .env.example)

Private Supabase credentials must be configured via environment variables.

### 1. `.env.example` (Committed to Git)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
PORT=8000
```

### 2. `.env` (Git-Ignored)
Create a `.env` file in `week 4/` with your actual Supabase Project URL and Anon API key:
```env
SUPABASE_URL=https://auth-practice.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=8000
```

---

## 🚀 Quickstart: How to Run in Under 1 Minute

### Prerequisites
* Python 3.10+ installed.

### One-Command Setup & Launch
```bash
python -m venv venv && source venv/bin/activate || venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8000
```

Once running, visit:
* **Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`
* **Root Endpoint:** `http://localhost:8000/`
* **Public Info:** `http://localhost:8000/public/info`

---

## 📋 API Endpoint Reference Table

| HTTP Method | Path | Auth Required? | Description | Success Code | Error Codes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | No | Root server information | `200 OK` | - |
| `GET` | `/public/info` | No | Public, unprotected information | `200 OK` | - |
| `POST` | `/auth/signup` | No | Register a new user account | `201 Created` | `400 Bad Request` |
| `POST` | `/auth/login` | No | Authenticate user & return Bearer JWT | `200 OK` | `400 Bad Request`, `401 Unauthorized` |
| `POST` | `/auth/logout` | **Yes (Bearer JWT)** | Revoke user session & logout | `204 No Content` | `401 Unauthorized` |
| `GET` | `/protected/profile` | **Yes (Bearer JWT)** | Fetch authenticated user profile | `200 OK` | `401 Unauthorized` |
| `GET` | `/protected/dashboard` | **Yes (Bearer JWT)** | View private dashboard metrics | `200 OK` | `401 Unauthorized` |

---

## 🧪 Sample `curl -i` Verification Commands

### 1. Sign Up (`POST /auth/signup`)
```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```
**Response:** `HTTP/1.1 201 Created`

### 2. Log In (`POST /auth/login`)
```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```
**Response:** `HTTP/1.1 200 OK` returning `access_token` and `refresh_token`.

### 3. Protected Profile with Bearer Token (`GET /protected/profile`)
```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN_HERE>"
```
**Response:** `HTTP/1.1 200 OK` returning user metadata.

---

## 🥊 Stage 7: The AI Rematch ("AI vs Me")

### The Prompt Used
> *"Build a secure Python FastAPI authentication API using Supabase Auth as the Identity Provider. Include POST /auth/signup (201 Created), POST /auth/login (200 OK with access_token), POST /auth/logout (204 No Content), GET /public/info (200 OK), and GET /protected/profile. Protect endpoints using a reusable FastAPI Depends dependency that parses 'Authorization: Bearer <token>', verifies it with Supabase Auth, and returns 401 Unauthorized for missing or invalid tokens."*

### Analysis & Diff Answers

#### 1. Token Extraction Handling (Bearer Prefix Parsing)
* **AI Version:** Used naive `authorization.replace("Bearer ", "").strip()`. If a client sent a token without the `Bearer ` prefix (e.g. raw token string), it silently passed un-stripped tokens to Supabase.
* **Hand-Built Version:** Used FastAPI's official `HTTPBearer(auto_error=False)` security scheme, which properly validates header formatting and integrates directly with Swagger UI's "Authorize" padlock button.

#### 2. Security Flaws & Invalid Token Handling
* **AI Version:** Used generic `except Exception: raise HTTPException(401, detail="Invalid token")` without checking for missing JSON body keys, resulting in internal 500 errors when empty JSON payloads `{}` were submitted.
* **Hand-Built Version:** Implemented explicit Pydantic and JSON body inspection (`400 Bad Request` for missing fields, `401 Unauthorized` for invalid credentials/tokens).

#### 3. What the Prompt Missed
* The prompt forgot to specify how Swagger UI bearer security should be configured, causing the AI version to generate `/docs` without the "Authorize" padlock button.

---

## 📌 Commit Log History

```text
* Stage 6: publish to GitHub and write README
* Stage 5: Swagger UI documentation with bearer auth
* Stage 4: auth middleware and logout endpoint
* Stage 3: profile route token verification
* Stage 2: public route and unverified protected route
* Stage 1: signup and login routes working
* Stage 0: setup server and supabase client
```
