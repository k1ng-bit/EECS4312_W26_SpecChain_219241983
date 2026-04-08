# Requirement ID: FR_hybrid_1
- Description: [The system shall allow users to record daily mood entries through structured checkins.]
- Source Persona: [Consistent Mood Tracker]
- Traceability: [Derived from review group H1]
- Acceptance Criteria: [Given the user opens the check in screen When the user selects and submits a mood then the entry shall be saved.]
- Notes: [Rewritten from the automated requirement to remove vague wording and improve testability.]

# Requirement ID: FR_hybrid_2
- Description: [The system shall provide users with access to previously recorded mood entries.]
- Source Persona: [Consistent Mood Tracker]
- Traceability: [Derived from review group H1]
- Acceptance Criteria: [Given the user opens mood history When past entries are displayed then entries shall be visible in chronological order.]
- Notes: [Added new requirement from the hybrid group to make sure system functions in a way the user wants it to.]

# Requirement ID: FR_hybrid_3
- Description: [The system shall launch successfully and allow users to access the app without crashing.]
- Source Persona: [Reliability Focused User]
- Traceability: [Derived from review group H2]
- Acceptance Criteria: [Given the user launches the app When startup completes then the app shall load without crashing.]
- Notes: [Updated and revised from the  auto spec doc to remove any kind of vague wording such as gracefully and also match properly with the hybrid group]

# Requirement ID: FR_hybrid_4
- Description: [The system shall save user entries reliably after submission.]
- Source Persona: [Reliability Focused User]
- Traceability: [Derived from review group H2]
- Acceptance Criteria: [Given the user submits an entry When the app is reopened then the entry shall still be available.]
- Notes: [Added requirement to match with the hybrid group to allow for more testability.]

# Requirement ID: FR_hybrid_5
- Description: [The system shall clearly identify premium features before requiring payment.]
- Source Persona: [Budget Conscious User]
- Traceability: [Derived from review group H3]
- Acceptance Criteria: [Given a free user accesses a premium feature When the feature is displayed then it shall be labeled as premium.]
- Notes: [Used auto spec requirement and matched with the hybrid group]

# Requirement ID: FR_hybrid_6
- Description: [The system shall display subscription pricing information before payment.]
- Source Persona: [Budget Conscious User]
- Traceability: [Derived from review group H3]
- Acceptance Criteria: [Given a user views subscription options When the payment screen is displayed then pricing details shall be visible.]
- Notes: [Revised the spec auto requirement and modified to better suit the hybrid group]

# Requirement ID: FR_hybrid_7
- Description: [The system shall provide users with insights based on recorded mood data.]
- Source Persona: [Mental Health Support User]
- Traceability: [Derived from review group H4]
- Acceptance Criteria: [Given the user has recorded entries When insights are generated then at least one insight shall be shown.]
- Notes: [Modified requirement from the auto spec doc to remove ambiguous wording and to increase testability fo the feature.]

# Requirement ID: FR_hybrid_8
- Description: [The system shall provide users with access to resources and support for managing their mental health.]
- Source Persona: [Mental Health Support User]
- Traceability: [Derived from review group H4]
- Acceptance Criteria: [Given the user opens the support section When the page loads then support content shall be available.]
- Notes: [Reused same requirement from auto spec document but modified groups to match the hybrid group]

# Requirement ID: FR_hybrid_9
- Description: [The system shall present privacy and data-handling information before collecting user data.]
- Source Persona: [Trust seeking User]
- Traceability: [Derived from review group H5]
- Acceptance Criteria: [Given the user signs up When personal data is requested then privacy information shall be displayed.]
- Notes: [Modified requirement from the auto spec doc to make it more precise and less vague and also add some testable features in it.]

# Requirement ID: FR_hybrid_10
- Description: [The system shall provide accessible support options for users.]
- Source Persona: [Trust seeking User]
- Traceability: [Derived from review group H5]
- Acceptance Criteria: [Given the user opens support options When options are displayed then at least one support method shall be available.]
- Notes: [Modified and added more details to the reequirement to make sure it remains testable and matches the hybrid group.]