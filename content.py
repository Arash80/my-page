DEMO_POSTS = [
    {
        "title": "Building a Secure Flask Application",
        "subtitle": "A practical checklist for protecting users and avoiding common web vulnerabilities.",
        "img_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1400&q=80",
        "body": """
<p>Security is easiest to manage when it is part of the design rather than a final checklist. A Flask project does not need to be large before it handles valuable information: login sessions, email addresses, comments, and administrative actions all deserve protection.</p>

<h2>Keep configuration outside the source code</h2>
<p>Secret keys and database credentials should come from environment variables. Commit an <code>.env.example</code> file containing safe placeholders, but keep the real <code>.env</code> file out of Git. If a secret is ever committed, replace it immediately; deleting the line in a later commit does not remove it from Git history.</p>

<h2>Protect every state-changing request</h2>
<p>Creating, editing, deleting, and logging out should use POST requests. Pair those requests with CSRF tokens so another website cannot silently submit actions on behalf of a logged-in user. Authorization must also be checked inside each protected route rather than only hiding buttons in the interface.</p>

<h2>Treat user HTML as untrusted</h2>
<p>Rich-text editors produce HTML, but that does not make their output safe. Sanitize posts and comments on the server and sanitize legacy content again when it is displayed. Template escaping should remain enabled for ordinary text.</p>

<h2>Finish with repeatable tests</h2>
<p>Good security tests verify behavior: anonymous users cannot reach admin pages, regular users receive a forbidden response, delete actions reject GET requests, and script tags never appear in rendered comments. These tests protect the application during future upgrades.</p>
""",
    },
    {
        "title": "A Maintainable Structure for Small Python Projects",
        "subtitle": "Simple organization choices that make a project easier to test, explain, and extend.",
        "img_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1400&q=80",
        "body": """
<p>A small project benefits from structure, but it does not need dozens of folders. The goal is to make important responsibilities obvious: application behavior belongs in Python modules, presentation belongs in templates, configuration belongs in the environment, and verification belongs in tests.</p>

<h2>Keep one clear dependency source</h2>
<p>Choose one package-management workflow and document it. A project becomes confusing when an old lock file, an unrelated <code>package.json</code>, and a separate requirements file all describe different environments. New contributors should be able to install dependencies with one documented command.</p>

<h2>Separate data from version-controlled code</h2>
<p>Development databases, uploaded files, editor settings, virtual environments, and secrets should usually be ignored by Git. Provide sample configuration and deterministic seed content instead. This gives every developer a useful starting point without publishing private data.</p>

<h2>Write documentation for a first-time visitor</h2>
<p>A strong README answers four questions quickly: what does the project do, how is it installed, how is it run, and how is it tested? Screenshots and architecture details are helpful later, but reliable setup instructions provide the greatest immediate value.</p>

<h2>Automate the confidence checks</h2>
<p>Run tests in GitHub Actions on every push and pull request. Even a focused suite covering public pages, authentication, permissions, and CRUD operations gives maintainers confidence that refactoring did not change essential behavior.</p>
""",
    },
    {
        "title": "From Local Flask App to Production",
        "subtitle": "What changes when a development server becomes a real deployed service.",
        "img_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1400&q=80",
        "body": """
<p>Flask's development server is excellent for local work, but it is intentionally not a production server. Deployment means defining how the application starts, where configuration comes from, how data persists, and how failures are observed.</p>

<h2>Use a production WSGI server</h2>
<p>On a Linux host, Gunicorn can serve the Flask application with a command such as <code>gunicorn main:app</code>. The hosting platform should manage the process, restart it after failures, and send requests through HTTPS.</p>

<h2>Configure the environment on the host</h2>
<p>Production secrets should be created in the hosting provider's environment settings, never uploaded in an <code>.env</code> file. Debug mode must remain disabled. Secure cookies and HTTPS should be enabled wherever authentication is used.</p>

<h2>Plan for persistent data</h2>
<p>SQLite is convenient for local development, but many hosted applications use PostgreSQL for durable, concurrent access. Database migrations should describe schema changes so upgrades can be reviewed and applied without deleting existing records.</p>

<h2>Observe before optimizing</h2>
<p>Add structured logs, error reporting, health checks, and backups before worrying about advanced performance tuning. A modest application that reports failures clearly and restores data reliably is more production-ready than a fast application nobody can diagnose.</p>
""",
    },
]
