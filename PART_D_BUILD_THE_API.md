# Part D: Build the API, step by step

**Goal:** wrap your `app/birds.py` in a web API that other code can call. It gets two endpoints (`/health` and `/identify`), an API-key check, and limits on what it accepts.

**You're done when:** every error case returns the right HTTP status code. You'll prove it with the test table in Step 9.

**Time:** about 5 hours across 9 small steps. Each step ends with a **Check**. Don't start the next step until the Check passes.

**How to use hints:** each step has hints hidden in fold-outs. Open **Hint 1** first. Open **Hint 2** only if you're still stuck after trying Hint 1. Neither hint contains the full answer.

All commands run in Terminal, from the `listen-api/` folder unless a step says otherwise.

---

## Before you start (20 minutes)

1. **Read** these pages of the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/): First Steps, Request Files, Request Forms and Files, Header Parameters, Dependencies, and Handling Errors. Skim them; you'll come back to each one when its step needs it.
2. **Answer in `LEARNING_LOG.md`:** Why check the API key in a dependency instead of inside the endpoint? What's the Express equivalent?
3. **Plan:** write 3–5 lines in your log describing what `app/main.py` will do, in your own words.
4. **Confirm** FastAPI is installed:

   ```
   uv run python -c "import fastapi, multipart; print('ok')"
   ```

   It should print `ok`. (`multipart` comes from `python-multipart`, which FastAPI needs to read file uploads.)

---

## The concepts in one page

### FastAPI compared with Express

| Idea | Express (JavaScript) | FastAPI (Python) |
|---|---|---|
| Create the app | `const app = express()` | `app = FastAPI()` |
| A route | `app.get("/health", (req, res) => ...)` | a function with `@app.get("/health")` above it |
| Send JSON | `res.json({ status: "ok" })` | `return {"status": "ok"}` (a dict becomes JSON automatically) |
| Read a header | `req.get("X-API-Key")` | a function parameter declared with `Header()` |
| Read an uploaded file | `multer` middleware, then `req.file` | a parameter typed `UploadFile` declared with `File()` |
| Read a form field | `req.body.lat` (after a body parser) | a parameter declared with `Form()` |
| Validate input | you write it, or use a library like zod | type hints and limits like `Form(ge=-90, le=90)`; FastAPI checks them and returns 422 itself |
| Shared logic before a route | middleware: `app.post("/identify", requireKey, handler)` | a dependency: `Depends(require_key)` |
| Return an error | `res.status(401).json(...)` or `throw` to an error handler | `raise HTTPException(status_code=401, detail="...")` |
| Run the server | `node server.js` | `uv run uvicorn app.main:app --reload` |

The big difference: in Express you pull things out of `req`. **In FastAPI you declare what you need as function parameters, and FastAPI hands them to you**, already checked.

### HTTP status codes you'll use

| Code | Name | Whose fault | When Bird Nerd uses it |
|---|---|---|---|
| 200 | OK | Nobody's | It worked |
| 400 | Bad Request | Caller | The file is empty |
| 401 | Unauthorized | Caller | The API key is missing or wrong |
| 404 | Not Found | Caller | Wrong URL (FastAPI does this) |
| 405 | Method Not Allowed | Caller | `GET /identify` instead of `POST` (FastAPI does this) |
| 413 | Content Too Large | Caller | The file is over 10 MB |
| 415 | Unsupported Media Type | Caller | ffmpeg can't read the file as audio |
| 422 | Unprocessable Content | Caller | A field is missing or out of range (FastAPI does this) |
| 500 | Internal Server Error | **Server** | Your code crashed |

**Rule of thumb:** 4xx means "the caller sent something wrong; fixing the request will fix it." 5xx means "the server broke; retrying the same request won't help." A good API never returns 500 for bad input.

---

## Step 1: Hello FastAPI, and `/health` (30 minutes)

**Learn:** a health endpoint lets a hosting service (Cloud Run, in Part G) ask "are you alive?" without doing any real work.

**Build:** create `app/main.py` with a FastAPI app and a `GET /health` route that returns `{"status": "ok"}`.

**Run it:**

```
uv run uvicorn app.main:app --reload
```

