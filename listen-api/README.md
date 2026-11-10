# Listen API

## Requirements

- [uv](https://docs.astral.sh/uv/)
- ffmpeg (`brew install ffmpeg`)

## How to run

Run these commands from the `listen-api/` folder.

### Convert a recording to WAV

`to_wav(src, dst)` converts an audio file to a mono, 48 kHz WAV containing at most the first 60 seconds. If the output file already exists, it is overwritten.

1. Start Python:

   ```
   uv run python
   ```

2. When you see the `>>>` prompt, import the function. You only need to do this once per Python session:

   ```python
   from app.birds import to_wav
   ```

3. Convert a file, giving the input path first and the output path second:

   ```python
   to_wav("samples/clip1.m4a", "samples/clip1.wav")
   ```

4. Leave Python when you're done:

   ```python
   exit()
   ```

If you edit `app/birds.py`, exit and start Python again to pick up your changes.

### Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `NameError: name 'to_wav' is not defined` | The import hasn't been run in this Python session | Run the import in step 2 |
| `CalledProcessError` | ffmpeg couldn't convert the file, often because the input path is wrong | Check that the input file exists and the path is correct |
