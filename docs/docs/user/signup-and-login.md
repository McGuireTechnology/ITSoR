# Signup and Login Guide

This guide explains how to create an account and sign in to ITSoR from the frontend app.

## Before you begin

- Confirm the frontend is running (default: `http://127.0.0.1:5173` or `http://localhost:5173`).
- Confirm the backend API is running and reachable.

## Create an account (Signup)

1. Open the signup page: `/signup`.
2. Enter:
   - `Username`
   - `Email`
   - `Password`
3. Select **Signup**.

On success:

- Your account is created.
- You are signed in automatically.
- You are redirected to the users page (`/users`).

## Sign in (Login)

1. Open the login page: `/login`.
2. Enter:
   - `Username or Email`
   - `Password`
3. Select **Login**.

On success:

- You are signed in.
- You are redirected to the users page (`/users`).

## Switch between signup and login

- On **Login**, select **Signup** to create a new account.
- On **Signup**, select **Login** if you already have an account.

## Common issues

### "Invalid credentials"

- Verify username/email and password.
- Confirm the account exists.

### Signup fails

- Check whether the username or email is already in use.
- Verify backend is running and database migrations are applied.

### Cannot reach the page

- Confirm frontend server is running.
- Confirm you are using the correct URL and port.

## Related docs

- [User Guide](index.md)
- [Backend Auth Setup Guide](../developer/backend-auth-setup.md)
- [Frontend Auth Integration Guide](../developer/frontend-auth-integration.md)