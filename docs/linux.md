# Linux servers

Same target state as in WSL ([wsl.md](wsl.md)):

| What | Where |
|---|---|
| Program | `/usr/local/bin/oh-my-posh` |
| Theme | `/usr/local/share/oh-my-posh/themes/mw88.omp.json` |
| Integration | block in `/etc/bash.bashrc` |

In the homelab, an Ansible role sets up this state (program version and theme are defined there).
Without Ansible, steps 1–3 from [wsl.md](wsl.md) apply unchanged.

Remote hosts show **orange** dots and an orange host name; root shows a **red** first dot and `#`.

## Test a new theme before rolling it out

Without changing anything on the system, directly on the server:

```bash
tag=v2.0.0
curl -fsSL -o /tmp/mw88.omp.json "https://raw.githubusercontent.com/mw88-personal/oh-my-posh-theme/$tag/mw88.omp.json"
bash --norc
eval "$(oh-my-posh init bash --config /tmp/mw88.omp.json)"
false            # → ✘ 1
sleep 3          # → 3s
cd <git-repo>    # → branch box, annotation above it if there are changes
exit
```

Check for: no message `unable to create text based on template` (would indicate an oh-my-posh
version that is too old), orange dots, may green `»`, annotation hook above the branch, no
transient prompt.