`app.main:app` means "in the file `app/main.py`, use the variable named `app`." `--reload` restarts the server when you save, like `nodemon`.

<details><summary>Hint 1</summary>

The "First Steps" page of the tutorial builds almost exactly this. Change the path and what it returns.
</details>

<details><summary>Hint 2</summary>

You need one import (`from fastapi import FastAPI`), one line to create the app, and a three-line function with a decorator.
</details>

**Check:** in a second Terminal window:

```
curl -i http://127.0.0.1:8000/health
```

The first line says `HTTP/1.1 200 OK` and the last line is `{"status":"ok"}`. Also open `http://127.0.0.1:8000/docs`: FastAPI built interactive docs for you.

---

## Step 2: A stub `/identify` (20 minutes)

**Learn:** build the outside of an endpoint first and fill it in later. A stub lets you test the checks around it before the slow BirdNET part exists.

**Build:** add `POST /identify` that, for now, just returns `{"stub": true}`.

**Check:**

```
curl -i -X POST http://127.0.0.1:8000/identify
```

returns 200 with `{"stub":true}`. Then try `curl -i http://127.0.0.1:8000/identify` (a GET). What status do you get, and why? Write the answer in your log.

---

## Step 3: The API-key check (45 minutes)

**Learn:**

- Re-read the **Dependencies** and **Header Parameters** pages.
- A **dependency** is a function FastAPI runs before your endpoint. If it raises `HTTPException`, the endpoint never runs. This is the same job as Express middleware like `requireKey(req, res, next)`, except you attach it to one route with `Depends()` instead of a `next()` chain.
- Header names: a parameter named `x_api_key` declared with `Header()` reads the `X-API-Key` header. FastAPI turns underscores into hyphens, and header names ignore case.
- Environment variables: Python reads them with `os.environ`, like `process.env` in Node.

**Build:**

1. Write a function, for example `require_api_key`, that reads the `X-API-Key` header.
2. Compare it with the `LISTEN_API_KEY` environment variable. If they don't match, raise `HTTPException` with status 401.
3. Attach it to `/identify` with `Depends()`. Leave `/health` open: the hosting service won't have your key.

**Think before you code:** what should happen if `LISTEN_API_KEY` isn't set at all on the server? If the variable is missing and the header is missing, a careless comparison could let everyone in. Write down which status code you'll return in that case and why.

<details><summary>Hint 1</summary>

Make the header optional (default `None`) so a missing header reaches your code and gets your 401. If it's required, FastAPI returns 422 before your check runs.
</details>

<details><summary>Hint 2</summary>

- Read the variable with `os.environ.get("LISTEN_API_KEY")`, which returns `None` instead of crashing when it's unset.
- Compare keys with `secrets.compare_digest(a, b)` instead of `==`. `==` stops at the first different character, so an attacker can time it to guess a key one character at a time. Both arguments must be strings, so handle `None` first.
- You can attach a dependency without receiving its value: `@app.post("/identify", dependencies=[Depends(require_api_key)])`, or as a parameter in the endpoint. Either works.
</details>

**Run the server with a key:** stop the server (Ctrl+C), then:

```
export LISTEN_API_KEY=dev-key-123
uv run uvicorn app.main:app --reload
```

`export` only lasts for this Terminal window. Run it again in any new window.

**Check:**

| Request | Expected |
|---|---|
| `curl -i -X POST http://127.0.0.1:8000/identify` | 401 |
| `curl -i -X POST -H "X-API-Key: wrong" http://127.0.0.1:8000/identify` | 401 |
| `curl -i -X POST -H "X-API-Key: dev-key-123" http://127.0.0.1:8000/identify` | 200 |
| `curl -i http://127.0.0.1:8000/health` (no key) | 200 |

---

## Step 4: Accept the audio file (40 minutes)

**Learn:**

- Re-read **Request Files**.
- Files arrive as `multipart/form-data`, the same format an HTML `<form enctype="multipart/form-data">` sends. In Express you'd add `multer`; in FastAPI you declare a parameter typed `UploadFile` with `File()`.
- An `UploadFile` has `.filename`, `.content_type`, and `.file`, a normal Python file object you can `.read()`.

