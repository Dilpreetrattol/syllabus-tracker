# Common/Shared Images

Drop shared assets used across all pages here:

## Logos
- `logo-main.png` - Primary logo (header)
- `logo-footer.png` - Footer logo variant
- `logo-white.png` - White/light version for dark backgrounds
- `favicon.ico` - Browser favicon
- `favicon-32x32.png` - High-res favicon
- `logo-icon.svg` - Icon-only logo variant

## Navigation & UI Icons
- `home-icon.svg`
- `profile-icon.svg`
- `settings-icon.svg`
- `logout-icon.svg`
- `menu-icon.svg`
- `close-icon.svg`
- `search-icon.svg`
- `notification-icon.svg`

## Status & Feedback
- `loading-spinner.svg`
- `success-checkmark.svg`
- `error-icon.svg`
- `warning-icon.svg`
- `info-icon.svg`

## Placeholders
- `avatar-placeholder.png` - Default user avatar
- `image-placeholder.svg` - Generic image placeholder
- `no-data-illustration.svg` - Empty state illustration

## Background Patterns
- `pattern-light.png` - Light background pattern
- `pattern-dark.png` - Dark background pattern

Reference in templates:
```
{{ url_for('static', filename='images/common/logo-main.png') }}
```
