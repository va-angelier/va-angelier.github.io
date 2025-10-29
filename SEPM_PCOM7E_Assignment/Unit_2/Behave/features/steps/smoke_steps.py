from behave import given, when, then

@given('I have the text "{msg}"')
def step_given(context, msg):
    context.msg = msg

@when("I uppercase the text")
def step_when(context):
    context.output = context.msg.upper()

@then('I see "{expected}"')
def step_then(context, expected):
    assert context.output == expected
