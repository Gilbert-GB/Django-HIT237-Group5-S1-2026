## Architecture Decision Record (ADR) for:
### _Authentication System Design (Login, Register, Logout, Auto Login)_

## Status
Accepted

## Last updated
2026-05-26

---

## Introduction

### Prologue (Summary):
In the Youth Justice NT web application, we implemented a Django-based authentication system to manage user access securely and efficiently. This includes user registration, login, logout, and automatic login after registration. The goal was to create a simple, user-friendly authentication flow while following Django’s built-in authentication framework and avoiding unnecessary complexity.

---

### Discussion (Context):
Before implementing authentication, the application had no control over user access. Anyone could access all pages without logging in, and there was no distinction between authenticated and anonymous users.

Problems identified:
- No user identity system (everyone accessed the system anonymously)
- No secure login/logout flow
- Users had to manually log in after registration
- Logout functionality caused HTTP 405 errors due to GET vs POST mismatch
- Navigation bar did not dynamically change based on authentication state
- No clear redirect flow after login or registration

These issues made the system insecure and not aligned with real-world government-style applications.

---

### Solutions (Decision):

**1. Django Authentication Framework**
We used Django’s built-in authentication system (`django.contrib.auth`) for:
- Login (`LoginView`)
- Logout (custom logout view used to fix HTTP 405 issue)
- Session management

This ensures security and reliability without reinventing authentication logic.

---

**2. Registration System (Custom View)**
We created a custom `RegisterForm` and `register_view`:
- Users are created using `form.save()`
- Passwords handled securely by Django User model
- Users are redirected after successful registration

---

**3. Auto Login After Registration**
To improve user experience, users are automatically logged in after registration using:

- `login(request, user)`

This removes the need to manually log in after signing up.

---

**4. Logout Implementation (Fix for HTTP 405 Error)**
The default `LogoutView` caused HTTP 405 errors because it expects a POST request, while the navbar used a GET request.

To fix this, a custom logout view was created:
- Calls `logout(request)`
- Redirects to login page
- Allows simple GET-based logout from navbar

---

**5. Authentication-Based Navigation**
Navbar uses:

- `user.is_authenticated`

This allows dynamic UI:
- Logged in → username + logout
- Logged out → login + register

---

**6. Redirect Flow**
Defined user flow:
- Login → dashboard/home
- Register → auto-login → dashboard/home
- Logout → login page

---

### Consequences (Results):

**Positive attributes:**
- Secure authentication using Django built-in system
- Improved UX with auto-login after registration
- Fixed HTTP 405 logout issue
- Cleaner navigation experience
- Consistent redirect flow
- Reduced complexity

---

**Negative attributes:**
- Custom logout bypasses Django’s recommended POST security pattern
- Authentication logic split between built-in and custom code
- Requires understanding of Django auth system
- Future scaling (roles/social login) may need refactoring

---

## Code References

```text
accounts/views.py
- register_view()
- logout_view() (custom)
- login() for auto login

accounts/urls.py
- LoginView
- Register URL
- Logout URL (custom)

templates/accounts/
- login.html
- register.html