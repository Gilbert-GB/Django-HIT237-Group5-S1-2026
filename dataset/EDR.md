## Entity Relationship Diagram (ERD) - Draft


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
