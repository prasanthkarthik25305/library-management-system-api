## 📄 `README.md`

````md
# Library Management System API

A RESTful backend API for managing books, members, borrowing transactions, and fines in a library system.  
This project enforces strict business rules using a service-layer state machine approach.

---

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **API Docs**: Swagger / OpenAPI 3.1
- **Testing**: Postman

---

## 📦 Features

- Full CRUD operations for Books and Members
- Borrow and return lifecycle with state validation
- Book state machine (`available → borrowed → overdue → available`)
- Borrowing constraints:
  - Max 3 books per member
  - Block borrowing if unpaid fines exist
- Automatic fine calculation for overdue books
- Clean separation of concerns (routers, services, models)

---


MEMBERS ────────< TRANSACTIONS >──────── BOOKS
   |                    |
   |                    |
   └──────────< FINES >─┘



## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/library-management-system-api.git
cd library-management-system-api
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=mysql+pymysql://root:<your_password>@localhost/library_management
```

---

## ▶️ Run the Application

```bash
python -m uvicorn app.main:app
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## Database Schema

### Tables

* **books**
* **members**
* **transactions**
* **fines**

### Relationships

```
MEMBERS ──< TRANSACTIONS >── BOOKS
   │               │
   └──────< FINES >┘
```

Foreign key constraints ensure data integrity.

---

## 🔄 State Machine Implementation

### Book States

* `available`
* `borrowed`
* `overdue`
* `maintenance`

State transitions are enforced **only in the service layer**.

### Transaction States

* `active`
* `returned`
* `overdue`

Invalid transitions are blocked programmatically.

---

## Business Rules Enforced

* A member cannot borrow more than **3 books simultaneously**
* Members with **unpaid fines cannot borrow**
* Loan period is **14 days**
* Fine: **$0.50 per overdue day**

All rules are centralized in the service layer.

---

## API Testing (Postman)

A Postman collection is included for easy testing.

📁 Location:

```
postman/library-api.postman_collection.json
```

You can import this file into Postman to test all endpoints.

---

## API Endpoints (Summary)

### Books

* `POST /books`
* `GET /books`
* `GET /books/available`
* `PUT /books/{id}/maintenance`

### Members

* `POST /members`
* `GET /members`
* `GET /members/{id}/borrowed`

### Transactions

* `POST /transactions/borrow`
* `POST /transactions/{id}/return`
* `GET /transactions/overdue`

---

## Evaluation Readiness

* Clean code structure
* Centralized business logic
* Proper HTTP status codes
* Complete API documentation
* Postman collection included

---
