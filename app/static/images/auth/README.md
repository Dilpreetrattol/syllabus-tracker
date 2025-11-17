# Images for Authentication Pages

Drop login and registration page images here:

- `login-bg.jpg` - Login page background
- `login-illustration.png` - Login page hero/illustration
- `register-bg.jpg` - Registration page background
- `register-illustration.png` - Registration page illustration
- `logo-auth.png` - Logo variant for auth pages
- `forgot-password-icon.svg` - Forgot password icon
- Any other auth-related visuals

These will be referenced in templates as:
```
{{ url_for('static', filename='images/auth/login-bg.jpg') }}
```
