*** Settings ***
Resource    ../../resources/base_visible_elements.resource

Suite Setup       Open Wikipedia App
Suite Teardown    Close Wikipedia App

*** Test Cases ***
# Run Keyword
#     Get Visible Elements On Screen    all    debug=True

Return all visible elements
    [Documentation]    Should return all visible elements on the screen
    [Tags]             smoke    visible    all 
    # The goal of a smoke test is to validate the minimum working flow. Accepting an empty list could hide a problem.
    # So we use 'Should Not Be Empty' to ensure the return is not empty.
    ${elements}=    Get Visible Elements On Screen    all    auto    debug=True 
    Should Not Be Empty    ${elements}

Return only clickable elements
    [Documentation]    Should return only elements where the 'clickable' attribute is true
    [Tags]             regression    filter    clickable
    ${elements}=    Get Visible Elements On Screen    clickable    auto    debug=True
    FOR    ${el}    IN    @{elements}
        Should Be True    ${el['clickable']} == ${True}
    END

Return only elements with visible text
    [Documentation]    Should return only elements whose "text" attribute is not empty
    [Tags]             regression    filter    text
    @{elements}=    Get Visible Elements On Screen    text    auto    debug=True
    FOR    ${el}    IN    @{elements}
        Should Not Be Empty    ${el['text']} 
    END

Return only resource_id when id_mode is resource_id (debug mode)
    [Documentation]    All 'kind' should be 'resource_id'
    [Tags]             id_mode    resource_id    debug
    @{els}=    Get Visible Elements On Screen    all    resource_id    debug=True
    FOR    ${el}    IN    @{els}
        Dictionary Should Contain Key    ${el}    identifier
        ${id}=    Get From Dictionary    ${el['identifier']}    kind
        Should Be Equal    ${id}    resource_id
        # non-empty value
        ${val}=    Get From Dictionary    ${el['identifier']}    value
        Should Not Be Empty    ${val}
    END

Return only accessibility_id when id_mode is accessibility_id (debug mode)
    [Documentation]    All 'kind' should be 'accessibility_id'
    [Tags]             id_mode    accessibility_id    debug
    @{els}=    Get Visible Elements On Screen    all    accessibility_id    debug=True
    FOR    ${el}    IN    @{els}
        ${id}=    Get From Dictionary    ${el['identifier']}    kind
        Should Be Equal    ${id}    accessibility_id
        ${val}=    Get From Dictionary    ${el['identifier']}    value
        Should Not Be Empty    ${val}
    END

Auto id_mode returns mixed kinds (debug mode)
    [Documentation]    'kind' could be both: 'resource_id' and 'accessibility_id'
    [Tags]    id_mode    auto    debug
    @{els}=    Get Visible Elements On Screen    all    auto    debug=True
    FOR    ${el}    IN    @{els}
        ${kind}=    Get From Dictionary    ${el['identifier']}    kind
        Should Be True    '${kind}'=='resource_id' or '${kind}'=='accessibility_id'
    END

Return only Buttons
    [Documentation]    Should return only elements whose class contains the substring "Button"
    [Tags]             regression    filter    button
    ${elements}=    Get Visible Elements On Screen    button    auto    debug=True
    FOR    ${el}    IN    @{elements}
        Should Contain    ${el['class']}    Button
    END

Return only text input fields
    [Documentation]    Should return only elements whose class contains the substring "EditText"
    [Tags]             regression    filter    input
    ${elements}=    Get Visible Elements On Screen    input    debug=True
    FOR    ${el}    IN    @{elements}
        Should Contain    ${el['class']}    EditText
    END

Validate normal mode structure
    [Documentation]    Validates the string list (no-dict) returned in normal mode
    [Tags]             normal    type    exploratory
    @{ids}=    Get Visible Elements On Screen    clickable    auto    debug=False
    FOR    ${item}    IN    @{ids}
        ${is_str}=    Evaluate    isinstance($item, str)
        Should Be True    ${is_str}
        Should Not Be Empty    ${item}
    END

No duplicates in normal mode results
    [Documentation]    Checks if '(kind, value)' used by 'seen' works correctly
    [Tags]    dedup    normal
    @{ids}=    Get Visible Elements On Screen    all    auto    debug=False
    ${count}=    Get Length    ${ids}
    @{unique}=    Remove Duplicates    ${ids}
    ${ucount}=    Get Length    ${unique}
    Should Be Equal As Integers    ${count}    ${ucount}

Validate debug mode structure
    [Documentation]    Validates the JSON structure returned in debug mode
    [Tags]             debug    exploratory
    ${result}=    Get Visible Elements On Screen    all    auto    debug=True
    FOR    ${el}    IN    @{result}
        Dictionary Should Contain Key    ${el}    identifier
        Dictionary Should Contain Key    ${el}    resource_id
        Dictionary Should Contain Key    ${el}    accessibility_id
        Dictionary Should Contain Key    ${el}    text
        Dictionary Should Contain Key    ${el}    class
        Dictionary Should Contain Key    ${el}    clickable
        # identifier with 'value' and 'kind'
        ${id_dict}=    Get From Dictionary    ${el}    identifier
        Dictionary Should Contain Key         ${id_dict}    value
        Dictionary Should Contain Key         ${id_dict}    kind
        Should Not Be Empty                   ${id_dict['value']}
        Should Be True                       '${id_dict['kind']}'=='resource_id' or '${id_dict['kind']}'=='accessibility_id'
    END

Validate error for invalid id_mode
    [Documentation]    When passing a invalid mode, the keyword should fail with a clear message
    [Tags]             negative    error    invalid_id_mode
    Run Keyword And Expect Error    Invalid id_mode*
    ...    Get Visible Elements On Screen    all    aoo

Validate error for invalid filter
    [Documentation]    When passing an invalid filter, the keyword should fail with a clear message
    [Tags]             negative    error    invalid_filter
    Run Keyword And Expect Error    Invalid filter*    
    ...    Get Visible Elements On Screen    foo    auto

Allow empty results for strict combinations
    [Documentation]    strict combination (input + accessibility_id, in this case) can return empty lists in a screen without "EditText" with "content-desc"
    [Tags]    edgecase    empty_ok
    @{els}=    Get Visible Elements On Screen    input    accessibility_id    debug=False
    # Should accept empty without failure
    ${is_list}=    Evaluate    isinstance(${els}, list)
    Should Be True    ${is_list}