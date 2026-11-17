# Linux-Server

Auf den Servern im Homelab übernimmt die Ansible-Rolle `sys-base` (Task `_omp.yml`) die
Einrichtung. Diese Seite beschreibt den Zielzustand und wie man ein neues Theme vorab testet.

## Zielzustand

| Was | Wo |
|---|---|
| Programm | `/usr/local/bin/oh-my-posh` (Version aus `sys_base__config._omp.version`) |
| Theme | `/usr/local/share/oh-my-posh/themes/<sys_base__config._omp.theme_file>` |
| Einbindung | Block `# BEGIN/END ANSIBLE MANAGED BLOCK - OH-MY-POSH` in `/etc/bash.bashrc` |

Entfernte Hosts erscheinen mit **oranger** Host-Box, root mit **Bordeaux**.

## Neues Theme vor dem Ausrollen testen

Ohne etwas am System zu ändern:

```powershell
# unter Windows
scp D:\usr\local\share\oh-my-posh\themes\mw88.omp.json <user>@<host>:/tmp/
ssh <user>@<host>
```

```bash
# auf dem Server
bash --norc
eval "$(oh-my-posh init bash --config /tmp/mw88.omp.json)"
false            # → ✘ 1
sleep 3          # → 3s
cd <git-repo>    # → Git-Box, ggf. Git-Zeile
exit
```

Achten auf: keine Meldung `unable to create text based on template` (würde auf eine zu alte
oh-my-posh-Version hindeuten), orange Host-Box, maigrünes `»`, kein Transient Prompt.

## Manuell (ohne Ansible)

Wie in [wsl.md](wsl.md), Schritte 1 und 3. Das Theme statt aus `/mnt/d` aus dem Repo beziehen,
z. B. per `scp` vom Ansible-Controller oder per flachem Klon des Tags:

```bash
tag=v1.0.0
git -c advice.detachedHead=false clone --quiet --depth 1 --branch "$tag" \
  git@github.com:mw88-personal/oh-my-posh-theme.git /tmp/omp-theme
sudo install -D -m 644 /tmp/omp-theme/mw88.omp.json /usr/local/share/oh-my-posh/themes/mw88.omp.json
rm -rf /tmp/omp-theme
```
