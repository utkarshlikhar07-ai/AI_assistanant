JARVIS AI — Frontend Assets Directory
======================================

Place static assets here:

- images/        : Logo images, icons, background textures
- icons/         : SVG icon files
- fonts/         : Custom font files (if self-hosted)
- audio/         : Sound effects for JARVIS voice feedback

The application uses emoji icons and inline SVG for most UI elements,
so no external image assets are strictly required for the base build.

If you add images, reference them from HTML/CSS as:
  /assets/images/your-image.png

Example usage in CSS:
  background-image: url('/assets/images/grid-bg.svg');
