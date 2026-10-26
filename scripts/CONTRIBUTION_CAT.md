# Contribution cat

A standalone animated SVG inspired by [Platane/snk](https://github.com/Platane/snk),
generated here without dependencies. The original orange pixel cat from the
website runs back and forth beneath the real GitHub contribution calendar on a 24-second loop.
The cat avoids every square and leaves all contribution colors intact. The
three-frame sprite is embedded in the SVG, so the image works on its own. The SVG supports dark mode and shows
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
