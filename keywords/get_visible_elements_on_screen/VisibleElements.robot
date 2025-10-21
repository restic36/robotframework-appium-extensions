*** Settings ***
Resource    VisibleElementsResource.robot

Suite Setup       Open Wikipedia App
Suite Teardown    Close Wikipedia App

*** Test Cases ***
# Run Keyword
#     Get Visible Elements On Screen    all    debug=True

Return all visible elements
    [Documentation]    Should return all visible elements on the screen
    [Tags]    smoke    visible    all 
    # The goal of a smoke test is to validate the minimum working flow. Accepting an empty list could hide a problem.
    # So we use 'Should Not Be Empty' to ensure the return is not empty.
    ${elements}=    Get Visible Elements On Screen    all    debug=True 
    Should Not Be Empty    ${elements}

Return only clickable elements
    [Documentation]    Should return only elements where the 'clickable' attribute is true
    [Tags]    regression    filter    clickable
    ${elements}=    Get Visible Elements On Screen    clickable    debug=True
    FOR    ${el}    IN    @{elements}
        Should Be True    ${el['clickable']}
    END

Return only elements with visible text
    [Documentation]    Should return only elements whose "text" attribute is not empty
    [Tags]    regression    filter    text
    @{elements}=    Get Visible Elements On Screen    text    debug=True
    FOR    ${el}    IN    @{elements}
        Should Not Be Empty    ${el['text']} 
    END

Return only Buttons
    [Documentation]    Should return only elements whose class contains the substring "Button"
    [Tags]    regression    filter    button
    ${elements}=    Get Visible Elements On Screen    button    debug=True
    FOR    ${el}    IN    @{elements}
        Should Contain    ${el['class']}    Button
    END

Return only text input fields
    [Documentation]    Should return only elements whose class contains the substring "EditText"
    [Tags]    regression    filter    input
    ${elements}=    Get Visible Elements On Screen    input    debug=True
    FOR    ${el}    IN    @{elements}
        Should Contain    ${el['class']}    EditText
    END

Validate debug mode structure
    [Documentation]    Validates the JSON structure returned in debug mode
    [Tags]    debug    exploratory
    ${result}=    Get Visible Elements On Screen    all    debug=True
    FOR    ${el}    IN    @{result}
        Dictionary Should Contain Key    ${el}    resource_id
        Dictionary Should Contain Key    ${el}    accessibility_id
        Dictionary Should Contain Key    ${el}    text
        Dictionary Should Contain Key    ${el}    class
        Dictionary Should Contain Key    ${el}    clickable
    END

Validate error for invalid filter
    [Documentation]    When passing an invalid filter, the keyword should fail with a clear message
    [Tags]             negative    error    invalid_filter
    Run Keyword And Expect Error    Filter inválido*    
    ...    Get Visible Elements On Screen    foo