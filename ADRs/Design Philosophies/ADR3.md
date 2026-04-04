## Architecture Decision Record (ADR) for:  
### _Design Philosophy : Separate Logic from Presentation_

## Introduction

### Proluge (Summary):
I any web application/website development process, developers often try to separate backend logic from frontend display, using django`s design philosophy of **Separate Logic from Presentation** we can develop a clean and manageable code structure for our project, accepting it requires us to learn the Django templates.

### Discussion (Context):
In web development, we need to make sure to avoid mixing business logic (Python Code) with presentation (HTML, CSS and Javascript) so that our code is not difficult to read and maintain.

Django demands we:
- Keep logic code inside separate **Python Files**
- Keep presentation code inside templates

If we don`t have this approach and both logic and presentation is mixed then:
- Code becomes messy and hard to read
- Difficulty in debugging errors
- Updating GUI can be tough for future versions of application

### Solutions (Decision):
Using this design philosophy, we will:
- Write all logic code inside models and views files
- Use templates for only frontend display
- Avoid writing any logic code inside HTML files
- Pass data from views to templates using consistent variables

For example:
- Views file handles filtering programs
- Template will only display the filtered results we got from our backend
