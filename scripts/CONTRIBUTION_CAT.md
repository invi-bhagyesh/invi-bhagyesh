# Contribution cat

A standalone animated SVG inspired by [Platane/snk](https://github.com/Platane/snk),
drawn and generated here without dependencies. A ginger cat runs across the real
GitHub contribution calendar, clearing each square as it passes. The calendar
refills at the end of the 42-second loop. The SVG supports dark mode and shows
the static calendar when reduced motion is requested.

Regenerate from the repository root:

```sh
python3 scripts/contribution_cat.py --user invi-bhagyesh --output assets/contribution-cat.svg
```

The workflow refreshes the image daily at 03:23 UTC and can also be triggered
manually. GitHub may delay scheduled runs. Public contribution-calendar HTML is
used, so no personal token is required. If GitHub changes that HTML or a request
fails, generation fails before replacing the previous image. Check the workflow
logs if the dates stop updating.

For an offline run, pass `--input path/to/saved-calendar.html`. To embed elsewhere:

```md
![My contribution cat](https://raw.githubusercontent.com/invi-bhagyesh/invi-bhagyesh/main/assets/contribution-cat.svg)
```
