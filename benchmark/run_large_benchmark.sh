(
    cd pivotpy_readme_x1000 && \
    # Download a large README file for benchmarking (~7MB)
    curl -sOL https://github.com/asaboor-gh/pivotpy/blob/2ad43748d0a306412f1c9ee889ff3647f4f196c8/README.md && \
    hyperfine \
        'python comrak_bench.py' -n baseline \
        'python markdown_bench.py' -n markdown \
        'python markdown2_bench.py' -n markdown2 \
        --warmup 5
    rm README.md
)
