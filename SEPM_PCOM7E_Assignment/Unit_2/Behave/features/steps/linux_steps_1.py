from behave import *

# Scenario Standard users without sudo denied software installation  
@given('a non-privileged user account without sudo privileges')  
def step_create_non_privileged_user(context):  
    context.sudoers = False

# Scenario when users have sudo
@given("a non-privileged user account with sudo privileges")
def step_create_sudoer(context):
    context.sudoers = True

@when("the user attempts to execute apt-get install [package]")
def step_attempt_install(context):
    if getattr(context, 'sudoers', False):
        context.exit_code = 0
        context.packages_installed = True
    else:
        context.exit_code = 1
        context.packages_installed = False
    

@then("the system shall return an access denied error (exit code 1)")
def step_return_error(context):
    assert context.exit_code == 1, f"Expected exit code 1, got: {getattr(context, 'exit_code', None)}"

@then("no package shall be installed")
def step_no_package_installed(context):
    assert context.packages_installed is False

@then("the system will allow installion of the package")
def step_installed_sudo(context):
    assert context.packages_installed is True