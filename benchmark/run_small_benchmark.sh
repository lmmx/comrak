(
    cd hello_world_x1000 && \
    hyperfine \
        'python comrak_bench.py' -n baseline \
        'python markdown_bench.py' -n markdown \
        'python markdown2_bench.py' -n markdown2 \
        --warmup 5
)
