## 2024-05-22 - [Enhancing Drop Zone Accessibility]
**Learning:** Standard drag-and-drop zones often lack keyboard accessibility. Making the container focusable and handling keyboard events (Enter/Space) allows non-mouse users to trigger the file dialog.
**Action:** When creating custom interactive controls like drop zones, always add tabindex="0", role="button", and keydown handlers.

## 2025-05-23 - [Icon-Only Button Accessibility]
**Learning:** Icon-only buttons are invisible to screen readers without proper labels. Adding `aria-label` provides necessary context, while `aria-hidden="true"` on the icon prevents redundant or confusing announcements.
**Action:** Always pair icon-only buttons with `aria-label="Action description"` and `title="Action description"`, and hide the icon itself from assistive technology.
