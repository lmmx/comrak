## Small string (8 lines)

Source: `hello_world_x1000`

```sh
bash run_small_benchmark.sh
```

```
Benchmark 1: baseline
  Time (mean ± σ):      42.2 ms ±   0.9 ms    [User: 34.0 ms, System: 7.7 ms]
  Range (min … max):    40.6 ms …  46.0 ms    68 runs

Benchmark 2: markdown
  Time (mean ± σ):     854.2 ms ±   4.9 ms    [User: 833.7 ms, System: 20.0 ms]
  Range (min … max):   844.5 ms … 861.0 ms    10 runs

Benchmark 3: markdown2
  Time (mean ± σ):     608.1 ms ±   6.0 ms    [User: 586.7 ms, System: 16.0 ms]
  Range (min … max):   601.5 ms … 619.7 ms    10 runs

Summary
  'baseline' ran
   14.42 ± 0.34 times faster than 'markdown2'
   20.26 ± 0.46 times faster than 'markdown'
```

## Medium file (1200 lines)

Source: `awesome_python_readme_x1000`

```sh
bash run_medium_benchmark.sh
```

```
Benchmark 1: baseline
  Time (mean ± σ):     126.1 ms ±   1.7 ms    [User: 110.7 ms, System: 14.9 ms]
  Range (min … max):   123.0 ms … 129.8 ms    23 runs

Benchmark 2: markdown
  Time (mean ± σ):      2.070 s ±  0.010 s    [User: 2.034 s, System: 0.028 s]
  Range (min … max):    2.054 s …  2.084 s    10 runs

Benchmark 3: markdown2
  Time (mean ± σ):      7.205 s ±  0.041 s    [User: 7.160 s, System: 0.024 s]
  Range (min … max):    7.149 s …  7.299 s    10 runs

Summary
  'baseline' ran
   16.42 ± 0.24 times faster than 'markdown'
   57.14 ± 0.84 times faster than 'markdown2
```
