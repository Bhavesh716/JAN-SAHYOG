# JAN SAHYOG — Hardware Design

## 1. Purpose

The AI Seva Kiosk provides a simple, physical access point for rural users who may not own a smartphone or feel comfortable typing. It combines a display, voice input/output, and optional document capture with a backend AI service.

## 2. Proposed Hardware

| Component | Role | Notes |
|---|---|---|
| 21.5–32 inch touchscreen | Main user interface | Choose a sunlight/readability-appropriate panel for the installation site |
| Kiosk compute unit | Runs kiosk UI | Android/Linux mini PC or industrial panel PC; size to be selected |
| Microphone | Captures voice queries | Noise handling matters in public locations |
| Speaker | Speaks responses | Include volume control and audible clarity |
| Camera | Optional document/visual input | Do not use facial recognition by default |
| Document/QR scanner | Captures supported forms or codes | Confirm format and integration requirements |
| ESP32-S3 | Embedded controller | Suitable for peripherals and device control, not a large-screen UI or server-scale LLM |
| Cellular modem/SIM | Internet connectivity | Verify network bands, coverage, and data plan |
| Wi-Fi/Ethernet | Alternative connectivity | Depends on the site |
| Power supply/UPS | Stable power | Size based on actual display and compute power draw |
| Enclosure and mounting | Physical protection | Consider ventilation, accessibility, maintenance, and tamper resistance |

## 3. Logical Hardware Layout

```text
Touchscreen + Microphone + Speaker + Optional Scanner
                       |
                       v
                Kiosk Compute Unit
              (UI and input handling)
                       |
                Local device link
                       |
                       v
                ESP32-S3 Controller
             (peripherals / device status)

Kiosk Compute Unit
       |
       v
Cellular Modem / Wi-Fi / Ethernet
       |
       v
JAN SAHYOG Backend Server
```

The exact connection between the kiosk compute unit, modem, and ESP32 depends on the selected hardware. The ESP32 can communicate with suitable peripherals over supported interfaces, but should not be assumed to power or directly drive any arbitrary large touchscreen.

## 4. Connectivity and Limited Internet

- Use cellular connectivity where wired internet is unavailable.
- Provide Wi-Fi or Ethernet where practical.
- Cache only approved, non-sensitive information for offline access.
- Clearly label cached information with its last update date.
- Synchronize when connectivity returns.
- Do not promise live scheme status or current eligibility checks while offline.

LoRa may be evaluated for low-bandwidth structured data in specific deployments. It is not a substitute for carrying ordinary voice calls or full kiosk UI traffic.

## 5. Privacy and Physical Safety

- Do not enable facial recognition as a default feature.
- Avoid saving document images after processing unless necessary and authorized.
- Secure service ports and internal components.
- Provide safe cable routing, ventilation, and stable mounting.
- Use access controls for maintenance.
- Protect the kiosk from power interruptions and unexpected shutdowns.

## 6. Prototype Validation Checklist

- Touchscreen remains responsive during normal use.
- Microphone captures speech in realistic background noise.
- Speaker output is understandable.
- Scanning works for the intended document types.
- Cellular reconnection works after network loss.
- Power supply handles measured peak load.
- The kiosk UI recovers after a restart.
- No secrets are stored in public client files.
- Users can identify when information is offline or out of date.
