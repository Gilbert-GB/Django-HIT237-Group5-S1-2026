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

The system is centred around the **Program** entity, which represents youth diversion and support programs.

- A **User** can create programs and may be linked to an **Organisation**
- An **Organisation** manages multiple programs
- Programs can be either system-provided or user-generated (via the `source` attribute)

The **CrimeData** and **YouthJusticeData** entities store simplified external datasets used for dashboard insights. These are not directly related to programs but support data visualisation and analysis.