Feature: Linux Operating System Access Control  
  As a system administrator  
  I want to enforce role-based access control  
  So that unauthorised users cannot compromise system integrity  

Scenario: Standard user denied software installation privilege
  Given a non-privileged user account without sudo privileges
  When the user attempts to execute apt-get install [package]
  Then the system shall return an access denied error (exit code 1)
  And no package shall be installed
  
Scenario: Users accounts with sudo shoud allow installation privilege
  Given a non-privileged user account with sudo privileges
  When the user attempts to execute apt-get install [package]
  Then the system will allow installion of the package

Scenario: Root users can create users and install packages
  Given a root user account
  When the user creates a user account
  Then the system should allow

Scenario: Root users can create users and install packages
  Given a root user account
  When the users tries to install packages
  Then the system should allow
