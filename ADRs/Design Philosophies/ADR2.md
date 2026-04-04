## Architecture Decision Record (ADR) for:  
### _Design Philosophy : Less Code_

## Introduction

### Proluge (Summary):
Facing difficulty in managing large, complex code for our django-based web application, as a team of beginner-level developers we considered following django`s philosophy of writing **less code**. This will make development process much more quicker and efficient enhancing readability in our code, helping us achieve simplicity and less errors and bugs at the cost of reduced-control.

### Discussion:
Writing a project with large amount of code can be overwhelming for our team and it can be hard to debug any issues considering hard navigation throughout the large and complex code structure. Django helps in this regard through its built-in tools and functions that will help our team to minimize our code while ensuring core functionalities.  
Possible issues can be as follows:
- Writing many raw SQL queries to manage database is tough than simply using Django ORM
- Manually handling and coding forms is harder compared to usability of ModelForms

We, as a team, can prioritize and focus on understanding and enhancing the functionality of our application rather than coding complex components simply through use of this design philosophy.