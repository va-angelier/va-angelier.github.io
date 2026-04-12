**React UI for Secure CRUD API (Unit 11\)**

---

**Overview**

This frontend application was developed using React to provide a simple user interface for the Secure CRUD API implemented in Unit 9\. The purpose of this interface is to demonstrate how a client application interacts with a backend API in a structured and controlled manner.

The application supports user authentication, record management and role-based access to administrative functionality. The emphasis is not on visual design, but on the correct and secure integration with a backend service in a distributed architecture.

---

**Architecture**

The frontend is implemented as a separate application and communicates with the Flask API over HTTP. This reflects a common architectural pattern in which responsibilities are clearly separated:

* The backend API is responsible for data processing, validation and security controls  
* The frontend is responsible for user interaction and presentation

The frontend communicates with the API using HTTP requests and includes:

* X-Session-Token for authentication  
* X-API-Key for protected operations

The application follows a stateless API design. After successful authentication, the client stores a session token in browser sessionStorage. This token is included in subsequent requests, allowing the backend to resolve user identity and role on each request.

No user identity (such as username or role) is trusted from the client side. All access control decisions are enforced server-side based on the validated session token. This ensures that security logic remains centralised within the backend and cannot be manipulated by the client.

---

**Authentication Model**

Authentication is implemented using a token-based approach. Upon successful login, the backend issues a session token which is stored in sessionStorage.

Subsequent requests include this token in the X-Session-Token header. The backend validates the token and determines the associated user and role for each request.

The frontend does not maintain authoritative authentication state. Instead, it retrieves the current user context via the /api/me endpoint. This ensures that all security-sensitive decisions are derived from the backend rather than from client-controlled data.

---

**Features**

The application provides the following functionality:

* User registration  
* User login and session handling  
* Dashboard view after authentication  
* Viewing records  
* Creating and updating records  
* Administrative functionality (depending on user role), including:  
  * Viewing security events  
  * Deleting records  
  * Toggling security mode  
* Token-based authentication with server-side identity resolution

The interface adapts dynamically based on the authenticated user role, demonstrating role-based access control at the presentation level while relying on backend enforcement for security.

---

**Project Structure**

The frontend follows a simple and modular structure:

* components/  
  Reusable UI elements such as navigation and route protection  
* pages/  
  Application pages (login, dashboard, records, admin)  
* services/  
  API communication logic and session handling

This structure is intentionally kept straightforward to prioritise clarity, maintainability and separation of concerns.

---

**Installation**

Navigate to the frontend directory:

cd Unit\_11/API-UI

Install dependencies:

npm install

---

**Running the Application**

Start the development server:

npm run dev

The application will be available at:

[http://localhost:5173](http://localhost:5173/)

**Credentials**

username: admin  
password: AdminPass123\!

---

**API Configuration**

The frontend is configured to communicate with the backend API at:

[http://127.0.0.1:5000/api](http://127.0.0.1:5000/api)

Before starting the frontend, ensure that the backend API is running.

Example:

python app.py \--seed-admin \--run-api \--secure on

---

**Important Note on Integration**

Because the frontend and backend run on different ports during development, browser security policies may block requests.

To resolve this, one of the following approaches may be required:

* Enabling CORS in the Flask API  
* Configuring a proxy in the frontend development server

This is a common consideration in distributed application development and reflects real-world deployment challenges.

---

**Limitations**

This frontend implementation is intentionally minimal and has several limitations:

* No persistent session storage beyond the browser session  
* API key is exposed in the frontend (not suitable for production)  
* No advanced state management (e.g. Redux or Context API)  
* Token is stored in sessionStorage, which may be vulnerable to client-side attacks such as XSS  
* No token expiration or refresh mechanism is implemented  
* No HTTPS enforcement (development environment)  
* Input validation is primarily enforced at the backend, with minimal client-side validation

These limitations are acceptable within the scope of this module, where the focus is on demonstrating secure API interaction and architectural design rather than production readiness.

---

**Conclusion**

This frontend demonstrates how a React-based client can interact with a secure backend API using structured, token-based communication. The implementation highlights the importance of separating concerns between user interface and backend logic, while ensuring that security-critical decisions remain server-side.

Although intentionally simple, the application provides a clear and functional example of a distributed system in which frontend and backend components operate independently, communicate via defined interfaces, and enforce security through well-defined boundaries.

