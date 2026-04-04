## Entity Relationship Diagram (ERD)

```mermaid
erDiagram

    USER ||--o{ ORGANISATION : owns
    ORGANISATION ||--o{ PROGRAM : manages
    USER ||--o{ PROGRAM : creates

    PROGRAM {
        int id
        string name
        string location
        string age_group
        string program_type
        string availability
        string source
    }

    ORGANISATION {
        int id
        string name
        string contact_info
    }

    USER {
        int id
        string username
        string email
    }

    CRIME_DATA {
        int id
        string offence_type
        string location
        date month
        int count
    }

    YOUTH_JUSTICE_DATA {
        int id
        string category
        string indigenous_status
        float value
        int year
    }

### ERD Explanation

The system is centred around the **Program** entity, which represents youth diversion and support programs.

- A **User** can create programs  
- An **Organisation** manages multiple programs  
- Programs can be either system-provided or user-generated (using the `source` field)  

The **CrimeData** and **YouthJusticeData** entities store simplified external data used for the dashboard. They are not directly linked to programs but support data visualisation and insights.