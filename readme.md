# Recursive parser

## Description
This project is a web scraper that collects data from websites and builds graphs of page relationships. The parser runs inside a Docker container and uses Selenium for automated website navigation.

## Key Features
- Page parsing with configurable recursion depth
- Support for different scanning modes (`strict`, `semi-strict`, `normal`)
- Data storage in pickle format
- Graph visualization using `pyvis`
- Option to exclude GET parameters from analysis
- Flexible configuration through `config.py`

## Requirements
- Docker
- docker-compose
- Selenium WebDriver image

## Installation and Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/ChainsAre2Tight/recursive-parser.git
   cd recursive-parser
   ```
2. Start the project using `docker-compose`:
   ```bash
   docker-compose up
   ```
   This will launch Selenium WebDriver and execute `python main.py both`, which first performs parsing and then graph construction.

## Modes of Operation
The project supports three modes:
- `parse` — performs website parsing and saves data.
- `export` — reads saved data and constructs a graph.
- `both` — sequentially executes `parse` and `export`.

## Configuring `config.py`
The configuration file is located in `/app/config.py` and allows customization of:
- Start page (`start_page`).
- Recursion depth (`maximum_recursion_depth`).
- Browser settings (`browser`).
- Page load wait time (`wait_time`).
- Parsing mode (`mode`).
- Use of cookies and directory grouping.

### Recommended Settings
- For an initial quick scan, set `maximum_recursion_depth = 1`, enable `cookies = True`, and `get_directories = True`.
- After the first scan, increase recursion depth or change the start page.
- `mode = strict` is recommended for the initial stage. Switch to `semi-strict` when expanding parsing boundaries. Use `normal` mode only if there are no social media links in the graph.
- Adjust `wait_time` based on your internet speed: lower values for fast connections, higher values for slow networks.

For detailed configuration explanations, see the [config README](app/readme.md).

