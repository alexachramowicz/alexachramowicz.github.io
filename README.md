# alexachramowicz.github.io

My personal static site!

## Local development

Requires Python 3.9 or newer; no packages need installing.
From the repository root, run `py -m http.server 8000` on Windows
(or `python3 -m http.server 8000` elsewhere). Open http://localhost:8000.
Stop the server with Ctrl+C.

## Validation before merging

Run `py -B -m unittest discover -s tests -v` (use `python3` elsewhere)
and `git diff --check` before pushing.
Tests check local HTML/CSS asset paths and filename casing, internal navigation,
unique IDs, and core page structure. They do not check visual layout, accessibility,
or availability of external websites.

Preview the site at desktop and phone widths and check navigation, project hover
descriptions, and keyboard access. Known accessibility gaps include missing image
alternative text and project links hidden until hover.

GitHub Actions runs the tests on pushes and pull requests into `main`.
After the first successful CI run, protect `main` in GitHub repository settings:
require a pull request, require the `Site regression checks` status check,
and require branches to be up to date before merging. Apply these requirements
to administrators too if you want to prevent bypassing checks.
Keep GitHub Pages configured to publish from `main`; feature branch pushes
then run validation without publishing the site. CI alone does not block merging
or deployment without the corresponding repository settings.

Credits:
"https://iconscout.com/illustrations/cash" Cash flow in dollar Illustration
