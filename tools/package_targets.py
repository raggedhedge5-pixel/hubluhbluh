#!/usr/bin/env python3
"""
Turns the ONE built plugin jar into three upload files - one for ALL of Paper, one for ALL of Bukkit and one
for ALL of Spigot - plus an upload sheet that says exactly what to tick for each.

All three files contain the identical plugin code (that is the point - every platform and version behaves the
same). The only difference is a tiny text file, META-INF/rtpduels-target.txt, so each file has its own checksum
(Modrinth refuses a second upload of byte-identical files).

    python3 tools/package_targets.py --jar target/RTPDuels.jar --out dist --sheet dist/MODRINTH_UPLOADS.md
"""
import argparse
import hashlib
import os
import sys
import xml.etree.ElementTree as ET
import zipfile


def rng(prefix, last):
    return [prefix] + ["%s.%d" % (prefix, i) for i in range(1, last + 1)]


# (group label, Minecraft versions on that group) - the single source of truth for every file and the sheet.
GROUPS = [
    ("1.8", rng("1.8", 9)),
    ("1.9", rng("1.9", 4)),
    ("1.10", rng("1.10", 2)),
    ("1.11", rng("1.11", 2)),
    ("1.12", rng("1.12", 2)),
    ("1.13", rng("1.13", 2)),
    ("1.14", rng("1.14", 4)),
    ("1.15", rng("1.15", 2)),
    ("1.16", rng("1.16", 5)),
    ("1.17", rng("1.17", 1)),
    ("1.18", rng("1.18", 2)),
    ("1.19", rng("1.19", 4)),
    ("1.20", rng("1.20", 6)),
    ("1.21", rng("1.21", 11)),
    ("26.1", ["26.1", "26.1.1", "26.1.2"]),
    ("26.2", ["26.2"]),
    ("26.3", ["26.3"]),
]

ALL_VERSIONS = [v for _, versions in GROUPS for v in versions]

# Platform id (= Modrinth loader id) and display name. Each gets ONE file covering every version above.
PLATFORMS = [
    ("paper", "Paper"),
    ("bukkit", "Bukkit"),
    ("spigot", "Spigot"),
]


def targets():
    """Yields (platform_id, platform_name, label, minecraft_versions)."""
    for pid, pname in PLATFORMS:
        yield pid, pname, "all", ALL_VERSIONS


def project_version(pom):
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    root = ET.parse(pom).getroot()
    node = root.find("m:version", ns)
    if node is None or not node.text:
        raise SystemExit("could not read <version> from " + pom)
    return node.text.strip()


def file_name(version, pid, label):
    return "RTPDuels-%s-%s.jar" % (version, pid)


def write_stamped_copy(src_jar, dest, version, pid, label, mc_versions):
    stamp = (
        "plugin=RTPDuels\n"
        "version=%s\n"
        "platform=%s\n"
        "minecraft-versions=%s\n"
        "note=Identical plugin code in every file; this text only gives each upload its own checksum.\n"
        % (version, pid, ",".join(mc_versions))
    )
    with zipfile.ZipFile(src_jar, "r") as zin, zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "META-INF/rtpduels-target.txt":
                continue
            zout.writestr(item, zin.read(item.filename))
        info = zipfile.ZipInfo("META-INF/rtpduels-target.txt", date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        zout.writestr(info, stamp)


def sheet_text(version, rows):
    lines = []
    a = lines.append
    a("# Uploading RTP Duels to Modrinth")
    a("")
    a("Project: https://modrinth.com/plugin/rtp-duels  (add each file below as a **new version** on it).")
    a("")
    a("The build gives you **3 files**: one for ALL of Paper, one for ALL of Bukkit and one for ALL of Spigot. "
      "All three contain the identical plugin, so it behaves exactly the same everywhere; they only differ in which "
      "loader you tick. Each one covers all %d game versions listed below (Minecraft 1.8 up to 26.3)." % len(rows[0]["mc"]))
    a("")
    a("For each file: **Create version** -> upload the file -> set the **Version number** -> tick the **Loader** -> "
      "tick **all** the game versions -> add the changelog (below) -> publish. PlaceholderAPI can be added as an "
      "*optional* dependency (only used to show the TimeSMP rank in the GUI).")
    a("")
    a("| # | File | Version number | Loader |")
    a("|---|------|----------------|--------|")
    for r in rows:
        a("| %d | `%s` | `%s` | %s |" % (r["n"], r["file"], r["version_number"], r["platform_name"]))
    a("")
    a("## Game versions to tick (the same list on all three)")
    a("")
    a(", ".join(rows[0]["mc"]))
    a("")
    a("**Before uploading:** run the *Test on real servers* workflow once and leave unticked any version that shows a red "
      "cross there. A version marked \"skipped\" just has no server download to test on.")
    a("")
    a("Folia is built into the same code (it adds `folia-supported: true`), so the Paper file also runs on Folia 1.19.4 "
      "and newer. Tick Folia on it only if you want Modrinth to list it.")
    a("")
    a("## Changelog text you can paste")
    a("")
    a("> Now supports Bukkit, Spigot and Paper on Minecraft 1.8 up to 26.3 (Java 8 or newer). Behaviour is unchanged: "
      "same chat buttons, confirmation GUI, countdowns, land-only random spot, command lock and teleport protection.")
    a("> On Paper the random spot is loaded asynchronously, so far-away chunks no longer pause the server.")
    a("> The plugin is now called RTPDuels (config folder `plugins/RTPDuels/`); permissions are unchanged.")
    a("")
    a("## Edit the project page once")
    a("")
    a("- **Requirements:** replace \"Paper 1.21+ and Java 21\" with \"Bukkit, Spigot or Paper - Minecraft 1.8 to 26.3 - Java 8 or newer\".")
    a("- Everything else (commands, permissions, features) stays accurate.")
    a("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", help="the built RTPDuels.jar")
    ap.add_argument("--out", help="folder for the per-version jars")
    ap.add_argument("--sheet", help="where to write MODRINTH_UPLOADS.md")
    ap.add_argument("--pom", default="pom.xml")
    args = ap.parse_args()

    version = project_version(args.pom)
    rows = []
    n = 0
    for pid, pname, label, mc in targets():
        n += 1
        rows.append({
            "n": n, "platform": pid, "platform_name": pname, "group": label, "mc": mc,
            "file": file_name(version, pid, label),
            "version_number": "%s-%s" % (version, pid),
        })

    if args.jar and args.out:
        if not os.path.isfile(args.jar):
            raise SystemExit("jar not found: " + args.jar)
        os.makedirs(args.out, exist_ok=True)
        seen = {}
        for r in rows:
            dest = os.path.join(args.out, r["file"])
            write_stamped_copy(args.jar, dest, version, r["platform"], r["group"], r["mc"])
            with zipfile.ZipFile(dest) as z:
                bad = z.testzip()
                if bad:
                    raise SystemExit("corrupt entry %s in %s" % (bad, dest))
            digest = hashlib.sha256(open(dest, "rb").read()).hexdigest()
            if digest in seen:
                raise SystemExit("duplicate checksum: %s == %s" % (r["file"], seen[digest]))
            seen[digest] = r["file"]
        print("wrote %d jars to %s" % (len(rows), args.out))

    if args.sheet:
        folder = os.path.dirname(args.sheet)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(args.sheet, "w") as f:
            f.write(sheet_text(version, rows))
        print("wrote " + args.sheet)


if __name__ == "__main__":
    sys.exit(main())
