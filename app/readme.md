# README for config.py

## Description

The `config.py` file contains all the settings for the parser and graph generation. This file allows configuring parameters that determine the parser's behavior, the depth of website analysis, and link processing methods.

## Parameter Description

### Main Parameters

- **`start_page`** — the starting page for parsing.
- **`browser`** — the browser used by Selenium for loading pages.
- **`wait_time`** — the waiting time for page loading (in seconds).
- **`maximum_recursion_depth`** — the maximum recursion depth during parsing.
- **`mode`** — the parsing mode:
  - `strict` — the parser stays within a single website.
  - `semi-strict` — the parser moves beyond the website but remains within the domain.
  - `normal` — the parser follows all found links.

### Data Saving Parameters

- **`pickle_dump_file_name`** — the filename where parsing results are saved.
- **`graph_file_name`** — the filename for the output graph.
- **`strip_GET_params`** — if `True`, GET parameters will be removed from links.

### Link Processing Parameters

- **`cookies`** — if `True`, cookie information will be used.
- **`get_directories`** — if `True`, links will be grouped by directories.

## Configuration Recommendations

### Recursion Depth

- Start with `maximum_recursion_depth = 1` for quick reconnaissance of the website structure.
- Enable `cookies = True` and `get_directories = True` to gather as much useful information as possible.
- After the initial reconnaissance, increase the recursion depth or select a new starting page.

### Parsing Mode

- Use `strict` initially to prevent navigating outside the website.
- Switch to `semi-strict` if you need to expand the research area.
- `normal` may lead to parsing social media links, so it should only be used if no social media links are present in the graph.

### Wait Time

- Set `wait_time` based on your internet speed:
  - **Slow connection**: Increase `wait_time` (e.g., 5-10 seconds) to ensure pages load completely.
  - **Fast connection**: Decrease `wait_time` (e.g., 1-3 seconds) for quicker parsing.

## Additional Information

For more details on project configuration and execution, see the [main README](../readme.md).

