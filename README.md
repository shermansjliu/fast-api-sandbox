Project Specification: LinkHub API
🎯 Goal
Build a RESTful API using FastAPI that allows users to register, login, and manage a collection of favorite internet links.

🛠 Tech Stack
Language: Python 3.9+

Framework: FastAPI

Database: SQLite (for simplicity)

ORM: SQLModel (recommended) or SQLAlchemy

Auth: JWT (JSON Web Tokens) & Passlib

Level 1: The Foundation (Basics & Pydantic)
Focus: Understanding Schemas, Routing, and Validation.

[x] Project Setup: Create a virtual environment and install fastapi and uvicorn.

[x] Health Check: Create a GET / route that returns {"message": "Welcome to LinkHub API"}.

[x] Define Models: Create a Pydantic schema (schemas.py) for a Link.

Fields: title (str), url (str), description (optional str).

Requirement: Use Pydantic's HttpUrl type to ensure the URL is valid.

[ ] In-Memory CRUD: Create a temporary list fake_db = [].

Create a POST /links endpoint to add a link to the list.

Create a GET /links endpoint to return all links.

Level 2: The Data Layer (Async DB & ORM)
Focus: Connecting a real database and using async/await.

[x] Database Setup: Install sqlmodel and aiosqlite. Configure the engine.

[x] Table Creation: Create a database model (models.py) representing the Link table.

Columns: id (int, primary key), title, url, description, created_at (datetime).

[ ] Async Session: Create a dependency function get_session() that yields a database session.

[x] Refactor Routes: Replace the fake_db list with real Database queries.

Requirement: You must use async def for your routes and await for your database calls.

[x] Get Single Link: Create GET /links/{link_id}.

Handle 404 Not Found if the ID doesn't exist.

Level 3: Security & Authentication
Focus: User management, Password Hashing, and JWTs.

[x] User Model: Create a User table in the database.

Columns: id, username (unique), email (unique), password_hash.

[ ] Registration: Create POST /auth/register.

Requirement: Hash the password using bcrypt (via passlib) before saving to the DB. Never save plain text passwords!

[ ] Login: Create POST /auth/token.

Accept username/password form data (OAuth2 standard).

Verify password.

Return a JWT (JSON Web Token) containing the user's ID/subject.

[ ] Protect Routes: Lock down the POST /links route.

Only authenticated users with a valid JWT can add links.

Use Depends(get_current_user) to validate the token.

Level 4: Advanced Logic & Relationships
Focus: Connecting Tables and Authorization.

[ ] Database Relationships: Modify the Link table to include a user_id Foreign Key.

A Link belongs to a User. A User has many Links.

[ ] Ownership Logic: When a user creates a link, automatically assign their user_id to that link (using the token info).

[ ] Delete Endpoint: Create DELETE /links/{link_id}.

Critical Requirement: A user can only delete a link if they own it. If User A tries to delete User B's link, return 403 Forbidden.

Level 5: Polish (Query Params & Docs)
Focus: Developer Experience.

[ ] Pagination: Update GET /links to accept query parameters:

skip (default 0)

limit (default 10)

[ ] Search: Add an optional search query parameter to filter links by title.

[ ] Documentation: Add descriptions and examples to your Pydantic models so the automatic /docs page looks professional.