# Arash Golabi — Portfolio

A responsive static portfolio for applied AI, machine learning, research, robotics, and control-engineering work.

## Website files

The complete GitHub Pages site lives in [`docs/`](docs/):

- `index.html` — portfolio homepage
- `style.css` — shared layout and visual styling
- `portfolio-filters.css` — project category and filtering styles
- `case-studies.html` — detailed project and research case studies
- `resume.html` — printable résumé page
- `.nojekyll` — serves the static files directly through GitHub Pages

## Local preview

No application server or package installation is required. From the repository root, run:

```powershell
python -m http.server 8000 --directory docs
```

Then open `http://127.0.0.1:8000/`.

## Deployment

GitHub Pages should be configured to publish the `docs` folder from the repository's default branch.
