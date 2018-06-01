*** Test Cases ***
One Step
    No Operation

Several Steps
    Log         First Step
    Log         Second Step
    Log         Third Step

Different Status Steps
    No Operation
    Fail

Embedded Steps
    First Step

# Not tested
Multiline Message In Step
    Log     First Line\nSecond Line

*** Keywords ***
First Step
    Second Step

Second Step
    Third Step

Third Step
    No Operation