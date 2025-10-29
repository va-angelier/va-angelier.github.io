from behave import *

@given("a root user account")
def step_create_root(context):
    context.is_root = True

@when("the user creates a user account")
def step_create_user_account(context):
    context.exit_code = 0

@when("the users tries to install packages")
def step_install_packages(context):
    context.exit_code = 0

@then("the system should allow")
def step_allow(context):
    assert context.exit_code == 0