**Build:** change the stub so `/identify` requires a file field named `audio`. For now, return the file's name and how many bytes it has.

**Make test files.** Keep them outside your repo so they never get committed:

```
mkdir -p ~/bird-test
touch ~/bird-test/empty.m4a
head -c 11000000 /dev/zero > ~/bird-test/big.m4a
echo "this is not audio" > ~/bird-test/not-audio.m4a
```

That gives you an empty file, an 11 MB file of zeros, and a text file pretending to be audio.

<details><summary>Hint 1</summary>

The parameter name must match the form field name exactly: `audio`.
</details>

<details><summary>Hint 2</summary>

`len(audio.file.read())` gives the size in bytes. You'll replace this in the next step, because reading the whole file at once is a problem when someone uploads 2 GB.
</details>

**Check:** `-F` sends a form field, and `@` means "read this file."

| Request | Expected |
|---|---|
| `curl -i -X POST -H "X-API-Key: dev-key-123" -F audio=@samples/clip1.m4a http://127.0.0.1:8000/identify` | 200, with the file name and size |
| `curl -i -X POST -H "X-API-Key: dev-key-123" http://127.0.0.1:8000/identify` (no file) | 422 (FastAPI: required field missing) |

Read the 422 response body. FastAPI tells the caller exactly which field is wrong. Note in your log how that compares with hand-written validation in Express.

---

## Step 5: Size limits: 400 and 413 (40 minutes)

**Learn:** why limit size at all? Every byte you accept uses memory and processing time. Without a limit, one person can take your server down with one huge upload.

**Build:**

1. Add a constant at the top of the file: 10 MB in bytes. (10 MB is `10 * 1024 * 1024`.)
2. Read the upload **without reading all of it**: read at most one byte more than the limit.
3. If you got 0 bytes, raise 400.
4. If you got more than the limit, raise 413.

<details><summary>Hint 1</summary>

If the limit is 10 bytes and you ask for 11, you'll get 11 bytes only if the file is too big. You never need to know how big it really is.
</details>

<details><summary>Hint 2</summary>

`audio.file.read(MAX_BYTES + 1)` returns `bytes`. Check its `len()`. FastAPI's `status` module has named constants if you prefer them to bare numbers, but `413` works too.
</details>

**Check:**

| Request (add `-H "X-API-Key: dev-key-123"` to each) | Expected |
|---|---|
| `-F audio=@$HOME/bird-test/empty.m4a` | 400 |
| `-F audio=@$HOME/bird-test/big.m4a` | 413 |
| `-F audio=@samples/clip1.m4a` | 200 |

**Answer in your log:** which check should run first, the API key or the file size? Why?

---

## Step 6: Location fields and 422 (40 minutes)

**Learn:**

- Re-read **Request Forms and Files**. Form fields and files travel in the same request body.
- `Form(ge=..., le=...)` means "greater than or equal to" and "less than or equal to." FastAPI checks the range and returns 422 for you, so you write no `if` statements for it.
- A parameter typed `date` is parsed from text like `2026-11-11` into a Python `date`. In JavaScript you'd call `new Date(...)` yourself and check for `Invalid Date`.

**Build:** add three optional form fields:

| Field | Type | Allowed range |
|---|---|---|
| `lat` | number | −90 to 90 |
| `lon` | number | −180 to 180 |
| `recorded_on` | date | any valid date |

Return them in the stub response for now, so you can see what arrived.

<details><summary>Hint 1</summary>

Optional means the type allows `None` and the default is `None`.
</details>

<details><summary>Hint 2</summary>

The shape is `name: float | None = Form(default=None, ge=..., le=...)`. `float | None` is Python's version of TypeScript's `number | null`.
</details>

**Check** (key and `-F audio=@samples/clip1.m4a` on each):

| Extra form fields | Expected |
|---|---|
| `-F lat=47.6 -F lon=-122.3 -F recorded_on=2026-11-11` | 200, fields echoed back |
| `-F lat=200` | 422 |
| `-F lon=-181` | 422 |
| `-F recorded_on=yesterday` | 422 |

