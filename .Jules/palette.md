## 2024-05-22 - [Enhancing Drop Zone Accessibility]
**Learning:** Standard drag-and-drop zones often lack keyboard accessibility. Making the container focusable and handling keyboard events (Enter/Space) allows non-mouse users to trigger the file dialog.
**Action:** When creating custom interactive controls like drop zones, always add tabindex="0", role="button", and keydown handlers.
