# CSI2113 — Containerized Web Application with CI/CD

A small Flask task-tracker app, containerised with Docker, deployed via a full
GitHub Actions CI/CD pipeline to Docker Hub and back down to a local machine.

## Architecture

```
Develop (Flask app) → Git/GitHub → GitHub Actions
    → Build & Test (pytest) → Build Docker Image
    → Push to Docker Hub → Deploy to local computer (self-hosted runner)
```

## Project structure

```
webapp/
├── app.py                  # Flask application
├── templates/index.html    # UI
├── static/style.css        # Styling
├── tests/test_app.py       # pytest test suite
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── .github/workflows/ci-cd.yml   # CI/CD pipeline
```

---

## Step-by-step setup (do this before the viva)

### 1. Push to GitHub
```bash
cd webapp
git init
git add .
git commit -m "Initial commit: Flask task tracker with Docker + CI/CD"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
Make a few more commits as you go (e.g. after adding tests, after adding the
workflow) — "meaningful commits" is part of the Git/GitHub marks.

### 2. Create a Docker Hub account & access token
1. Sign up at hub.docker.com if you don't have an account.
2. Go to **Account Settings → Security → New Access Token**, generate one, copy it.

### 3. Add GitHub Actions secrets
In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**
- `DOCKERHUB_USERNAME` = your Docker Hub username
- `DOCKERHUB_TOKEN` = the access token from step 2

### 4. Set up a self-hosted runner (this is what makes "Deploy to Local Computer" real)
GitHub's cloud runners can't reach your machine, so the deploy step needs a
runner that lives on your computer.

In your repo: **Settings → Actions → Runners → New self-hosted runner**, then
follow GitHub's shown commands, roughly:
```bash
mkdir actions-runner && cd actions-runner
# (copy the exact download/config commands GitHub shows you — they include a token)
./config.sh --url https://github.com/<you>/<repo> --token <RUNNER_TOKEN>
./run.sh
```
Leave that terminal running (or install it as a service) — it's what listens
for the `deploy` job and runs it locally, using your machine's Docker.

### 5. Push and watch it run
```bash
git push
```
Go to the **Actions** tab on GitHub and watch the three jobs run in order:
`build-and-test` → `build-and-push` → `deploy`.

### 6. Confirm it's live
```bash
docker ps
curl http://localhost:5000/api/health
```
Open http://localhost:5000 in a browser.

---

## Running it manually (without CI, for local dev)

```bash
docker compose up --build
```
Visit http://localhost:5000

## Running tests manually

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## Viva demonstration checklist

Walk the assessor through the pipeline in this order:

1. **Show the app running** at `http://localhost:5000` — add/complete/delete a task.
2. **Show the code** — `app.py`, `tests/test_app.py`, `Dockerfile`.
3. **Show GitHub** — commit history (Git/GitHub marks), and the repo structure.
4. **Make a small change** (e.g. edit a string in `index.html`), commit, push.
5. **Show the Actions tab live** — the three jobs running: test → build & push → deploy.
6. **Show Docker Hub** — the new image tag just pushed (`latest` and the commit SHA).
7. **Show the local container updating** — `docker ps`, and the app in the
   browser reflecting your change after the deploy job finishes.
8. **Explain each YAML section** in `ci-cd.yml` briefly if asked — what each job does and why it depends on the previous one (`needs:`).

This demonstrates every required stage end-to-end, live.
