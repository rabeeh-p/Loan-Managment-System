# Loan Management API

## Overview
The Loan Management API is a Django-based backend system that enables users to apply for loans, view their loan details, make payments, and foreclose loans. Admins can manage loans, view all loan details, and delete loan records.

## Features
- User authentication and authorization (JWT-based)
- OTP-based user verification
- Loan application
- View user's loan list
- Loan foreclosure
- Admin functionalities (view all loans, delete loans)

## Technologies Used
- Django Rest Framework (DRF)
- JWT Authentication
- PostgreSQL
 
 

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/rabeeh-p/Loan-Managment-System/
cd loan-management
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file and add the necessary environment variables:
```sh
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/loan_db
```

### 5. Apply Migrations
```sh
python manage.py migrate
```

### 6. Create a Superuser (Admin)
```sh
python manage.py createsuperuser
```

### 7. Run the Server
```sh
python manage.py runserver
```

## API Endpoints
### User Authentication
| Method | Endpoint         | Description          |
|--------|----------------|----------------------|
| POST   | /api/login/    | User login          |
| POST   | /api/register/ | User registration   |

### Loan Management
| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| GET    | /api/loans/         | View user's loans       |
| POST   | /api/loans/         | Apply for a loan        |
| POST   | /api/loans/{id}/foreclose/ | Foreclose a loan |

### Admin Endpoints  
| Method | Endpoint               | Description                              |  
|--------|------------------------|------------------------------------------|  
| GET    | /api/admin/loans/      | View all loans (Admin only)             |  
| GET    | /api/admin/loans/{id}/ | View details of a specific loan (Admin only) |  
| DELETE | /api/admin/loans/{id}/ | Delete a loan (Admin only)              |  




## Role-Based Access
- **User**: Can apply for loans, view their loan details, and foreclose loans.
- **Admin**: Can view all loans, delete loans, and manage loan records.


## Developer Information
- **Name**: Rabeeh  
- **Role**: Full Stack Developer (Django + React.js)  
- **Email**: rabeehp008@example.com  
- **GitHub**: [github.com/rabeeh-p](https://github.com/rabeeh-p)  
- **Skills**: Backend Development, API Design, Database Management, Frontend (React.js)  
- **Passion**: Building scalable and efficient applications 🚀  

