# Code and Tool Implementation Description

## 1. Revised artefact

The implemented artefact is titled **Cybersecurity Awareness Questionnaire**. It is presented clearly as an academic questionnaire and research study. Participants are informed on the first page that they are contributing to research and that the application is not an instructional course or professional qualification. The application does not request names, email addresses or account registration details.

## 2. Participant information and informed consent

The `app.py` file creates the opening participant-information page. It explains the research purpose, activities, expected duration, voluntary participation, withdrawal arrangements, potential risks, confidentiality and research use of the responses. It identifies the researcher as **Amna Rashid**, the supervisor as **Dr. Maria Alvanou**, and the institution as the **University of Essex**. Participants must confirm informed consent and that they are aged 18 or above before continuing. An anonymous participant code is then generated automatically.

## 3. Questionnaire structure

The `1_Initial_Questionnaire.py` page records participants’ existing awareness and confidence. It contains Likert-scale questions about phishing, password security, social engineering, suspicious-message responses and multi-factor authentication. It also asks about confidence and exposure to suspicious communications.

The phishing, password-security and social-engineering pages provide interactive questionnaire sections. Participants respond to realistic cybersecurity situations and receive explanatory feedback. Section-completion information is recorded so that the application can control the order of the research process.

The `5_Knowledge_Assessment.py` page contains ten objective cybersecurity questions. It records the score, percentage and anonymised answers for research analysis. The `6_Final_Questionnaire.py` page records participants’ final perceptions of awareness, confidence, usability, clarity and usefulness. It also collects open-text suggestions and comments.

## 4. Database code

The `database.py` file creates four SQLite tables: `participants`, `questionnaire_responses`, `module_progress` and `quiz_results`. The participant table stores the anonymous code, broad demographic categories, consent status and completion time. The questionnaire table stores initial and final responses. The progress table stores completion of the interactive sections, while the results table stores knowledge-assessment scores and answer data. Directly identifying information is not collected.

The file also contains functions for creating participants, checking existing records, saving or updating questionnaire responses, recording section completion, saving assessment results, marking a study as complete and exporting table contents. Parameterised SQL queries are used to reduce the risk of SQL injection.

## 5. Researcher results and feedback

The `7_Researcher_Results.py` page provides restricted researcher access. The password is read from Streamlit Secrets or an environment variable and is not written directly into the public source code. Once access is granted, the researcher can view response counts and export anonymous participant data, questionnaire responses, assessment results and section-progress records as CSV files.

## 6. Converting the Python code into the web-based tool

The source code is converted into an interactive web application through Streamlit. First, Python processes the questionnaire logic, consent checks, answer validation, scoring and database operations. Streamlit converts commands such as `st.title`, `st.radio`, `st.form`, `st.button` and `st.text_area` into visible browser components. Each Python file inside the `pages` folder becomes a separate page in the application sidebar. SQLite provides local structured data storage, while session-state variables preserve the anonymous participant code during navigation.

To run the tool locally, Python 3.11 is installed, the project folder is opened in Visual Studio Code, and the required packages are installed using `pip install -r requirements.txt`. The command `streamlit run app.py` starts a local Streamlit server and opens the questionnaire in a web browser. For online use, the files can be uploaded to a GitHub repository and connected to Streamlit Community Cloud. The researcher password must then be added under the application’s Secrets settings before deployment.

## 7. Ethical alignment

The revised design applies data minimisation, informed consent and anonymous identification. It separates participant pages from the restricted researcher-results page. The wording, data-retention period, withdrawal procedure and contact details should remain consistent with the approved ethics documents before responses are collected.
