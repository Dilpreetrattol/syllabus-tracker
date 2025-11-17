# Design Assets Structure

This folder contains the organized structure for all design assets used in the Syllabus Tracker application.

## Directory Organization

### `/app/static/images/`
All image assets organized by user role and purpose:

#### **`/auth/`** - Authentication Pages
- Login page backgrounds, illustrations, logos
- Register page visuals
- Password reset imagery

#### **`/student/`** - Student Dashboard & Features
- Student-specific icons and illustrations
- Subject/course visuals
- Progress indicators
- Study materials icons

#### **`/teacher/`** - Teacher Dashboard & Features
- Teacher-specific icons
- Class management visuals
- Topic tracking imagery
- Resource upload icons

#### **`/hod/`** - Head of Department Dashboard
- Department analytics visuals
- Faculty management icons
- Reports and charts backgrounds
- Administrative icons

#### **`/coordinator/`** - Coordinator Dashboard
- Multi-department overview visuals
- System-wide analytics imagery
- Report generation icons
- Cross-department indicators

#### **`/common/`** - Shared Assets
- Logo variants (header, footer, favicon)
- Common UI icons (home, profile, settings, logout)
- Navigation elements
- Loading spinners, error illustrations
- Background patterns

### `/app/static/css/pages/`
Page-specific stylesheets:
- `auth.css` - Login/register styling
- `student-portal.css` - Student portal (dashboard, subjects, detail)
- `teacher-dashboard.css` - Teacher-specific styles
- `hod-dashboard.css` - HOD-specific styles
- `coordinator-dashboard.css` - Coordinator-specific styles

### `/app/static/js/pages/`
Page-specific JavaScript:
- `auth.js` - Login/register interactions
- `student-dashboard.js` - Student dashboard functionality
- `teacher-dashboard.js` - Teacher dashboard functionality
- Charts, interactions, AJAX calls

## How to Use in Templates

### Images
```jinja2
<!-- Common logo -->
<img src="{{ url_for('static', filename='images/common/logo.png') }}" alt="Logo">

<!-- Student dashboard icon -->
<img src="{{ url_for('static', filename='images/student/progress-icon.png') }}" alt="Progress">

<!-- Auth background -->
<div style="background-image: url({{ url_for('static', filename='images/auth/login-bg.jpg') }})">
```

### CSS
```jinja2
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/student-portal.css') }}">
{% endblock %}
```

### JavaScript
```jinja2
{% block scripts %}
<script src="{{ url_for('static', filename='js/pages/student-dashboard.js') }}"></script>
{% endblock %}
```

## File Naming Conventions

- Use lowercase with hyphens: `progress-chart-bg.png`
- Be descriptive: `student-profile-placeholder.jpg`
- Include role prefix for role-specific assets: `student-course-card-bg.png`
- Use consistent formats:
  - `.png` for icons, logos, transparent graphics
  - `.jpg` for photos, backgrounds
  - `.svg` for scalable vector graphics (preferred for icons)
  - `.webp` for optimized web images

## Image Size Guidelines

- **Icons**: 24x24, 32x32, 48x48, 64x64 px
- **Logos**: 
  - Header: 180x60 px
  - Footer: 120x40 px
  - Favicon: 32x32, 64x64 px
- **Backgrounds**: 1920x1080 px (Full HD)
- **Cards/Thumbnails**: 400x300 px
- **Profile images**: 200x200 px (square)

## Optimization Tips

1. Compress images before uploading (use TinyPNG, ImageOptim)
2. Use responsive images with `srcset` for different screen sizes
3. Lazy-load images below the fold
4. Prefer SVG for icons and simple graphics
5. Use CSS sprites for small repeated icons

## Current Page Designs Needed

- [x] Login page
- [x] Register page  
- [x] Student dashboard
- [ ] Teacher dashboard
- [ ] HOD dashboard
- [ ] Coordinator dashboard
- [ ] Subject detail view
- [ ] Topic management
- [ ] Progress tracking
- [ ] Reports

## Design Handoff Checklist

When dropping design files:
1. ✅ Export all images in correct formats
2. ✅ Include @2x versions for retina displays
3. ✅ Provide color palette (hex codes)
4. ✅ Include font specifications
5. ✅ Export CSS/SCSS if available
6. ✅ Document interactive states (hover, active, disabled)
7. ✅ Include responsive breakpoints
8. ✅ Provide icon sprite sheets if applicable

## Support

For questions about asset integration, contact the development team or refer to the main README.md in the project root.
