## Small string (8 lines)

Source: `hello_world_x1000`

```sh
bash run_small_benchmark.sh
```

```
Benchmark 1: baseline
  Time (mean ± σ):      15.4 ms ±   0.4 ms    [User: 11.3 ms, System: 4.0 ms]
  Range (min … max):    14.9 ms …  19.7 ms    190 runs

  Warning: Statistical outliers were detected. Consider re-running this benchmark on a quiet system without any interferences from other programs. It might help to use the '--warmup' or '--prepare' options.

Benchmark 2: markdown
  Time (mean ± σ):     300.4 ms ±   5.7 ms    [User: 291.1 ms, System: 8.6 ms]
  Range (min … max):   290.8 ms … 308.1 ms    10 runs

Benchmark 3: markdown2
  Time (mean ± σ):     212.7 ms ±   3.5 ms    [User: 204.0 ms, System: 8.4 ms]
  Range (min … max):   206.6 ms … 219.6 ms    13 runs

Summary
  baseline ran
   13.82 ± 0.41 times faster than markdown2
   19.52 ± 0.60 times faster than markdown
```

## Medium file (1200 lines)

Source: `awesome_python_readme_x1000`

```sh
bash run_medium_benchmark.sh
```

```
Benchmark 1: baseline
  Time (mean ± σ):      31.0 ms ±   0.8 ms    [User: 24.7 ms, System: 6.1 ms]
  Range (min … max):    29.5 ms …  32.8 ms    90 runs

Benchmark 2: markdown
  Time (mean ± σ):     632.0 ms ±   4.4 ms    [User: 621.7 ms, System: 9.7 ms]
  Range (min … max):   625.8 ms … 639.6 ms    10 runs

Benchmark 3: markdown2
  Time (mean ± σ):      2.620 s ±  0.017 s    [User: 2.610 s, System: 0.010 s]
  Range (min … max):    2.592 s …  2.647 s    10 runs

Summary
  baseline ran
   20.40 ± 0.52 times faster than markdown
   84.57 ± 2.16 times faster than markdown2
```

## Large file (1200 lines)

Source: `pivotpy_readme_x1000`

```sh
bash run_large_benchmark.sh
```

```
Benchmark 1: baseline
  Time (mean ± σ):      24.9 ms ±   0.4 ms    [User: 19.3 ms, System: 5.5 ms]
  Range (min … max):    24.3 ms …  26.1 ms    118 runs

Benchmark 2: markdown
  Time (mean ± σ):     237.6 ms ±   9.0 ms    [User: 225.0 ms, System: 12.1 ms]
  Range (min … max):   228.0 ms … 258.5 ms    12 runs

Benchmark 3: markdown2
  Time (mean ± σ):     408.5 ms ±   5.7 ms    [User: 400.5 ms, System: 7.8 ms]
  Range (min … max):   403.6 ms … 422.8 ms    10 runs

Summary
  baseline ran
    9.54 ± 0.39 times faster than markdown
   16.40 ± 0.35 times faster than markdown2
```

## Review

|   Size |   comrak |  markdown |  markdown2 |
| -----: | -------: | --------: | ---------: |
|  Small | ~15.4 ms | ~300.4 ms |  ~212.7 ms |
| Medium | ~31.0 ms | ~632.0 ms | ~2620.0 ms |
|  Large | ~24.9 ms | ~237.6 ms |  ~408.5 ms |

<img width="630" height="470" alt="image" src="https://github.com/user-attachments/assets/04aedb18-a4a7-45ae-b696-b786534ec10d" />

- The "Small" string has 8 lines, 18 words and 110 chars
- The "Medium" sized README has 1196 lines, 7900 words and 79936 chars
- The "Large" sized README has 1438 lines, 11963 words and 186580 chars

Or relatively:

- Medium has 150x more lines, 148x more words, 726x more chars vs. small
- Large has 1.2x more lines, 1.5x more words, 2.3x more chars vs. medium

If we plot the baseline (comrak) of small vs medium vs large we can see more clearly that this is unexpectedly non-monotonic runtime growth with size (i.e. the medium is not middling) indicating runtime depends more on structure than volume, something about the medium case likely triggers worst case parsing paths, while the large is syntactically simpler despite being longer

<img width="630" height="470" alt="image" src="https://github.com/user-attachments/assets/a0843cb2-1ca6-4ef2-b23a-3be283d77df4" />
