FROM python:3.11-slim

# Install system dependencies for curses
RUN apt-get update && apt-get install -y ncurses-bin libncurses5-dev libncursesw5-dev && rm -rf /var/lib/apt/lists/*

# Install your game directly from PyPI
RUN pip install --no-cache-dir estregg-ybj

# Set the entrypoint to launch your game directly
CMD ["estregg"]
