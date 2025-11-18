from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from urllib.parse import urlparse as url_parse
from .forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, ChangePasswordForm
from . import auth_bp
from app.services.email import send_email
from app.services.ratelimit import rate_limit
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit(limit=10, window_seconds=60)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        if not user.is_active:
            flash('Your account is inactive. Please contact admin.', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for(f'dashboard.{user.role}')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


def _get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@rate_limit(limit=5, window_seconds=120)
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        # Always show the same message to avoid enumeration
        flash('If an account with that email exists, a reset link has been sent.', 'info')
        if user:
            s = _get_serializer()
            token = s.dumps({'email': email}, salt='password-reset')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            # In development, log the link for convenience
            current_app.logger.info(f"Password reset link for {email}: {reset_url}")
            # Try to send email if configured
            try:
                send_email(
                    to_email=email,
                    subject="Reset your Syllabus Tracker password",
                    body_text=f"Click the link to reset your password: {reset_url}\nThis link expires in 1 hour.",
                    body_html=f"""
                        <p>We received a request to reset your password.</p>
                        <p><a href='{reset_url}'>Click here to reset your password</a></p>
                        <p>This link expires in 1 hour. If you didn't request this, you can ignore this email.</p>
                    """
                )
            except Exception:
                # already logged in send_email
                pass
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', title='Forgot Password', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    email = None
    try:
        s = _get_serializer()
        data = s.loads(token, max_age=3600, salt='password-reset')
        email = (data or {}).get('email')
    except (BadSignature, SignatureExpired):
        flash('The reset link is invalid or has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid reset request.', 'error')
            return redirect(url_for('auth.forgot_password'))
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset Password', form=form)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('auth.change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/change_password.html', title='Change Password', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            role='student',  # Default role for self-registration
            department=form.department.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
