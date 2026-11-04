# Arash Golabi — Portfolio

A responsive static portfolio for applied AI, machine learning, backend engineering, research, robotics, and control-engineering work.

Website: [arash80.github.io/my-page](https://arash80.github.io/my-page/)

## Website files

The complete GitHub Pages site lives in [`docs/`](docs/):

### Pages

| File | Purpose |
| --- | --- |
| `index.html` | Portfolio homepage with featured work, project filters, research, publications, and contact details |
| `aegisops.html` | AegisOps Loan Risk case study: ML lifecycle, monitoring, and incident investigation |
| `techrag.html` | TechRAG Local case study: document retrieval, local generation, and evaluation |
| `workplaceops.html` | WorkplaceOps case study: backend architecture, authorization, and booking integrity |
| `fraud-platform.html` | Fraud ML Platform case study: temporal evaluation, uncertainty, and local/AWS implementation |
| `case-studies.html` | Project directory with expandable engineering and research notes; existing project anchors are preserved |
| `fraudscope.html` | FraudScope Agents case study |
| `resume.html` | Printable résumé with a Print / Save as PDF action |

### Shared styles, behavior, and assets

- `style.css` — shared visual system, navigation, homepage, legacy case-page layouts, and résumé print styles.
- `case-studies.css` — dedicated case-study pages, architecture diagrams, and the expandable project directory.
- `site.js` — mobile navigation, project filtering, opening case notes from URL fragments, and copying the contact email.
- `assets/favicon.svg` — site icon.
- `assets/aegisops-langgraph-workflow.svg` — published AegisOps investigation diagram.
- `.nojekyll` — serves the static files directly through GitHub Pages.

The existing `portfolio-filters.css` is retained for reference. Current pages use `style.css` for project-filter styling.

## Local preview

The site uses plain HTML, CSS, and JavaScript. No package installation or build step is required. With Python 3 available, run this command from the repository root:

```sh
python -m http.server 8000 --directory docs
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Use `python3` instead of `python` if that is the command available on your system. Stop the preview with `Ctrl+C`.

Open any page directly at the same address, for example [http://127.0.0.1:8000/aegisops.html](http://127.0.0.1:8000/aegisops.html). Project-directory URLs such as `case-studies.html#alignmentops` open the matching notes automatically.

## Deployment

GitHub Pages should be configured to publish the `docs` folder from the repository's default branch.

