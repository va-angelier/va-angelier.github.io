# API Test Coverage

## User registration
- Register user successfully
- Reject duplicate username registration
- Reject registration when password is too short
- Reject registration when role is invalid

## Authentication
- Log in successfully and return a session token
- Reject login when password is invalid
- Reject login when username does not exist
- Lock account after repeated failed login attempts when secure mode is enabled

## Profile access
- Return user profile successfully with a valid session
- Reject profile access when session token is missing or invalid

## Authentication and authorisation controls
- Reject record creation when API key is missing
- Reject record creation when session token is missing
- Reject record deletion for non-admin users

## Record creation
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
- Reject suspicious input when secure mode is enabled

## Record retrieval
- Return empty list when no records exist
- Return all created records
- Return single record by ID
- Return 404 when record does not exist

## Record update
- Update record successfully
- Return 404 when updating unknown record
- Reject update when name is missing
- Reject update when name is empty
- Reject update when name is not a string
- Reject update when name exceeds 100 characters
- Reject update when description is not a string
- Reject update when description exceeds 500 characters
- Reject update when unexpected fields are sent
- Reject malformed JSON during update

## Record deletion
- Delete record successfully as admin
- Return 404 when deleting unknown record
- Confirm deleted record is no longer present

## User deletion
- Delete user successfully as admin
- Return 404 when deleting unknown user

## Security mode
- Return current security mode as a boolean
- Change security mode successfully
- Allow suspicious input when secure mode is disabled

## Security event monitoring
- Return structured security events successfully for admin users