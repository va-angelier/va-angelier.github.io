# Secure CRUD API for Unit 9 and Unit 10

## Overview

This API was developed in Python using Flask and provides Create, Read, Update and Delete functionality for a standardised `Record` object. The design intentionally uses in-memory storage so that the focus remains on CRUD behaviour, endpoint design, validation, testing and secure handling of client input rather than on database configuration.

The application includes structured JSON responses, consistent endpoint naming, input validation, and lightweight API key protection for write operations. These choices were made to improve predictability, reduce the risk of unintended state changes, and demonstrate secure software development principles in a clear and testable manner.

A current limitation is that records are not persistent and are therefore lost when the application restarts. In a production environment, this implementation would need to be extended with persistent storage, stronger secret management and more mature authentication and authorisation mechanisms.

---

## Security Design Decisions

Several security-focused design choices were implemented in the API:

- Input payloads must be valid JSON objects.
- Only expected fields are accepted.
- The `name` field is required and must be a non-empty string.
- Maximum length constraints are enforced on `name` and `description`.
- Unexpected fields are rejected to reduce the risk of unintended or manipulated state.
- Write operations (`POST`, `PUT`, `DELETE`) require an API key through the `X-API-Key` header.
- Read operations (`GET`) remain open to support simple retrieval behaviour.

These controls help mitigate common risks such as:
- Injection-style attacks through strict input validation
- Broken access control via enforced API key checks
- Data integrity issues caused by malformed or unexpected input

---

## Unit 10 Seminar

### Relevance of Bogner et al. (2023) design rules to this API

The design rules proposed by Bogner et al. (2023) emphasise consistency, clarity and robustness in web API design. This is reflected in the API through consistent endpoint structures such as `/api/records` and `/api/records/<id>`, together with standardised JSON responses.

Strict input validation is applied through type checks, required fields, length constraints and rejection of unexpected fields. This improves both security and data integrity, particularly in distributed systems where multiple clients interact with the same service.

Clear error handling is implemented using appropriate HTTP status codes (`201`, `400`, `401`, `404`) and structured JSON responses. This supports client-side error handling and improves debugging.

A limitation of the current implementation is the use of in-memory storage, which does not provide persistence or scalability. A production system would require a database-backed architecture and stronger authentication mechanisms.

---

## Installation

### Linux or macOS

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the API

```bash
python app.py
```

---

## Running the Test Suite

```bash
pytest
```

---

## Running Code Quality Checks

```bash
flake8 .
pylint app.py
```

---

## Example Protected Request

The following example shows how to create a record using the required API key header for write operations:

```bash
curl -X POST http://127.0.0.1:5000/api/records ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: my-secret-api-access-token" ^
  -d "{\"name\":\"Example Record\",\"description\":\"Example Description\"}"
```

---

## Test Coverage

The automated test suite covers:

* Input validation (type checking, required fields, length constraints)
* Error handling (400, 401, 404 responses)
* CRUD operations (create, read, update, delete)
* Security behaviour (API key enforcement)
* Handling of malformed JSON input

All tests were executed successfully:

```text
32 passed
```

---

## Execution Evidence

The API was executed locally and tested using `pytest` and `curl`.

Successful verification includes:

* Record creation returns HTTP `201`
* Invalid input returns HTTP `400`
* Missing or incorrect API key returns HTTP `401`
* Retrieval of records returns HTTP `200`
* Non-existent records return HTTP `404`

These results confirm correct functional and security behaviour.

---

## Code Quality Evidence

Code quality was validated using `flake8` and `pylint` to ensure compliance with PEP-8 and general Python best practices. Any identified issues were resolved prior to submission.

---

## Files Included

* `app.py` — main Flask API
* `tests/test_api.py` — automated pytest test suite
* `requirements.txt` — project dependencies
* `README.md` — installation, usage and design documentation

---

## Limitations and Future Improvements

* Replace in-memory storage with a persistent database (e.g. PostgreSQL)
* Implement stronger authentication (e.g. OAuth or JWT)
* Move API keys to environment variables or secure configuration
* Add logging and monitoring to improve detection of abnormal behaviour
* Introduce rate limiting to reduce abuse risk

---

## References

* OWASP (2021) *OWASP Top 10*. Available at: [https://owasp.org](https://owasp.org)
* NIST (2022) *Secure Software Development Framework (SSDF)*
* Olmsted, A. (2024) *Security-Driven Software Development*. Packt Publishing

---

## Conclusion

This implementation demonstrates a secure and well-structured CRUD API with input validation, protected write operations and automated testing. It applies key principles of secure software development, including defensive input handling, access control and predictable API design.

Although simplified for academic purposes, the system provides a strong foundation for extension into a production-ready service aligned with industry security practices.