# **Secure Online Retailer API / CLI Prototype (Unit 9\)**

## **Overview**

This project implements a secure online retailer API and CLI prototype using Python and Flask as part of the Secure Software Development module. The system extends beyond a basic CRUD application by incorporating secure account management, authentication, session handling, role-based access control, and security monitoring.

The implementation is designed to demonstrate how security controls can be embedded within application logic, aligning with secure software development principles and the design work developed earlier in the module.

---

## **Location**

SSDC\_POCM7E\_Assignment/Unit\_9/Artifacts/API

---

## **Core Features**

### **User Management**

* Secure user registration  
* Password hashing using PBKDF2-HMAC-SHA256 with per-user salt  
* Role assignment (user / admin)

### **Authentication & Sessions**

* Secure login mechanism  
* Cryptographically secure session token generation  
* Session-based authentication via `X-Session-Token` header  
* Logout and session invalidation

### **Access Control**

* Role-based access control (RBAC)  
* Admin-only operations (e.g. user deletion, security event access)  
* Combined enforcement of API key and session token for protected endpoints

### **Record Management (CRUD)**

* Create, Read, Update, Delete operations on records  
* Input validation for all operations  
* Consistent JSON responses

### **Security Monitoring**

* Structured security event logging  
* Tracking of authentication attempts, failures, and administrative actions  
* Retrieval of security events via protected endpoint

### **Security Mode**

* Runtime toggle for enabling or disabling security controls  
* Demonstrates impact of security configurations on system behaviour

### **CLI Support**

* Optional command-line interface for administrative actions  
* Ability to seed default admin user  
* Listing of users and records for testing purposes

---

## **Security Features**

The system implements multiple security mechanisms aligned with common application-layer risks:

* Strict JSON validation (rejects malformed requests)  
* Field-level validation and sanitisation  
* Detection of simple suspicious input patterns (e.g. injection indicators)  
* Password hashing using PBKDF2-HMAC-SHA256  
* Secure session token generation  
* Role-based access control  
* Account lockout after repeated failed login attempts  
* Controlled error handling to prevent information leakage  
* Structured security event logging

These controls address common vulnerabilities such as injection, broken access control, and insufficient logging, as identified in OWASP guidance.

---

## **Setup**

Install required dependencies:

pip install \-r requirements.txt

---

## **Running the Application**

Run the API:

python app.py \--run-api

Optional flags:

\--secure on/off       Enable or disable security mode    
\--seed-admin          Create default admin account    
\--list-records        List records via CLI    
\--list-users          List users via CLI  

---

## **Authentication Example**

### **Register a User**

curl \-X POST http://127.0.0.1:5000/api/register \\  
\-H "Content-Type: application/json" \\  
\-d '{"username": "user1", "password": "StrongPass123\!", "role": "user"}'

### **Login**

curl \-X POST http://127.0.0.1:5000/api/login \\  
\-H "Content-Type: application/json" \\  
\-d '{"username": "user1", "password": "StrongPass123\!"}'

### **Authenticated Request**

curl \-X GET http://127.0.0.1:5000/api/me \\  
\-H "X-Session-Token: \<token\>"

---

## **Record Example**

curl \-X POST http://127.0.0.1:5000/api/records \\  
\-H "Content-Type: application/json" \\  
\-H "X-API-Key: your\_api\_key" \\  
\-H "X-Session-Token: \<token\>" \\  
\-d '{"name": "example", "description": "test record"}'

---

## **Testing**

Run unit tests:

pytest

Static analysis (example):

flake8 .

---

## **Limitations**

* In-memory storage (no persistence)  
* No token expiry or refresh mechanism  
* No HTTPS enforcement (development environment only)  
* Simplified input validation and pattern detection  
* No rate limiting or advanced monitoring

---

## **Future Improvements**

* Integration with secure database (e.g. ORM with parameterised queries)  
* Token-based authentication (e.g. JWT with expiry)  
* Rate limiting and intrusion detection  
* Deployment behind reverse proxy with TLS  
* Centralised logging and monitoring

---

## **Relationship to UI**

This API is used by the UI implemented in Unit 11\.  
All security controls are enforced server-side, while the UI acts purely as a testing and demonstration layer.

---

## **Summary**

This implementation demonstrates how security can be integrated into application design through layered controls, including validation, authentication, authorisation, and monitoring. The system reflects a defence-in-depth approach and provides a practical foundation for further development.

