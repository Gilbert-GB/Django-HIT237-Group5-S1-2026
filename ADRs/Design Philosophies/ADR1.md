## Architecture Decision Record (ADR) for:  
### _Design Philosophy : Quick Development_

## Introduction

### Proluge (Summary):
In the context of building a web app for NT youth diversion and support program, our team is facing time constraint to go with beginner-level experience in django projects, considering these circumstances we decided to go with Django`s philosopgy of **Quick Development**. This is help us achieve faster implementation for our project with fully-functional working features along with an appealing user interface design and effective customisation options.  
### Discussion:
The features to be developed in this web application are:
+ Searching programs
+ Filtering by location, age and type of crime
+ Allowing NGOs and organizations to manage listings

As new-to-django developer team, creating all these features from scratch will consume alot of time and increase difficulty overall. But according to this philosophy of django, the frameword already has alot of built-in features to fast track coding projects.

Using pre-built features from django helps reduce workload and add common components of our website quick and easy, this allows our team to focus on core functionality of our web app and conserving time and effort from adding low-level features on our app.

### Solutions (Decision):
Making use of this philosophy, we will:
- Use **Django`s Admin Panel** to manage all listings on the web app
- Using **Django`s Built-in Authentication** feature for user/organisation login activity
- Avoiding advanced or unnecessary features in projects (by reviewing client desireables)

This simple method allows our team to build a functional web application timely, ensuring all the important features are included without getting stuck with complex implementation issues in development process.

### Consequences (Results):
Postive attributes:
1. Quick and Easy development of application
2. Less effort required, higher funcationality ensured
3. Good learning curve for deveopment team, easy understanding and implementation

Negative attributes:
1. User interface might not be very complex
2. Customization options can be limited
3. Room for improvement in future versions

**This Data will be updated as the project development progresses.**