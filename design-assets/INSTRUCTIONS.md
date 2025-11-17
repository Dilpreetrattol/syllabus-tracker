# Asset Drop Instructions

## Quick Start

1. **Drop your design images** in the appropriate folder under `/app/static/images/`:
   - Login/Register images → `/app/static/images/auth/`
   - Student dashboard images → `/app/static/images/student/`
   - Teacher dashboard images → `/app/static/images/teacher/`
   - HOD dashboard images → `/app/static/images/hod/`
   - Coordinator dashboard images → `/app/static/images/coordinator/`
   - Logos, icons, shared images → `/app/static/images/common/`

2. **Drop CSS files** in `/app/static/css/pages/`:
   - `auth.css` - Login/register styles
   - `student-portal.css` - Student portal (dashboard, subjects, detail)
   - (Other role-specific CSS files already created)

3. **Drop JavaScript files** in `/app/static/js/pages/`:
   - `auth.js` - Login/register interactions
   - `student-dashboard.js` - Student page interactions (will extend portal behaviors)
   - (Other role-specific JS files can be added)

## Design Files Checklist

When you're ready to integrate, provide:
- [ ] **Screenshots/mockups** of each page
- [ ] **Image assets** (backgrounds, icons, illustrations)
- [ ] **CSS files** or style specifications
- [ ] **JavaScript** (if any interactions needed)
- [ ] **Color palette** (hex codes)
- [ ] **Font specifications** (family, sizes, weights)

## File Naming

- Use lowercase with hyphens: `login-background.jpg`
- Be descriptive: `student-progress-icon.svg`
- Include size variants: `logo@2x.png` for retina

## Next Steps

Once you drop the files:
1. I'll integrate them into the appropriate templates
2. Update CSS references in `base.html` and page-specific blocks
3. Wire up any JavaScript interactions
4. Test responsive behavior
5. Optimize images if needed

## Current Status

✅ Folder structure created
✅ README files added to guide asset placement
✅ Placeholder CSS/JS files ready
⏳ Waiting for your design assets

**Simply drag and drop your files into the appropriate folders, then let me know!**
