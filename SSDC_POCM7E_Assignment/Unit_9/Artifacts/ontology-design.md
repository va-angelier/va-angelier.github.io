# API Project

The API developed for this unit demonstrates the implementation of basic CRUD functionality within a distributed architecture context, specifically focusing on Create and Read operations. Flask was selected as the underlying framework due to its lightweight nature and suitability for rapid API development. The system exposes RESTful endpoints which allow clients to create new records and retrieve stored data through HTTP methods such as POST and GET.

A simple ontology was defined to standardise the structure of data exchanged between components. Each record consists of an identifier, name, description and timestamp, ensuring consistency across requests and responses. This structured approach is essential in distributed systems, where multiple services may interact with the same data model. By enforcing a clear schema, the API reduces ambiguity and supports interoperability between services.

From a security perspective, basic validation is implemented to ensure that required fields are present and that malformed input is rejected. Although the current implementation uses in-memory storage for simplicity, the design can be extended to persistent storage systems without altering the API contract. This separation between interface and implementation reflects principles of distributed system design, where services communicate through well-defined interfaces.

Overall, the API illustrates how backend functionality can be exposed in a controlled and structured manner, forming the foundation for more complex distributed or microservice-based systems.

This API implements the full CRUD model through REST-style endpoints using Flask. Create, Read, Update and Delete operations are exposed through POST, GET, PUT and DELETE methods respectively. The system uses a simple in-memory datastore for demonstration purposes, which is appropriate for a teaching example because it allows the API behaviour to be tested without introducing database complexity. Basic validation is applied to incoming JSON payloads to ensure that required fields are present, that values have the correct type, and that empty or excessively long inputs are rejected. This improves reliability and reduces the risk of malformed data being accepted by the service. A clear ontology is also present, as each record follows a standard structure consisting of an identifier, name, description and timestamps. In a distributed environment, such standardisation is important because it provides consistency between components and makes the API easier to integrate, maintain and extend.

## Entity: Record

|Field|Type|Description|
|id||int|Unique|identifier|
|name|string|Record name|
|description|string|Optional description|
|created_at|string|Timestamp|


## Validation / security rules

Accepted request body

The API only accepts a JSON object with these fields:

name
description

No other fields are allowed.

### Rule 1: Request body must be valid JSON

If the request body is missing, malformed, or not a JSON object, reject it.

Error message:
Request body must be a valid JSON object.

### Rule 2: Only expected fields are allowed

If the client sends fields other than name and description, reject the request.

Example invalid fields:

admin
password
created_at
updated_at

Error message format:
Unexpected field(s): field_name.

### Rule 3: name is required for create

When creating a record, the name field must be present.

Error message:
Field 'name' is required.

### Rule 4: name must be a string

If name exists, it must be a string.

Error message:
Field 'name' must be a string.

### Rule 5: name cannot be empty

After trimming whitespace, name must still contain text.

Examples rejected:

""
" "

Error message:
Field 'name' cannot be empty.

### Rule 6: name must not exceed 100 characters

If name is longer than 100 characters, reject it.

Error message:
Field 'name' must not exceed 100 characters.

### Rule 7: description must be a string

If description is present, it must be a string.

Error message:
Field 'description' must be a string.

### Rule 8: description must not exceed 500 characters

If description is longer than 500 characters, reject it.

Error message:
Field 'description' must not exceed 500 characters.

### Rule 9: Missing description gets a safe default

If description is not provided, store it as an empty string.

### Rule 10: Non-existent record IDs return 404

If a client requests, updates, or deletes a record that does not exist, return:

Error message:
Record not found.

Validation behaviour by CRUD operation
Create

Endpoint: POST /api/records

Validation applied:

JSON object required
only name and description allowed
name required
name must be a non-empty string
name max 100 chars
description optional
if provided, description must be a string
description max 500 chars
Read all

Endpoint: GET /api/records

Validation applied:

no request body validation needed
Read one

Endpoint: GET /api/records/<id>

Validation applied:

record must exist
Update

Endpoint: PUT /api/records/<id>

Validation applied:

record must exist
JSON object required
only name and description allowed
name required
name must be a non-empty string
name max 100 chars
description optional
if provided, description must be a string
description max 500 chars
Delete

Endpoint: DELETE /api/records/<id>

Validation applied:

record must exist

## Validation checklist

- Request body must be a valid JSON object
- Only 'name' and 'description' are allowed
- 'name' is required for create and update
- 'name' must be a string
- 'name' cannot be empty after trimming
- 'name' must not exceed 100 characters
- 'description' must be a string if present
- 'description' must not exceed 500 characters
- Missing 'description' defaults to an empty string
- Read/update/delete on unknown ID returns 404

