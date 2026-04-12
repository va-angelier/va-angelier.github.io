# **API UI (Unit 11\)**

## **Overview**

This user interface (UI) provides a lightweight front-end for interacting with the Secure CRUD API developed in Unit 9\. The primary purpose of the UI is to support demonstration, validation, and testing of the API functionality within a controlled development environment.

The UI enables users to manually construct and submit requests to the API and to observe structured JSON responses. It is intentionally minimal and does not aim to provide production-level functionality, but instead focuses on illustrating the behaviour of the underlying secure API.

---

## **Location**

SSDC\_POCM7E\_Assignment/Unit\_11/API-UI

---

## **Purpose**

The UI was developed to complement the backend API by providing a simple interface for:

* Demonstrating CRUD operations (Create, Read, Update, Delete)  
* Validating API responses under normal conditions  
* Testing error handling and input validation mechanisms  
* Supporting evidence collection for execution and testing

This approach aligns with secure software development practices, where both functional behaviour and failure modes must be observable and verifiable.

---

## **Features**

* Basic interface to send HTTP requests to the API  
* Display of structured JSON responses  
* Manual input fields for testing different payloads  
* Support for testing both valid and invalid input scenarios

---

## **Security Considerations**

The UI has been intentionally designed with minimal functionality to reduce complexity and avoid introducing additional attack surfaces. The following considerations apply:

* No authentication credentials are stored within the UI  
* No sensitive data is persisted in the browser  
* No client-side business logic is trusted for validation  
* All security controls are enforced server-side

This reflects the principle that security should not rely on the client layer but must be enforced within the backend system.

---

## **Limitations**

* No client-side validation beyond basic input formatting  
* No session management or authentication handling  
* No HTTPS enforcement (development environment only)  
* Not suitable for production deployment

---

## **Usage**

To use the UI:

1. Ensure the API is running locally (default: [http://127.0.0.1:5000](http://127.0.0.1:5000/))  
2. Open the UI in a web browser  
3. Enter request data and submit to the API  
4. Observe the returned JSON responses

---

## **Relationship to API**

This UI interacts directly with the Secure CRUD API implemented in Unit 9\. All security mechanisms, including validation, authentication, and error handling, are enforced by the backend API. The UI acts purely as a testing and demonstration layer.

