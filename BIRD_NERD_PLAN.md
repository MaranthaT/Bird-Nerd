# Bird Nerd: Portfolio Plan

Two parts: **Part 1, the Plan** (the checklist for all 10 weeks) and **Part 2, the Weeks 1–3 guide** (step-by-step lessons for the Python service).

Confidence tags: **[certain]** = backed by a source, **[likely]** = strong inference, **[guessing]** = estimate.

---

# Part 1: The Plan

## Overview

Build **Bird Nerd**: you record a bird on your phone, a Python API identifies it, an AI agent checks it against real eBird sightings, and you confirm it. **You write the code; Claude teaches.** About 10 weeks at 10–12 hours a week, on a Mac. Start applying after week 7. Cost: a one-time $5 Anthropic API credit purchase (you'll likely use $1–3 of it), with your existing Claude plan for learning; everything else is free.

**The goal is two things:** a portfolio project you can honestly say you built, and a reusable playbook so your next project goes faster.

## How you'll learn

**The loop for every step:**

1. **Learn:** read the linked material, then answer the step's question in your own words in `LEARNING_LOG.md`.
2. **Plan:** write 3–5 lines describing what you'll build before writing code.
3. **Build:** type the code yourself.
4. **Check:** the step's **Check** must be true.
5. **Reflect:** two lines in `LEARNING_LOG.md`: what I learned, and what I'd do differently next time.

**Make Claude Code a tutor, not a builder.** Create a `CLAUDE.md` file in your repo root with this text. Claude Code reads it automatically.

```
# How to help me
I'm learning to build this project myself.
- Do not write or edit code in my files unless I say "write it".
- Explain concepts and compare them to JavaScript, which I know well.
- When I'm stuck, give the smallest useful hint first. Give more only if I ask.
- When I ask for a review, point out problems and ask me questions; let me fix them.
- Before I move on from a step, quiz me with 2 questions about what I built.
```

**The 45-minute rule:** stuck for 45 minutes, ask Claude for a hint. Still stuck after 3 hints, open the answer key (the starter kit), read the relevant part, then **close it and write your version from memory**.

**Rebuild from memory:** at the end of each phase, rebuild its core piece in an empty folder without notes. Whatever you can't rebuild is what to study next.

**Keep a playbook:** `PLAYBOOK.md` collects reusable patterns (for example, "wrap an ML model in an API"). Each entry: when to use it, the steps, and the gotchas you hit. This is what makes your next project faster.

## Timeline

| Phase | Weeks | Focus |
| --- | --- | --- |
| Setup | Week 0 | Keys and tools |
| Listen API | Weeks 1–3 | Learn Python, build the service |
| Bird Nerd app | Weeks 4–7 | Agent + portfolio site v1 |
| **Gate: Bird Nerd live** | End of week 7 | **Start applying every week from here** |
| Real users | Weeks 8–9 | 10+ birders |
| Finish | Week 10 | Playbook + polish |

## Week 0: Setup

- [x] Install Node.js LTS, uv and Docker. **Check:** all three run in your terminal.
- [x] Create free accounts: GitHub, Vercel, Neon and Langfuse. Make sure Claude Code is signed in with your Claude plan. **Check:** you can sign in to each.
- [x] Set up Clerk (sign-in for your app):
  - Sign up at [dashboard.clerk.com/sign-up](https://dashboard.clerk.com/sign-up) with your GitHub account.
  - Create an application named **Bird Nerd**. Choose **Consumer** (not B2B). Turn on **Email** and **Google** sign-in.
  - Open **API keys** and copy the Publishable Key and Secret Key into your password manager right away. The Secret Key is shown only once; if you lose it, create a new one on the same page.
  - **Check:** both keys are saved.
- [x] Set up the Anthropic API (billed separately from your Claude subscription):
  - At [console.anthropic.com](https://console.anthropic.com), go to **Billing** → **Buy credits** and buy $5, the minimum. Leave **auto-reload off**, so you can never spend more than you loaded.
  - Go to **API keys** → **Create Key**, name it `bird-nerd`, and copy it into your password manager. It's shown only once.
  - **Check:** the credit balance shows $5 and the key is saved.
- [x] Get free API keys: eBird (create a free eBird account, then request a key at ebird.org/api/keygen) and xeno-canto (register, verify your email, then copy the key from your account page). **Check:** both saved in a password manager.
- [x] Create repo `bird-nerd` with folders `listen-api/` and `web/`, a `.gitignore` listing `.env*`, and a `BUILD_LOG.md`. **Check:** `git status` shows no env files.
- [x] Interview 5 birders about how they identify birds. **Check:** a one-page summary naming their #1 problem.

## Weeks 1–3: Python Listen API

Detailed lessons, specs, hints and Mac commands: see **Part 2: Weeks 1–3 guide** below.

- [ ] **Python foundations.** Learn types, functions, modules and virtual environments. Build two small functions and their tests yourself. **Check:** all your tests pass.
- [ ] **Run BirdNET.** Learn how a sound model scores audio in 3-second chunks. Build a script that prints the top 3 species for your own clip. **Check:** it prints species and confidence scores.
- [ ] **Build the API.** Learn file uploads, FastAPI dependencies and HTTP status codes. Build `/health` and `/identify` with an API-key check and input limits. **Check:** every error case returns the right status code.
- [ ] **Write tests.** Learn why most tests use a fake model. **Check:** at least 8 tests pass and the linter is clean.
- [ ] **Measure accuracy.** Learn top-1 versus top-3 accuracy. Build a script that scores 100 labeled xeno-canto recordings. **Check:** a results summary, plus one sentence on what surprised you.
- [ ] **Deploy.** Learn what containers are and what Cloud Run does on a cold start. Write the Dockerfile yourself, run it on your Mac, then deploy. **Check:** a request with the key works on the live URL; without it you get 401.
- [ ] **Lock it in.** Rebuild `/identify` from memory in 60 minutes, write a decision note, and add 2 playbook entries. **Check:** your gaps are listed in `LEARNING_LOG.md`.

## Weeks 4–7: Bird Nerd app and agent (TypeScript)

You know this stack, so the learning focus is the AI parts. Write a short plan before each step.

- [ ] **Set up the app.** Next.js, Clerk sign-in, Neon + Drizzle. Sketch the data model on paper first (recordings, entries, entry events, agent runs). **Check:** you can sign in to an empty journal.
- [ ] **Record on the phone.** Learn the browser's `MediaRecorder` and permission prompts. Send the clip through your server to the Listen API, then delete it, with a "Warming up…" message and one retry. **Check:** a real bird gets identified on your phone.
- [ ] **eBird client.** Learn rate limits and caching. Build lookups for nearby sightings (50 km, 30 days) cached for 6 hours. **Check:** tests with mocked responses pass.
- [ ] **Learn agents before building one.** Read the [AI SDK Agents docs](https://ai-sdk.dev/docs/agents/overview). On paper, trace one tool-calling loop: what the model asks for, what your code returns, when it stops. **Check:** you can draw the loop from memory.
- [ ] **Build the agent in small steps.** First one tool, then all three. Use `claude-haiku-5-5`, at most 6 steps. Your code sets the verdict from eBird counts and keeps whichever is more cautious; skip the AI call when the bird is common and BirdNET is confident. **Check:** 10 real clips get sensible verdicts and you can explain every line.
- [ ] **Review screen.** Confirm / Correct / Reject; "Unusual" needs a note, enforced on the server; every action logged; a life list. **Check:** confirming an unusual bird without a note fails.
- [ ] **Tracing, cost and caps.** Learn what tokens and prompt caching are. Add Langfuse tracing, cost per result and daily caps. **Check:** runs appear in Langfuse and you can explain what one costs.
- [ ] **Evals in CI.** Learn what evals are and the weaknesses of AI grading. Write 10 test cases by hand before growing to 40. A GitHub Action blocks a merge if the pass rate drops more than 5 points; mocked AI responses for everyday tests. **Check:** a deliberately weakened prompt fails the check.
- [ ] **Deploy and lock it in.** Deploy to Vercel and publish your portfolio at `yourname.vercel.app`. Rebuild a one-tool agent from memory in 60 minutes; add playbook entries for agents with guardrails and evals in CI. **Check:** a friend can sign up and confirm a sighting.
- [ ] **Gate:** start applying, and recruit 10 testers (Audubon chapters, birding clubs, r/birding). **Check:** 10 sign-ups.

## Weeks 8–9: Real users

- [ ] **Privacy:** private by default, sensitive-species locations hidden, a working "Delete my data" button. **Check:** a test account's data is fully deleted.
- [ ] **Feedback:** a feedback button and an admin page with usage counts. **Check:** you can see real numbers.
- [ ] **Two-week test:** compare how often users correct the AI with your lab accuracy. **Check:** you've listed the top 3 problems.
- [ ] **Fix and write up:** fix the top 3 and publish "What [N] birders taught me." **Check:** the post is live.

## Week 10: Finish

- [ ] README: one-line pitch, live link, demo video, accuracy and eval numbers, BirdNET non-commercial license note.
- [ ] Case study with real numbers, plus a post: "Learning Python as a JavaScript developer."
- [ ] `PLAYBOOK.md` has at least 5 patterns. Test it: sketch a plan for a similar project (for example, a plant or flower identifier) using only the playbook.
- [ ] CI is green, there are no secrets in git, and you can give a 2-minute walkthrough out loud.

## Job search (from week 7)

- Apply every week; ask 3 former coworkers for referrals first.
- Spend about 3 hours a week on interview practice.
- For PM and TPM roles: keep three resume versions, write two case studies from your current job, and keep a `RISKS.md` plus a weekly 5-line status note.

---

# Part 2: Weeks 1–3 guide — Learn to build the Listen API

By the end of week 3 you'll have written a Python web service that identifies birds from recordings, with tests, an accuracy report and a live URL, and you'll understand every line because you wrote it.

**How each part works:**

- **Goal:** what you'll be able to do afterwards.
- **Learn:** what to read, plus a question to answer in `LEARNING_LOG.md` before you build.
- **Build:** a description of what your code must do. You write the code.
- **Hints:** open only when you're stuck (the 45-minute rule).
- **Check:** you're done when this is true.
- **Compare:** after the Check passes, compare with the answer key and write one difference in your log.

**The answer key** is the starter kit (`bird-nerd-listen-api-starter.zip`) from the chat. Keep it in a folder outside your repo and don't open a file until you've finished that part yourself.

**All commands are for a Mac**, run in Terminal.

## Part A: Python foundations (week 1, about 5 hours)

**Goal:** write small typed Python functions and their tests without help.

**Learn:**

- In Claude chat: *"I'm a JavaScript and Node developer with 5 years of experience. Give me a one-page Python cheat sheet comparing: npm vs uv, package.json vs pyproject.toml, TypeScript types vs Python type hints, Zod vs Pydantic, Express vs FastAPI, Vitest vs pytest, and async/await."*
- The official [Python tutorial](https://docs.python.org/3/tutorial/), sections 3–6 (skim what you already know from JavaScript).
- **Answer in your log:** What does a virtual environment do, and what's the closest thing to it in Node?

**Build:**

1. Install uv: `brew install uv`, then close and reopen Terminal.
2. Outside your repo, create a practice project:
   ```
   uv init python-practice --python 3.12
   cd python-practice
   uv add --dev pytest
   ```
3. In `practice.py`, write `count_birds(sightings: list[str]) -> dict[str, int]`, which counts how often each name appears, and `top_birds(counts: dict[str, int], n: int) -> list[str]`, which returns the `n` most common names.
4. In `test_practice.py`, write 3 tests for each: an empty input, one item, and repeats.

**Hints:**

- `counts.get(name, 0) + 1` adds to a count that may not exist yet.
- `sorted(counts, key=counts.get, reverse=True)` sorts names by their count.
- Python has `collections.Counter`, which does this for you. Write it by hand first, then try `Counter` and compare.

**Check:** `uv run pytest` shows all 6 of your tests passing.

## Part B: Set up the project (week 1, about 1 hour)

**Goal:** a Python project inside your repo with every library installed.

1. Install ffmpeg, which converts phone recordings into a format BirdNET reads: `brew install ffmpeg`
2. Check your chip: run `uname -m`. `arm64` means Apple Silicon and you're set. `x86_64` means an Intel Mac; see Troubleshooting before Part C.
3. Create the project in your repo:
   ```
   cd bird-nerd
   uv init listen-api --python 3.12
   cd listen-api
   uv add birdnet fastapi "uvicorn[standard]" python-multipart
   uv add --dev pytest httpx ruff
   ```
   If uv created a sample `main.py` or `hello.py`, delete it. Create empty folders `app`, `tests`, `eval` and `samples`, and an empty file `app/__init__.py`.
4. Add to the bottom of `pyproject.toml`, so pytest can find your code:
   ```
   [tool.pytest.ini_options]
   pythonpath = ["."]
   ```
5. Add to your repo's root `.gitignore`:
   ```
   listen-api/.venv/
   listen-api/samples/
   listen-api/eval/audio/
   __pycache__/
   ```
6. Make sure the tutor-mode `CLAUDE.md` from Part 1 is in your repo root.
7. **Answer in your log:** What did each `uv add` line install, and why are pytest, httpx and ruff "dev" dependencies?

**Check:** `uv run python -c "import birdnet, fastapi; print('ok')"` prints `ok`.

## Part C: Run BirdNET yourself (week 1, about 4 hours)

**Goal:** turn any recording into a ranked list of likely species.

**Learn:**

- The "Example usage" section of the [birdnet README](https://github.com/birdnet-team/birdnet).
- **Answer in your log:** BirdNET scores audio in 3-second chunks. Why can one recording produce several different species? And why might a location filter help?

**Get recordings:** record 3 clips on your phone, 20–30 seconds each, of birds you or a birder friend can identify. Save them in `samples/` as `clip1`, `clip2` and `clip3`, keeping the phone's extension (for example `clip1.m4a`).

**Build** `app/birds.py` with:

1. `to_wav(src, dst)`: converts any audio file to a mono, 48 kHz WAV of at most the first 60 seconds, using ffmpeg.
2. `identify(path)`: returns detections sorted by confidence, highest first, ignoring anything under 0.25. Each detection has a common name, scientific name, confidence, start second and end second.
3. A location filter: `identify(path, lat, lon, day)` also drops species BirdNET's location model scores below 0.03 for that place and week.
4. Try it on your clips with and without the location filter, from a short script or the Python prompt (`uv run python`).

**Hints:**

- Loading the models: `birdnet.load("acoustic", "2.4", "tf", library="litert")` and `birdnet.load("geo", "2.4", "tf", library="litert")`. The first call downloads the model, so allow a minute.
- Results have a `.to_csv(path)` method. Writing to a temporary file and reading it with `csv.DictReader` is the simplest reliable way to read them.
- Result columns: `species_name` looks like `Turdus migratorius_American Robin`, and `start_time` looks like `00:00:03.00`.
- The location model takes a week from 1 to 48: four per month.
- ffmpeg options: `-ac 1` (mono), `-ar 48000` (sample rate), `-t 60` (first 60 seconds). Run it with `subprocess.run(..., check=True)`.
- `@functools.lru_cache` on a function that loads a model makes it load only once.
- A `@dataclass` is Python's quick way to define a typed record, like a TypeScript interface with a constructor.

**Check:** your clips print species and confidence scores, and your log says whether the location filter changed the results.

**Compare** with `app/birds.py` in the answer key.

## Part D: Build the API (week 2, about 5 hours)

**Goal:** a web API that other code can call, with input checks and an API key.

**Learn:**

- The [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) pages: First Steps, Request Files, Request Forms and Files, Header Parameters, Dependencies, and Handling Errors.
- **Answer in your log:** Why check the API key in a dependency instead of inside the endpoint? What's the Express equivalent?

**Build** `app/main.py` to this spec:

| Rule | Response |
| --- | --- |
| `GET /health` | 200 with `{"status": "ok"}` |
| `POST /identify` takes a file field `audio` (required) and form fields `lat` (−90 to 90), `lon` (−180 to 180) and `recorded_on` (a date), all optional | 200 with `detections`, `model`, `location_filter` (true only when all three are given) and `processing_ms` |
| The `X-API-Key` header doesn't match the `LISTEN_API_KEY` environment variable | 401 |
| The file is empty | 400 |
| The file is over 10 MB | 413 |
| ffmpeg can't read the file | 415 |
| `lat` or `lon` is out of range | 422 (FastAPI does this for you) |

**Hints:**

- You'll use `Header()`, `File()`, `Form(ge=..., le=...)`, `Depends()` and `HTTPException` from FastAPI.
- Define `/identify` with `def`, not `async def`. BirdNET's work blocks, and FastAPI runs plain `def` endpoints in a thread so the server stays responsive.
- `audio.file.read(MAX_BYTES + 1)` lets you detect an oversized file without reading all of it.
- Return the identifier function from a small dependency (for example `get_identifier()`). That makes Part E much easier.

**Try it:**

```
export LISTEN_API_KEY=dev-key-123
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`, click **POST /identify** → **Try it out**, and test every row of the spec on purpose.

**Check:** every row of the spec returns the status code it should.

**Compare** with `app/main.py` in the answer key.

## Part E: Tests (week 2, about 4 hours)

**Goal:** tests that prove your API follows its spec, and run in seconds.

**Learn:**

- The [pytest getting started guide](https://docs.pytest.org/en/stable/getting-started.html), plus fixtures and `parametrize`.
- FastAPI's "Testing" and "Testing Dependencies with Overrides" pages.
- **Answer in your log:** Why should most tests not run the real BirdNET model? What would go wrong in CI if they did?

**Build:**

1. `tests/test_api.py`: at least one test per row of Part D's spec (8 or more), using a fake identifier instead of BirdNET.
2. `tests/test_real_model.py`: checks that each of your 3 clips has the right bird in its top 3, and skips any clip file that's missing.

**Hints:** `TestClient(app)`, `app.dependency_overrides[get_identifier] = ...`, `monkeypatch.setenv(...)`, and `pytest.skip(...)`.

**Check:** `uv run pytest` passes and `uv run ruff check .` prints `All checks passed!`

**Compare** with the `tests` folder in the answer key.

## Part F: Measure accuracy (week 3, about 4 hours)

**Goal:** an honest number for how often BirdNET is right, which you can quote in interviews.

**Learn:**

- Ask Claude: *"Explain top-1 and top-3 accuracy, and why test data should be separate from the data a model learned from."*
- **Answer in your log:** If top-3 accuracy is high but top-1 is low, what does that mean for Bird Nerd's review screen?

**Build** `eval/run_eval.py` that:

1. Takes a list of 20 birds common where you live.
2. Fetches 5 quality-A recordings of each from xeno-canto, caching the audio in `eval/audio/`, and waits 1 second between requests.
3. Runs each recording through `identify` with and without the location filter.
4. Writes `eval/results/recordings.csv`, `eval/results/summary.json` (top-1 and top-3, with and without location, plus per species) and `eval/results/credits.csv` (recordist and license for each recording).

**Hints:**

- Search URL: `https://xeno-canto.org/api/3/recordings?query=...&key=YOUR_KEY`, with a query like `en:"American Robin" q:A cnt:"United States"`.
- Useful fields on each recording: `id`, `file` (the download link), `lat`, `lon`, `date`, `rec`, `lic` and `url`.
- Python's built-in `urllib.request` can fetch and download without extra libraries.
- Read your key from an environment variable: `export XENO_CANTO_API_KEY=your-key`, then `os.environ["XENO_CANTO_API_KEY"]`.
- Run it with `uv run python -m eval.run_eval`. [guessing] The first run takes 20–40 minutes.

**Check:** `summary.json` exists, and your build log has the numbers plus one sentence on what surprised you. Commit `eval/results/`, but never `eval/audio/`: [certain] each recording has its own license, often non-commercial.

**Compare** with `eval/run_eval.py` in the answer key.

## Part G: Containerize and deploy (week 3, about 5 hours)

**Goal:** your API running at a public URL, and an understanding of what happens when a request arrives.

**Learn:**

- Docker's [getting started guide](https://docs.docker.com/get-started/): images, containers and layers.
- **Answer in your log:** When a request reaches Cloud Run and no copy of your service is running, what happens step by step, and why does that take time?

**Build a Dockerfile** that:

1. Starts from `python:3.12-slim`.
2. Installs `ffmpeg` and `libsndfile1` with apt.
3. Installs uv and your dependencies from `pyproject.toml` and `uv.lock`, without dev tools.
4. Copies in `app/`.
5. Downloads the BirdNET models during the build, so the first request doesn't have to.
6. Starts uvicorn on the port in the `PORT` environment variable (default 8080).

Also write a `.dockerignore` that keeps out `.venv`, `samples`, `eval`, `tests` and any `.env` files.

**Hints:**

- `COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv` gets uv into the image.
- `uv sync --frozen --no-dev --no-install-project` installs exactly what's in your lock file.
- Setting `BIRDNET_APP_DATA=/srv/models` tells birdnet where to store downloaded models.
- Copy `pyproject.toml` and `uv.lock` before your code: Docker then reuses the slow install step when only your code changes.

**Test it on your Mac first** (with Docker Desktop running):

```
docker build -t listen-api .
docker run -p 8080:8080 -e LISTEN_API_KEY=dev-key-123 listen-api
```

In a second Terminal window: `curl http://localhost:8080/health`

**Deploy:**

1. Sign up for the Google Cloud free trial now, not earlier, because its 90-day clock starts at signup:
   - Go to [cloud.google.com/free](https://cloud.google.com/free) → **Get started for free** → sign in with Google → choose your country, accept the terms, pick **Individual** → enter a card → **Start free**. The card only verifies your identity: you aren't billed during the trial, and a small temporary charge may appear and then be reversed.
   - **Create a project:** project picker at the top → **New project** → name it `bird-nerd` → **Create**. [likely] Google may add numbers to the ID; use whatever it gives you.
   - **Set a $1 budget alert:** menu (☰) → **Billing** → **Budgets & alerts** → **Create budget** → name it `bird-nerd-budget`, leave all projects and services selected → **Specified amount**: $1 → keep the 50%, 90% and 100% thresholds and email alerts → if you see **Spend cap enforcement**, turn it on → **Finish**. A plain budget only emails you; it doesn't stop charges.
   - **Set a calendar reminder for day 80 of the trial** to decide whether to upgrade so your demo stays online. After 90 days Google stops the service and doesn't charge you unless you upgrade. Until then, don't click **Upgrade** or **Activate full account**.
2. Install the Google Cloud CLI using the macOS instructions at [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install), then run `gcloud init`, sign in, and choose your `bird-nerd` project.
3. Make a strong key and save it in your password manager as "Listen API key": `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
4. From inside `listen-api`, deploy:
   ```
   gcloud run deploy listen-api --source . --region us-central1 --memory 2Gi --min-instances 0 --max-instances 2 --timeout 120 --allow-unauthenticated --set-env-vars LISTEN_API_KEY=PASTE_YOUR_KEY
   ```
   Before running it, **write in your log what each flag does**. Short version: `--source .` builds your Dockerfile on Google's servers; `--region us-central1` is a free-tier region; `--memory 2Gi` gives room for the model; `--min-instances 0` lets it shut down when idle (free); `--max-instances 2` caps costs; `--allow-unauthenticated` lets requests reach your code, where your API key check protects it. Answer **y** to prompts to enable APIs or create a repository. [likely] The first deploy takes 5–15 minutes and ends with a **Service URL**.
5. Test it:
   ```
   curl https://YOUR-SERVICE-URL/health
   curl -X POST https://YOUR-SERVICE-URL/identify -H "X-API-Key: YOUR_KEY" -F "audio=@samples/clip1.m4a"
   ```
   Then run the second command without the `-H` part and confirm a 401.
6. Time a cold start: leave it unused for 20 minutes, then run `time curl https://YOUR-SERVICE-URL/health`. Record the seconds; your app's "Warming up…" timeout in week 5 depends on it.
7. Keep storage costs near zero: [likely] each deploy stores a new image and this one is larger than the free allowance, so delete older images in the Cloud Console under **Artifact Registry** → **cloud-run-source-deploy**, keeping the newest.

**Check:** the budget appears under Budgets & alerts, the live URL works with your key, returns 401 without it, and the cold-start time is in your build log.

**Compare** with the `Dockerfile` in the answer key.

## Part H: Lock it in (week 3, about 2 hours)

**Goal:** make sure the learning sticks, and capture it for your next project.

1. **Rebuild from memory.** In an empty folder, with no notes or Claude, take 60 minutes to rebuild `/health` and `/identify` with the API-key check and one test (use a fake identifier). Afterwards, list what you couldn't do in `LEARNING_LOG.md` and review those topics.
2. **Decision note.** Write `docs/decisions/001-birdnet-python-service.md` with four headings: Decision; Options considered (sending audio to a general AI model, running BirdNET in the browser, this service); Why (accuracy, cost, speed and license, using your Part F and G numbers); Tradeoffs (cold starts, a second language, the license limit).
3. **Playbook.** Add two entries to `PLAYBOOK.md`: "Wrap an ML model in a web API" and "Deploy a container to Cloud Run." For each: when to use it, the steps in order, and the gotchas you actually hit.

**Check:** you can explain the decision note out loud in under a minute, and both playbook entries exist.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `command not found: uv` or `ffmpeg` | Close and reopen Terminal. If it persists, run the `brew install` command again. |
| `No module named 'app'` when running pytest | Check the `[tool.pytest.ini_options]` lines from Part B, and that `app/__init__.py` exists. |
| An error mentioning LiteRT or `ai_edge_litert` | Run `uv python pin 3.12`, then `uv sync`. On an Intel Mac (`uname -m` prints `x86_64`), load `birdnet.load("acoustic", "3.0", "onnx")` and `birdnet.load("geo", "3.0", "onnx")` instead. |
| `KeyError: 'species_name'` or `'confidence'` | The library's output columns may differ. Print one row and adjust your code to match. |
| 415 on a real recording | Test ffmpeg by hand: `ffmpeg -i samples/clip1.m4a test.wav`. |
| xeno-canto returns 401 or 403 | Your key is wrong or your email isn't verified. |
| `docker: command not found` or "Cannot connect to the Docker daemon" | Open Docker Desktop and wait until it says it's running. |
| Deploy fails with a billing or permission error | Link the `bird-nerd` project to your billing account under **Billing** → **My projects**. |
| Deploy succeeds but requests fail | Read the logs: `gcloud run services logs read listen-api --region us-central1`. |

When something breaks, ask Claude Code: *"Help me find the root cause. Ask me questions and give hints; don't fix it for me."* Record each problem and fix in your build log; they make your best interview stories.

## Sources

- [birdnet package (BirdNET team)](https://github.com/birdnet-team/birdnet)
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [AI SDK Agents docs](https://ai-sdk.dev/docs/agents/overview)
- [xeno-canto API key requirement](https://pypi.org/project/xenocanto-api/)
- [Deploying to Cloud Run from source](https://cloud.google.com/run/docs/deploying-source-code)
- [Cloud Run pricing](https://cloud.google.com/run/pricing)
- [Google Cloud free trial](https://cloud.google.com/free)
