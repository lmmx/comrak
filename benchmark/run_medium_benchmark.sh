(
    cd awesome_python_readme_x1000 && \
    curl -sOL https://raw.githubusercontent.com/vinta/awesome-python/master/README.md && \
    hyperfine \
        'python comrak_bench.py' -n baseline \
        'python markdown_bench.py' -n markdown \
        'python markdown2_bench.py' -n markdown2 \
        --warmup 5
    rm README.md
)