**Experiment:** send a **wrong key and `lat=200`** in one request. Before running it, predict whether you'll get 401 or 422. Then run it, and write in your log what this tells you about the order FastAPI runs things in.

---

## Step 7: Convert with ffmpeg: 415 (45 minutes)

**Learn:**

- ffmpeg needs a file on disk, but the upload is bytes in memory. Write the bytes to a temporary folder, convert, and let the folder delete itself, just as your `identify()` already does with `tempfile.TemporaryDirectory()`.
- Your `to_wav()` calls `subprocess.run(..., check=True)`. When ffmpeg fails, that raises `subprocess.CalledProcessError`. Catching it is like a `try/catch` around a failed child process in Node.
- Why 415 and not 400? 415 says specifically "I can't handle this kind of content," which tells the caller exactly what to fix.

**Build:**

1. Inside a temporary folder, save the uploaded bytes to a file.
2. Call your `to_wav()` to make a WAV in the same folder.
3. If ffmpeg fails, raise 415.

**Think before you code:** if ffmpeg isn't installed on the server at all, `subprocess.run` raises `FileNotFoundError`, not `CalledProcessError`. Should that return 415 or 500? (Use the "whose fault" column in the status-code table.)

<details><summary>Hint 1</summary>

Keep the original file's extension when you save it (from `audio.filename`). ffmpeg usually works out the format from the content, but the extension helps.
</details>

<details><summary>Hint 2</summary>

- `os.path.splitext(name)` splits `"clip1.m4a"` into `("clip1", ".m4a")`. The filename can be `None`, so have a fallback.
- Open the file with mode `"wb"` (write bytes) to save raw bytes.
- Catch only `subprocess.CalledProcessError`. A bare `except:` would also hide real bugs as 415s.
- Everything that uses the files must happen inside the `with` block, because the folder is deleted when the block ends.
</details>

**Check** (with the key):

| Request | Expected |
|---|---|
| `-F audio=@$HOME/bird-test/not-audio.m4a` | 415 |
| `-F audio=@samples/clip1.m4a` | 200 |

---

## Step 8: Call BirdNET and shape the response (60 minutes)

**Learn:**

- **`def` versus `async def`.** In Node, everything shares one event loop, and a slow synchronous call freezes every request. Python has the same problem with `async def`. BirdNET and ffmpeg block, so define `/identify` with plain `def`. FastAPI then runs it in a separate thread, and the server keeps answering other requests (like `/health`) meanwhile.
- **Why a `get_identifier()` dependency?** In Part E your tests will swap the real BirdNET for a fake one that answers instantly. If the endpoint calls `identify` directly, you can't swap it. If it receives the function through `Depends(get_identifier)`, a test can replace it in one line. It's the same idea as passing a mock into a function in Jest instead of importing the real thing.
- **Timing:** `time.perf_counter()` is Python's `performance.now()`, except it returns seconds, not milliseconds.

**Build:**

1. Write `get_identifier()`, which returns your `identify` function from `app/birds.py`.
2. Make `/identify` receive the identifier through `Depends(get_identifier)`.
3. Call it with the WAV path, plus `lat`, `lon` and `recorded_on`.
4. Return:

| Field | Value |
|---|---|
| `detections` | the list from `identify()` |
| `model` | a string naming the model, for example `"BirdNET 2.4"` |
| `location_filter` | `true` only when `lat`, `lon` and `recorded_on` were **all** given |
| `processing_ms` | how long the work took, in whole milliseconds |

<details><summary>Hint 1</summary>

FastAPI can turn a list of dataclasses into JSON on its own, so you can return `detections` as they are.
</details>

<details><summary>Hint 2</summary>

- Start the timer before the work and stop it after. Multiply the difference by 1000 and round it.
- `location_filter` can be one expression using `is not None` three times with `and`. Don't use plain truthiness: `lat=0` (the equator) is a real location, but `0` is falsy in Python just as in JavaScript.
- Your `identify()` names its date parameter `day`. Pass `recorded_on` to it.
</details>

**Check:**

```
curl -s -X POST -H "X-API-Key: dev-key-123" \
  -F audio=@samples/clip1.m4a \
  http://127.0.0.1:8000/identify
```

