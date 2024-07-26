# Thoughts API

Welcome to the Thoughts API repository! Thoughts is a notes application built using Django Rest Framework. It provides features like email or username login, a custom email system with a custom domain to keep users updated on any changes to their account, and a forgot password functionality with encoded token.

## Features

- **Login**: Users can log in using either their email or username.
- **Email System**: Custom email system with a custom domain to keep users informed about any changes to their account.
- **Forgot Password**: Forgot password functionality with encoded token for secure password reset.

## Usage

### Authentication

To authenticate with the API, use either email or username along with the corresponding password.

### Email System

Thoughts provides a custom email system with a custom domain. Users will receive notifications about any changes to their account.

### Forgot Password

If a user forgets their password, they can reset it securely using the forgot password functionality. An encoded token will be sent to the user's email for verification.
