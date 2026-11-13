# Build Log

## Part C: Run BirdNET yourself

### Clips

Recorded live near home on 2026-11-11 with Voice Memos. I identified the birds myself.

| Clip | Species (truth) | Length | BirdNET top result | Confidence | Match? |
|---|---|---|---|---|---|
| `clip1` | American Crow | 35.6 s | American Crow, 6 chunks. Also Red-shouldered Hawk 0.61 at 6 s. | 0.98 | ✅ |
| `clip2` | Dark-eyed Junco | 35.9 s | Dark-eyed Junco, 6 chunks | 0.97 | ✅ |
| `clip3` | Song Sparrow | 41.7 s | Song Sparrow, 5 chunks | 0.97 | ✅ |

### Earlier test: Merlin playback clips (replaced)

It was raining too hard to record live birds, so my first clips were Merlin app recordings played through a phone speaker and re-recorded. I've since deleted them and replaced them with the live clips above.

| Clip | Played from Merlin | BirdNET result (cutoff 0.25) |
|---|---|---|
| `clip1` | Barnacle Goose (probably) | Pileated Woodpecker 0.54 and Pacific Chorus Frog 0.50: both wrong. BirdNET did hear a Barnacle Goose, but only at 0.14. |
| `clip2` | Western Meadowlark | Western Meadowlark 0.93: correct. Also Indian Golden Oriole 0.29 and Rufous-backed Robin 0.26, which are unlikely here. |
| `clip3` | Banded Wren (probably) | Common Nightingale 0.29 and Saffron Finch 0.29: both wrong, and no wren detected |

**Lessons:**
- **The cutoff is a trade-off.** 0.25 removed wrong guesses, but it also removed the real Barnacle Goose at 0.14. A higher cutoff gives fewer wrong answers but more missed birds.
- **Speaker playback lowers scores.** Small speakers lose low and high notes, and the room adds echo.
- **A location filter only helps when the bird is really there.** Merlin clips of non-local birds would be removed even though they were the right answer.

### Log questions

**BirdNET scores audio in 3-second chunks. Why can one recording produce several different species?**

_My answer:_

**Why might a location filter help?**

_My answer:_

### Location filter results (step 15)

_Prediction before running it:_

Run on 2026-11-11 (week 42). Far-away location: Scotland (55.95, -3.19).

| Clip | No filter | Home location | Far-away location |
|---|---|---|---|
| `clip1` | 6 × American Crow (0.94–0.98), Red-shouldered Hawk 0.61 | 6 × American Crow. **Hawk removed.** | Nothing: all crows removed |
| `clip2` | 6 × Dark-eyed Junco (0.84–0.97) | 6 × Dark-eyed Junco, no change | Nothing: all juncos removed |
| `clip3` | 5 × Song Sparrow (0.96–0.97) | 5 × Song Sparrow, no change | Nothing: all sparrows removed |

_Did the filter change the results?_
