# Parrot Tester

Parrot Tester is a tool to help you analyze your parrot noises by providing details of each frame.

Say "parrot tester" to toggle the UI and start testing!

## Prerequisites
- Talon beta
- A `parrot_integration.py` file anywhere in your Talon user directory (will be auto discovered)
- A `patterns.json` file anywhere in your Talon user directory (will be auto discovered)

## Installation

Download or clone this repository into your Talon user directory. This tool depends on the `talon-ui-elements` library for the UI, so we will clone that as well.

```bash
# mac and linux
cd ~/.talon/user

# windows
cd ~/AppData/Roaming/talon/user

git clone https://github.com/rokubop/parrot_tester.git
git clone https://github.com/rokubop/talon-ui-elements.git
```

Done! You can now use the Parrot Tester tool. 🎉

Say "parrot tester" to toggle the UI and start testing!

## How it works

A spy is attached to your existing `parrot_integration.py` file upon UI launch, and restored when the UI is closed. Your `parrot_integration.py` and `patterns.json` files are not modified in any way. If you somehow get into an error state, a Talon restart will restore everything to normal.