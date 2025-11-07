README_video


How to use the .env toggles

Default behavior (no changes): Captions are burned in and the burned file is sent.

Keep only sidecar SRT (no burn-in):

```
CAPTIONS_MODE=sidecar
```

Keep both burned and sidecar, but send the burned one:

```
CAPTIONS_MODE=both
SEND_VARIANT=burned
```

Keep both, but send the plain file (some platforms auto-render sidecar):

```
CAPTIONS_MODE=both
SEND_VARIANT=plain
```