returns American Crow at the top, `location_filter` is `false`, and `processing_ms` is a number. Add `-F lat=... -F lon=... -F recorded_on=2026-11-11` with your home location and `location_filter` becomes `true`. (The first request is slow while the model loads; the second should be faster because of `lru_cache`.)

---

## Step 9: Prove every error case (30 minutes)

This is the Part D **Check**. Restart the server so you're testing the final code, then run every row. Fill in the **Actual** column yourself. Don't skip a row because "it worked in an earlier step." Later code can break earlier behavior.

Set these in your test Terminal first to keep the commands short:

```
URL=http://127.0.0.1:8000
KEY="X-API-Key: dev-key-123"
```

| # | Case | Command | Expected | Actual |
|---|---|---|---|---|
| 1 | Health | `curl -i $URL/health` | 200 | |
| 2 | Success, no location | `curl -i -H "$KEY" -F audio=@samples/clip1.m4a $URL/identify` | 200, `location_filter: false` | |
| 3 | Success, with location | row 2 plus `-F lat=47.6 -F lon=-122.3 -F recorded_on=2026-11-11` | 200, `location_filter: true` | |
| 4 | Only some location fields | row 2 plus `-F lat=47.6` | 200, `location_filter: false` | |
| 5 | No key | `curl -i -F audio=@samples/clip1.m4a $URL/identify` | 401 | |
| 6 | Wrong key | `curl -i -H "X-API-Key: nope" -F audio=@samples/clip1.m4a $URL/identify` | 401 | |
| 7 | Empty file | `curl -i -H "$KEY" -F audio=@$HOME/bird-test/empty.m4a $URL/identify` | 400 | |
| 8 | File over 10 MB | `curl -i -H "$KEY" -F audio=@$HOME/bird-test/big.m4a $URL/identify` | 413 | |
| 9 | Not audio | `curl -i -H "$KEY" -F audio=@$HOME/bird-test/not-audio.m4a $URL/identify` | 415 | |
| 10 | `lat` out of range | row 2 plus `-F lat=200` | 422 | |
| 11 | `lon` out of range | row 2 plus `-F lon=-181` | 422 | |
| 12 | Bad date | row 2 plus `-F recorded_on=yesterday` | 422 | |
| 13 | No file | `curl -i -X POST -H "$KEY" $URL/identify` | 422 | |
| 14 | Wrong method | `curl -i -H "$KEY" $URL/identify` | 405 | |

**Check:** every row's Actual matches Expected, and the server never returned 500. Save the filled-in table in `BUILD_LOG.MD`. In Part E you'll turn each row into an automated test.

---

## Wrap up (20 minutes)

1. **Compare** your `app/main.py` with the answer key's `app/main.py`. Write one difference in your log, and say which version you prefer and why.
2. **Reflect** in `LEARNING_LOG.md` (two lines): what I learned, and what I'd do differently next time.
3. **Playbook:** add an entry to `PLAYBOOK.md` called "Wrap an ML model in an API": when to use it, the steps, and the gotchas you hit.
4. **Commit** your work.
5. **Tick the box** for "Build the API" in `BIRD_NERD_PLAN.md`.
6. **Quiz:** ask Claude, "Quiz me on Part D." Answer 2 questions about what you built before moving to Part E.

## If something goes wrong

| What you see | Likely cause |
|---|---|
| Every request gets 401, even with the right key | `LISTEN_API_KEY` wasn't exported in the window running the server. Run `echo $LISTEN_API_KEY` there. |
| `RuntimeError: Form data requires "python-multipart"` | Run `uv sync` from `listen-api/`. |
| `Error loading ASGI app. Could not import module "app.main"` | You're not in `listen-api/`, or the file isn't at `app/main.py`. |
| A good clip returns 415 | Test ffmpeg by hand: `ffmpeg -i samples/clip1.m4a test.wav`. |
| Any request returns 500 | Read the traceback in the server's Terminal window. A 500 means an exception you didn't catch. Decide whether it's bad input (should be a 4xx) or a real bug. |
| `/health` hangs while `/identify` runs | `/identify` is probably `async def`. Change it to `def` (see Step 8). |