### Create record
```bash
curl -X POST http://127.0.0.1:5000/api/records \
-H "Content-Type: application/json" \
-d '{"name": "Test", "description": "First record"}'
```

### Get all records
```bash
curl http://127.0.0.1:5000/api/records
```

### Update record
```bash
curl -X PUT http://127.0.0.1:5000/api/records/1 \
-H "Content-Type: application/json" \
-d "{\"name\": \"Updated record\", \"description\": \"Updated description\"}"
```


## Tests
API test coverage

- Create record successfully
- Reject create when name is missing
- Reject create when name is empty
- Reject create when name is not a string
- Reject create when name exceeds 100 characters
- Reject create when description is not a string
- Reject create when description exceeds 500 characters
- Reject create when unexpected fields are sent
- Accept create when description is omitted and default to empty string
- Reject malformed JSON

- Return empty list when no records exist
- Return all created records
- Return single record by ID
- Return 404 when record does not exist

- Update record successfully
- Return 404 when updating unknown record
- Reject invalid update payload
- Reject unexpected fields during update

- Delete record successfully
- Return 404 when deleting unknown record
- Confirm deleted record is no longer present

## Test evidence
```bash
(base) victorangelier@VictorM1 API % pytest -v
================================================================= test session starts =================================================================
platform darwin -- Python 3.12.2, pytest-8.4.2, pluggy-1.6.0 -- /opt/anaconda3/bin/python
cachedir: .pytest_cache
hypothesis profile 'default'
rootdir: /Users/victorangelier/Documents/Prive/Victor/Essex/va-angelier.github.io/SSDC/Unit9/API
plugins: hypothesis-6.138.2, anyio-4.2.0, cov-7.0.0
collected 28 items                                                                                                                                    

tests/test_api.py::test_create_record_success PASSED                                                                                            [  3%]
tests/test_api.py::test_create_record_with_missing_name_returns_400 PASSED                                                                      [  7%]
tests/test_api.py::test_create_record_with_empty_name_returns_400 PASSED                                                                        [ 10%]
tests/test_api.py::test_create_record_with_non_string_name_returns_400 PASSED                                                                   [ 14%]
tests/test_api.py::test_create_record_with_name_too_long_returns_400 PASSED                                                                     [ 17%]
tests/test_api.py::test_create_record_with_non_string_description_returns_400 PASSED                                                            [ 21%]
tests/test_api.py::test_create_record_with_description_too_long_returns_400 PASSED                                                              [ 25%]
tests/test_api.py::test_create_record_with_unexpected_field_returns_400 PASSED                                                                  [ 28%]
tests/test_api.py::test_create_record_with_missing_description_uses_default_empty_string PASSED                                                 [ 32%]
tests/test_api.py::test_create_record_with_invalid_json_returns_400 PASSED                                                                      [ 35%]
tests/test_api.py::test_create_record_with_non_object_json_returns_400 PASSED                                                                   [ 39%]
tests/test_api.py::test_get_all_records_returns_empty_list_initially PASSED                                                                     [ 42%]
tests/test_api.py::test_get_all_records_returns_created_records PASSED                                                                          [ 46%]
tests/test_api.py::test_get_single_record_success PASSED                                                                                        [ 50%]
tests/test_api.py::test_get_single_record_not_found_returns_404 PASSED                                                                          [ 53%]
tests/test_api.py::test_update_record_success PASSED                                                                                            [ 57%]
tests/test_api.py::test_update_record_not_found_returns_404 PASSED                                                                              [ 60%]
tests/test_api.py::test_update_record_with_missing_name_returns_400 PASSED                                                                      [ 64%]
tests/test_api.py::test_update_record_with_empty_name_returns_400 PASSED                                                                        [ 67%]
tests/test_api.py::test_update_record_with_non_string_name_returns_400 PASSED                                                                   [ 71%]
tests/test_api.py::test_update_record_with_name_too_long_returns_400 PASSED                                                                     [ 75%]
tests/test_api.py::test_update_record_with_non_string_description_returns_400 PASSED                                                            [ 78%]
tests/test_api.py::test_update_record_with_description_too_long_returns_400 PASSED                                                              [ 82%]
tests/test_api.py::test_update_record_with_unexpected_field_returns_400 PASSED                                                                  [ 85%]
tests/test_api.py::test_update_record_with_invalid_json_returns_400 PASSED                                                                      [ 89%]
tests/test_api.py::test_update_record_with_non_object_json_returns_400 PASSED                                                                   [ 92%]
tests/test_api.py::test_delete_record_success PASSED                                                                                            [ 96%]
tests/test_api.py::test_delete_record_not_found_returns_404 PASSED                                                                              [100%]

================================================================= 28 passed in 0.27s ==================================================================
(base) victorangelier@VictorM1 API % 
```