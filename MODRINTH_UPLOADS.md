# Uploading RTP Duels to Modrinth

Project: https://modrinth.com/plugin/rtp-duels  (add each file below as a **new version** on it).

The build gives you **3 files**: one for ALL of Paper, one for ALL of Bukkit and one for ALL of Spigot. All three contain the identical plugin, so it behaves exactly the same everywhere; they only differ in which loader you tick. Each one covers all 75 game versions listed below (Minecraft 1.8 up to 26.3).

For each file: **Create version** -> upload the file -> set the **Version number** -> tick the **Loader** -> tick **all** the game versions -> add the changelog (below) -> publish. PlaceholderAPI can be added as an *optional* dependency (only used to show the TimeSMP rank in the GUI).

| # | File | Version number | Loader |
|---|------|----------------|--------|
| 1 | `RTPDuels-1.1.0-paper.jar` | `1.1.0-paper` | Paper |
| 2 | `RTPDuels-1.1.0-bukkit.jar` | `1.1.0-bukkit` | Bukkit |
| 3 | `RTPDuels-1.1.0-spigot.jar` | `1.1.0-spigot` | Spigot |

## Game versions to tick (the same list on all three)

1.8, 1.8.1, 1.8.2, 1.8.3, 1.8.4, 1.8.5, 1.8.6, 1.8.7, 1.8.8, 1.8.9, 1.9, 1.9.1, 1.9.2, 1.9.3, 1.9.4, 1.10, 1.10.1, 1.10.2, 1.11, 1.11.1, 1.11.2, 1.12, 1.12.1, 1.12.2, 1.13, 1.13.1, 1.13.2, 1.14, 1.14.1, 1.14.2, 1.14.3, 1.14.4, 1.15, 1.15.1, 1.15.2, 1.16, 1.16.1, 1.16.2, 1.16.3, 1.16.4, 1.16.5, 1.17, 1.17.1, 1.18, 1.18.1, 1.18.2, 1.19, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.20, 1.20.1, 1.20.2, 1.20.3, 1.20.4, 1.20.5, 1.20.6, 1.21, 1.21.1, 1.21.2, 1.21.3, 1.21.4, 1.21.5, 1.21.6, 1.21.7, 1.21.8, 1.21.9, 1.21.10, 1.21.11, 26.1, 26.1.1, 26.1.2, 26.2, 26.3

**Before uploading:** run the *Test on real servers* workflow once and leave unticked any version that shows a red cross there. A version marked "skipped" just has no server download to test on.

Folia is built into the same code (it adds `folia-supported: true`), so the Paper file also runs on Folia 1.19.4 and newer. Tick Folia on it only if you want Modrinth to list it.

## Changelog text you can paste

> Now supports Bukkit, Spigot and Paper on Minecraft 1.8 up to 26.3 (Java 8 or newer). Behaviour is unchanged: same chat buttons, confirmation GUI, countdowns, land-only random spot, command lock and teleport protection.
> On Paper the random spot is loaded asynchronously, so far-away chunks no longer pause the server.
> The plugin is now called RTPDuels (config folder `plugins/RTPDuels/`); permissions are unchanged.

## Edit the project page once

- **Requirements:** replace "Paper 1.21+ and Java 21" with "Bukkit, Spigot or Paper - Minecraft 1.8 to 26.3 - Java 8 or newer".
- Everything else (commands, permissions, features) stays accurate.
