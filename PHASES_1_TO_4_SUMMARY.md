# CivicPulse: Phases 1 to 4 Summary (Demo Preparation)

This document provides a high-level summary of the first four phases of the CivicPulse project. You can use this as a reference guide to explain the architecture and progress during your assignment demo.

---

## Phase 1: Frontend Shell (React + Vite)
**Goal:** Build the visual shell of the application without a real backend.
* **What we did:** We created the initial React frontend with three main pages: Submit a Complaint, Dashboard, and Stats. We set up routing, global CSS styles, and TypeScript interfaces for our data.
* **How we did it:** We used `Vite` for a fast development setup. Since we didn't have a backend yet, we hardcoded some "sample data" directly into the React app so we could see what the Dashboard would look like. We also built out the forms to ensure users could type in their complaints.

## Phase 2: Backend API Shell (FastAPI)
**Goal:** Build the backend endpoints and business logic, but store data temporarily in memory.
* **What we did:** We created a Python FastAPI backend. We defined all the API endpoints (Routes) for getting and creating complaints, and updating their status. We also added strict business logic so that complaints could only follow legal status transitions (e.g., Open -> In Progress), returning a `409 Conflict` error if a user tried an illegal move.
* **How we did it:** We used `Pydantic` to validate incoming data. For data storage, instead of setting up a database right away, we just used a simple Python `dictionary` (an in-memory store) in our repository layer. This allowed us to test our API endpoints quickly, even though the data would disappear if the server restarted.

## Phase 3: Frontend-Backend Integration
**Goal:** Connect Phase 1 and Phase 2 together.
* **What we did:** We made the React frontend talk to the FastAPI backend over the network. We deleted the hardcoded sample data from the frontend.
* **How we did it:** The frontend was updated to make real HTTP requests (`GET`, `POST`, `PATCH`) to our `localhost:8000` FastAPI server. When a user submitted a form on the React site, it successfully traveled to the FastAPI server and was saved in the Python dictionary. We also handled error messages—if a user tried an illegal status update on the frontend, the UI would catch the backend's `409` error and display it to the user.

## Phase 4: PostgreSQL Persistence (Database)
**Goal:** Replace the temporary in-memory dictionary with a real, permanent database.
* **What we did:** We connected our backend to a real PostgreSQL database so that user complaints would survive even if the FastAPI server restarted.
* **How we did it:** 
  1. **Postgres via Docker:** Instead of installing database software directly on our laptops, we spun up a PostgreSQL database inside a Docker container. This is a clean, standard way to run databases locally.
  2. **SQLAlchemy (ORM):** We used SQLAlchemy to write Python classes (Models) that represent our database tables. This way, we can interact with the database using Python objects instead of writing raw SQL code.
  3. **Alembic (Migrations):** We used Alembic to actually create the tables inside the Postgres database. Alembic tracks changes to our database schema over time (called "migrations"). If we ever need to add a new column to a table later, Alembic safely updates the database without deleting our existing data.

---
**Current Status:** The application now has a fully working frontend, a strict backend API, and a permanent PostgreSQL database.
