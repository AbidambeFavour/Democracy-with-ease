# SimpleVote API — Endpoint Reference

> **Django Voting System** | Session-based authentication | HTML responses (form-driven)

---

## Table of Contents

1. [Overview](#overview)
2. [Base URL & Environments](#base-url--environments)
3. [Authentication & Session Model](#authentication--session-model)
4. [Environment Variables](#environment-variables)
5. [Testing Notes](#testing-notes)
6. [Endpoint Groups](#endpoint-groups)
   - [General](#1-general)
   - [Authentication](#2-authentication)
   - [Accounts & Profiles](#3-accounts--profiles)
   - [Poll Management](#4-poll-management)
   - [Admin](#5-admin)
7. [Recommended Testing Order](#recommended-testing-order)
8. [Common Response Codes](#common-response-codes)

---

## Overview

SimpleVote is a Django-based voting platform. Its endpoints serve **server-rendered HTML pages** and handle **HTML form submissions** — they are not a REST/JSON API (with the exception of the Toggle Online Status endpoint). All write operations use `application/x-www-form-urlencoded` bodies, and most successful mutations respond with an HTTP `302` redirect.

The Postman collection (`SimpleVote API Collection`) mirrors every route in the application and includes automated test scripts on each request.

---

## Base URL & Environments

| Environment        | Base URL                  | File                                      |
|--------------------|---------------------------|-------------------------------------------|
| SimpleVote Local   | `http://127.0.0.1:8000`   | `postman/environments/SimpleVote Local.yaml` |

**Before sending any request:**

1. Select the **SimpleVote Local** environment in Postman.
2. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
3. Ensure the database is migrated:
   ```bash
   python manage.py migrate
   ```

The `{{baseUrl}}` variable resolves to `http://127.0.0.1:8000` by default. Update it in the environment if your server runs on a different port.

---

## Authentication & Session Model

SimpleVote uses **Django's built-in cookie-based session authentication**. There are no API tokens or Authorization headers to manage manually.

**How it works:**

1. Send a `GET` to the login page — Django sets a `csrftoken` cookie.
2. Send a `POST` to `/accounts/login/` with credentials — Django sets a `sessionid` cookie on success.
3. Postman automatically stores and forwards both cookies on all subsequent requests.
4. Send a `GET` to `/accounts/logout/` to clear the session.

> **No manual token handling is required.** Postman's cookie jar handles everything automatically as long as you run requests in order.

The Login test script also saves the `sessionid` value to the collection variable `sessionid` for reference.

---

## Environment Variables

All variables are defined in the **SimpleVote Local** environment file (`postman/environments/SimpleVote Local.yaml`).

| Variable        | Default Value                   | Purpose                                                        |
|-----------------|---------------------------------|----------------------------------------------------------------|
| `baseUrl`       | `http://127.0.0.1:8000`         | Root URL of the Django dev server                              |
| `username`      | `testuser123`                   | Test account username (used in login, registration, profile)   |
| `password`      | `complexpassword123`            | Test account password                                          |
| `email`         | `testuser123@example.com`       | Test account email (registration, password reset)              |
| `pk`            | `1`                             | Numeric ID of a poll (poll detail, submit vote)                |
| `poll_id`       | `1`                             | Numeric ID of a poll (comments, reactions)                     |
| `choice`        | `1`                             | Numeric ID of a poll choice (submit vote)                      |
| `reaction_type` | `like`                          | Reaction type — one of: `like`, `love`, `haha`, `wow`, `sad`, `angry` |
| `uidb64`        | `sample-uid`                    | Base64-encoded user ID from a password reset email link        |
| `token`         | `sample-token`                  | Token from a password reset email link                         |

> **Tip:** Update `pk`, `poll_id`, and `choice` to match IDs that actually exist in your local database. After creating a poll via the Create Poll request, the test script automatically captures the new poll's `pk` into the collection variable.

---

## Testing Notes

- **Response type:** Most endpoints return `text/html`. Only `Toggle Online Status` returns `application/json`.
- **Redirects:** Postman follows redirects by default. If you want to inspect the raw `302` response and its `Location` header, disable "Follow Redirects" in Postman settings for that request.
- **CSRF:** Django's CSRF middleware is active. The `csrftoken` cookie set by the GET login/register pages is automatically sent back by Postman on POST requests — no extra header is needed in most cases.
- **Order matters:** Run Authentication requests before Poll Management or Accounts requests that require login.
- **Test scripts:** Every request has an `afterResponse` test script. Run the full collection via **Collection Runner** to execute all tests in sequence.
- **Response time threshold:** All tests assert a response time below 3000–5000 ms. Adjust if your machine is slow.

---

## Endpoint Groups

---

### 1. General

#### `GET /`  — Home Redirect

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/` |
| **Auth required** | No |
| **Content-Type** | — |

**Description:** Root URL of the application. Redirects to the accounts landing page. Use this as a smoke test to confirm the server is running and reachable.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Server renders a page directly |
| `301`/`302`/`303` | Server redirects to landing page |

**Test assertions:**
- Server is reachable (2xx or 3xx)
- Response time < 3000 ms
- If 200: response body contains `<html`

---

### 2. Authentication

All authentication endpoints live under `/accounts/`. Form submissions use `Content-Type: application/x-www-form-urlencoded`.

---

#### `GET /accounts/register/`  — Register (GET)

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/register/` |
| **Auth required** | No |

**Description:** Loads the user registration page. Use this to confirm the form renders before submitting.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Registration form rendered |

**Test assertions:**
- Status 200
- Response is HTML
- Form contains `username` and `password` fields

---

#### `POST /accounts/register/`  — Register (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/accounts/register/` |
| **Auth required** | No |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Submit the registration form to create a new user account. On success, the user is automatically logged in and redirected to their dashboard.

**Body parameters:**

| Field | Value | Required | Description |
|-------|-------|----------|-------------|
| `username` | `{{username}}` | Yes | Unique username |
| `email` | `{{email}}` | Yes | Email address |
| `first_name` | `Test` | Yes | First name |
| `last_name` | `User` | Yes | Last name |
| `password1` | `{{password}}` | Yes | Chosen password |
| `password2` | `{{password}}` | Yes | Password confirmation — must match `password1` |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Registration successful — user logged in, redirected to dashboard |
| `200`  | Validation error — form re-rendered with error messages (e.g. username already taken) |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- If 302: `sessionid` cookie is set (user auto-logged in)
- If 200: no `500` or `Server Error` in body

---

#### `GET /accounts/login/`  — Login (GET)

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/login/` |
| **Auth required** | No |

**Description:** Loads the login page. Also sets the `csrftoken` cookie, which the test script captures into the `csrftoken` collection variable.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Login form rendered |

**Test assertions:**
- Status 200
- Response is HTML
- Form contains `username` and `password` fields
- `csrftoken` cookie captured into collection variable

---

#### `POST /accounts/login/`  — Login (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/accounts/login/` |
| **Auth required** | No |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Submit login credentials. On success, Django sets a `sessionid` cookie that Postman stores and forwards automatically on all subsequent requests.

**Body parameters:**

| Field | Value | Required | Description |
|-------|-------|----------|-------------|
| `username` | `{{username}}` | Yes | Account username |
| `password` | `{{password}}` | Yes | Account password |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Login successful — redirected to dashboard |
| `200`  | Invalid credentials — login page re-rendered |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- `sessionid` cookie is set and non-empty
- If 200: body does not contain `"Invalid username or password"`
- `sessionid` saved to collection variable `sessionid`

---

#### `GET /accounts/logout/`  — Logout

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/logout/` |
| **Auth required** | Yes (session cookie) |

**Description:** Logs out the currently authenticated user. Clears the session and redirects to the landing page.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Logged out — redirected to landing page |
| `200`  | Landing page rendered directly |

**Test assertions:**
- Status 200 or 302
- Response time < 3000 ms
- If 302: `sessionid` cookie is cleared or empty

---

#### `POST /accounts/password-reset/`  — Password Reset Request (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/accounts/password-reset/` |
| **Auth required** | No |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Submit an email address to trigger a password reset email. Django always redirects to the "done" page regardless of whether the email exists (to prevent user enumeration).

**Body parameters:**

| Field | Value | Required | Description |
|-------|-------|----------|-------------|
| `email` | `{{email}}` | Yes | Email address associated with the account |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Redirected to password reset done page |
| `200`  | Form re-rendered (rare) |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- If 200: no `500` or `Server Error` in body

---

#### `GET /accounts/password-reset/done/`  — Password Reset Done

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/password-reset/done/` |
| **Auth required** | No |

**Description:** Informational confirmation page shown after a password reset email has been sent.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Confirmation page rendered |

**Test assertions:**
- Status 200
- Response is HTML
- Body contains `email`, `password`, or `reset`

---

#### `POST /accounts/password-reset-confirm/{{uidb64}}/{{token}}/`  — Password Reset Confirm (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/accounts/password-reset-confirm/{{uidb64}}/{{token}}/` |
| **Auth required** | No |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Submit a new password using the reset link token. The `uidb64` and `token` values come from the password reset email link (e.g. `/accounts/password-reset-confirm/Mg/abc123-xyz/`).

**Path variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `uidb64` | `{{uidb64}}` | Base64-encoded user ID from the reset email link |
| `token` | `{{token}}` | One-time token from the reset email link |

**Body parameters:**

| Field | Value | Required | Description |
|-------|-------|----------|-------------|
| `new_password1` | `newSecurePassword123` | Yes | New password |
| `new_password2` | `newSecurePassword123` | Yes | New password confirmation — must match `new_password1` |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Valid token — password changed, redirected to complete page |
| `200`  | Invalid/expired token — form re-rendered with error |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- If 200: no `500` or `Server Error` in body

> **Tip:** Copy the `uidb64` and `token` values from the reset link in the email Django sends (check the console output in development mode) and update the environment variables before sending this request.

---

#### `GET /accounts/password-reset-complete/`  — Password Reset Complete

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/password-reset-complete/` |
| **Auth required** | No |

**Description:** Informational page shown after a password has been successfully reset.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Completion page rendered |

**Test assertions:**
- Status 200
- Response is HTML
- Body contains `password`, `complete`, or `login`

---

### 3. Accounts & Profiles

---

#### `GET /accounts/`  — Accounts Landing

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/` |
| **Auth required** | No |

**Description:** Landing page for unauthenticated users. Authenticated users are automatically redirected to their dashboard.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Unauthenticated — landing page rendered |
| `302`  | Authenticated — redirected to dashboard |

**Test assertions:**
- Status 200 or 302
- Response time < 3000 ms
- If 200: response is HTML containing `<html`

---

#### `GET /accounts/landing/`  — Accounts Landing (explicit route)

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/landing/` |
| **Auth required** | No |

**Description:** Explicit alias for the landing page. Functionally identical to `GET /accounts/`. Useful for verifying both URL aliases resolve correctly.

**Expected responses:** Same as `GET /accounts/`

---

#### `GET /accounts/dashboard/`  — User Dashboard

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/dashboard/` |
| **Auth required** | Yes (session cookie) |

**Description:** Authenticated user dashboard showing the user's polls, votes, and activity. Redirects to login if unauthenticated.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Authenticated — dashboard rendered |
| `302`  | Unauthenticated — redirected to login |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- If 200: response is HTML; body contains `dashboard`, `poll`, or `vote`
- If 302: `Location` header contains `login`

---

#### `GET /accounts/admin-dashboard/`  — Admin Dashboard

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/admin-dashboard/` |
| **Auth required** | Yes — staff user (`is_staff=True`) |

**Description:** Staff-only dashboard with site-wide statistics. Regular authenticated users receive a `302` redirect or `403`. Unauthenticated users are redirected to login.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Staff user — admin dashboard rendered |
| `302`  | Non-staff or unauthenticated — redirected |
| `403`  | Non-staff authenticated user — forbidden |

**Test assertions:**
- Status 200, 302, or 403
- Response time < 5000 ms
- If 200: response is HTML; body contains `admin`, `user`, or `poll`

---

#### `GET /accounts/profile/`  — Edit Profile (GET)

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/profile/` |
| **Auth required** | Yes (session cookie) |

**Description:** Loads the profile edit form for the currently authenticated user.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Authenticated — edit form rendered |
| `302`  | Unauthenticated — redirected to login |

**Test assertions:**
- Status 200 or 302
- Response time < 3000 ms
- If 200: response is HTML; form contains `first_name`, `email`, or `profile`

---

#### `POST /accounts/profile/`  — Edit Profile (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/accounts/profile/` |
| **Auth required** | Yes (session cookie) |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Update the current user's profile information. All fields are optional — only include the ones you want to update.

**Body parameters:**

| Field | Value | Required | Description |
|-------|-------|----------|-------------|
| `first_name` | `Test` | No | User first name |
| `last_name` | `User` | No | User last name |
| `email` | `{{email}}` | No | Email address |
| `bio` | `A short bio about the user.` | No | Short biography shown on profile page |
| `location` | `Lagos, Nigeria` | No | User location |
| `birth_date` | `1995-06-15` | No | Date of birth in `YYYY-MM-DD` format |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Update successful — redirected to profile page |
| `200`  | Validation error — form re-rendered |
| `302`  | Unauthenticated — redirected to login |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- If 200: no `500` or `Server Error` in body

---

#### `GET /accounts/profile/{{username}}/`  — View User Profile

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/accounts/profile/{{username}}/` |
| **Auth required** | No |

**Description:** View the public profile page of any user by their username.

**Path variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `username` | `{{username}}` | Username of the profile to view |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | User exists — profile page rendered |
| `404`  | User not found |

**Test assertions:**
- Status 200 or 404
- Response time < 3000 ms
- If 200: response is HTML; body contains the username value

---

#### `POST /accounts/toggle-online/`  — Toggle Online Status

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/accounts/toggle-online/` |
| **Auth required** | Yes (session cookie) |
| **Content-Type** | — (no body) |
| **Response type** | `application/json` |

**Description:** AJAX endpoint that updates the current user's `last_seen` timestamp to track online status. Typically called by the frontend on page load or at intervals. This is the **only endpoint that returns JSON**.

**Required header:**

| Header | Value | Description |
|--------|-------|-------------|
| `X-Requested-With` | `XMLHttpRequest` | Marks the request as an AJAX call |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Authenticated POST — `{"status": "success"}` |
| `302`  | Unauthenticated — redirected to login |
| `400`  | Wrong HTTP method (e.g. GET) — `{"status": "error"}` |

**Response body (200):**
```json
{
  "status": "success"
}
```

**Test assertions:**
- Status 200, 302, or 400
- Response time < 3000 ms
- If 200: `Content-Type` is `application/json`; body has `status` field equal to `"success"`

---

### 4. Poll Management

All poll endpoints live under `/voting/`. Write operations require an active login session.

---

#### `GET /voting/`  — List Polls

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/voting/` |
| **Auth required** | No |

**Description:** Retrieve the list of all polls. Supports optional query parameters for filtering.

**Query parameters (all optional, disabled by default in collection):**

| Parameter | Example | Description |
|-----------|---------|-------------|
| `category` | `Technology` | Filter polls by category slug |
| `search` | `programming` | Search polls by keyword in title or description |
| `status` | `active` | Filter by poll status: `active`, `ended`, or `upcoming` |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Poll list page rendered |

**Test assertions:**
- Status 200
- Response is HTML
- Response time < 5000 ms
- Body contains `poll`, `vote`, or `voting`

> **Tip:** Enable the query parameters in Postman by unchecking the "disabled" checkbox next to each one to test filtering.

---

#### `GET /voting/poll/{{pk}}/`  — Poll Detail (GET)

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/voting/poll/{{pk}}/` |
| **Auth required** | No |

**Description:** View a single poll including its choices, comments, reactions, and results (depending on poll visibility settings).

**Path variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `pk` | `{{pk}}` | Numeric primary key of the poll |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Poll exists — detail page rendered |
| `404`  | Poll not found |

**Test assertions:**
- Status 200 or 404
- Response time < 5000 ms
- If 200: response is HTML; body contains `poll`, `vote`, or `choice`

---

#### `POST /voting/poll/{{pk}}/`  — Submit Vote (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/voting/poll/{{pk}}/` |
| **Auth required** | Yes (session cookie) |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Cast a vote on a poll. The `choice` value must be the numeric ID of one of the poll's choices. If the poll allows multiple votes, you may submit multiple `choice` values.

**Path variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `pk` | `{{pk}}` | Numeric primary key of the poll to vote on |

**Body parameters:**

| Field | Value | Required | Description |
|-------|-------|----------|-------------|
| `choice` | `{{choice}}` | Yes | Numeric ID of the choice to vote for |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Vote cast — redirected back to poll detail |
| `302`  | Already voted or poll closed — redirected back with error message |
| `302`  | Unauthenticated — redirected to login |
| `404`  | Poll not found |

**Test assertions:**
- Status 200, 302, or 404
- Response time < 5000 ms
- If 302: `Location` header is not null

> **Tip:** Get the correct `choice` ID by inspecting the poll detail page HTML or the database. Update the `choice` environment variable before sending.

---

#### `GET /voting/create/`  — Create Poll Form (GET)

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/voting/create/` |
| **Auth required** | Yes (session cookie) |

**Description:** Loads the create poll form. Use this to confirm the form renders before submitting a new poll.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Authenticated — create poll form rendered |
| `302`  | Unauthenticated — redirected to login |

**Test assertions:**
- Status 200 or 302
- Response time < 3000 ms
- If 200: response is HTML; form contains `title`, `choice`, or `poll`
- If 302: `Location` header contains `login`

---

#### `POST /voting/create/`  — Create Poll (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/voting/create/` |
| **Auth required** | Yes (session cookie) |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Create a new poll. At least two choices must be provided (`choice_1`, `choice_2`). Dates use `YYYY-MM-DD` format and times use `HH:MM` format.

**Body parameters:**

| Field | Example Value | Required | Description |
|-------|---------------|----------|-------------|
| `title` | `Best programming language for beginners?` | Yes | Poll title |
| `description` | `Vote for the language you think is easiest...` | No | Detailed description |
| `category` | `Technology` | No | Poll category |
| `tags` | `programming, beginners, coding` | No | Comma-separated tags |
| `start_date` | `2025-01-01` | Yes | Poll start date (`YYYY-MM-DD`) |
| `start_time` | `08:00` | Yes | Poll start time (`HH:MM`) |
| `end_date` | `2025-12-31` | Yes | Poll end date (`YYYY-MM-DD`) |
| `end_time` | `23:59` | Yes | Poll end time (`HH:MM`) |
| `is_public` | `on` | No | Set to `on` to make the poll publicly visible |
| `allow_multiple_votes` | `off` | No | Set to `on` to allow multiple choice selection |
| `max_votes_per_user` | `1` | No | Maximum choices a single user can vote for |
| `show_results_immediately` | `on` | No | Set to `on` to show results immediately after voting |
| `choice_1` | `Python` | Yes | First choice option |
| `choice_2` | `JavaScript` | Yes | Second choice option (minimum required) |
| `choice_3` | `Scratch` | No | Third choice option (add more as needed) |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Poll created — redirected to new poll's detail page |
| `200`  | Validation error — form re-rendered |
| `302`  | Unauthenticated — redirected to login |

**Test assertions:**
- Status 200 or 302
- Response time < 5000 ms
- If 302 to poll detail: new poll `pk` extracted from `Location` header and saved to collection variable `pk`
- If 200: no `500` or `Server Error` in body

---

#### `POST /voting/poll/{{poll_id}}/comment/`  — Add Comment (POST)

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/voting/poll/{{poll_id}}/comment/` |
| **Auth required** | Yes (session cookie) |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Description:** Post a comment on a poll.

**Path variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `poll_id` | `{{poll_id}}` | Numeric ID of the poll to comment on |

**Body parameters:**

| Field | Example Value | Required | Description |
|-------|---------------|----------|-------------|
| `content` | `This is a great poll! My vote goes to Python.` | Yes | Comment text content |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Comment posted — redirected back to poll detail |
| `302`  | Unauthenticated — redirected to login |
| `404`  | Poll not found |

**Test assertions:**
- Status 200, 302, or 404
- Response time < 5000 ms
- If 302: `Location` header is not null

---

#### `POST /voting/poll/{{poll_id}}/react/{{reaction_type}}/`  — Toggle Reaction

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **URL** | `{{baseUrl}}/voting/poll/{{poll_id}}/react/{{reaction_type}}/` |
| **Auth required** | Yes (session cookie) |
| **Content-Type** | — (no body) |

**Description:** Toggle a reaction on a poll. If the user has already reacted with the same type, the reaction is removed (toggled off). Invalid reaction types are silently ignored.

**Path variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `poll_id` | `{{poll_id}}` | Numeric ID of the poll to react to |
| `reaction_type` | `{{reaction_type}}` | Reaction type — must be one of: `like`, `love`, `haha`, `wow`, `sad`, `angry` |

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `302`  | Reaction toggled — redirected back to poll detail |
| `302`  | Unauthenticated — redirected to login |
| `404`  | Poll not found |

**Test assertions:**
- Status 200, 302, or 404
- Response time < 5000 ms
- If 302: `Location` header is not null
- `reaction_type` variable is one of the six valid values

---

### 5. Admin

---

#### `GET /admin/`  — Django Admin Site

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL** | `{{baseUrl}}/admin/` |
| **Auth required** | Superuser account (separate from session) |

**Description:** Django's built-in admin interface. Access requires a superuser account. Use this URL to manage users, polls, votes, choices, comments, and reactions directly in the database.

**Expected responses:**

| Status | Condition |
|--------|-----------|
| `200`  | Admin login page or admin index rendered |

**Test assertions:**
- Status 200
- Response is HTML
- Body contains `django`, `admin`, or `log in`

> **Tip:** Create a superuser with `python manage.py createsuperuser` and log in at `/admin/` to inspect and manage all model data during testing.

---

## Recommended Testing Order

Run requests in this order for a complete end-to-end flow:

```
1.  GET  /                                          → Smoke test (server reachable)
2.  GET  /accounts/register/                        → Load registration form
3.  POST /accounts/register/                        → Create test account
4.  GET  /accounts/login/                           → Load login form (captures csrftoken)
5.  POST /accounts/login/                           → Authenticate (captures sessionid)
6.  GET  /accounts/dashboard/                       → Verify authenticated dashboard
7.  GET  /voting/                                   → Browse poll list
8.  GET  /voting/create/                            → Load create poll form
9.  POST /voting/create/                            → Create a new poll (captures pk)
10. GET  /voting/poll/{{pk}}/                       → View the new poll
11. POST /voting/poll/{{pk}}/                       → Submit a vote
12. POST /voting/poll/{{poll_id}}/comment/          → Add a comment
13. POST /voting/poll/{{poll_id}}/react/{{reaction_type}}/ → Toggle a reaction
14. GET  /accounts/profile/{{username}}/            → View public profile
15. GET  /accounts/profile/                         → Load edit profile form
16. POST /accounts/profile/                         → Update profile
17. POST /accounts/toggle-online/                   → Update online status (JSON)
18. GET  /accounts/logout/                          → Log out
19. POST /accounts/password-reset/                  → Request password reset
20. GET  /accounts/password-reset/done/             → View reset confirmation page
21. GET  /admin/                                    → Access Django admin
```

---

## Common Response Codes

| Code | Meaning in SimpleVote |
|------|-----------------------|
| `200` | Page rendered successfully (HTML or JSON) |
| `302` | Redirect — either successful action or auth redirect to login |
| `400` | Bad request — wrong HTTP method (Toggle Online Status) |
| `403` | Forbidden — insufficient permissions (Admin Dashboard) |
| `404` | Resource not found — invalid poll ID or username |
| `500` | Server error — check Django console for traceback |

---

*Generated from the SimpleVote API Collection — `postman/collections/SimpleVote API Collection`*  
*Environment: SimpleVote Local — `postman/environments/SimpleVote Local.yaml`*
