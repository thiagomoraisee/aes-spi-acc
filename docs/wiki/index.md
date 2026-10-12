<p align="center">
  <img src="assets/ciexpert.png" alt="LOGO" width="200" height="auto">
</p>

# AES SPI Accelerator Wiki

This is a self-hosted **Wiki** page for `AES SPI Accelerator` project. Its main objective is to serve as an interactive documentation and knowledge base for both newcomers and project managers. 

Here you will find study notes, guidelines, FAQs, weekly reports, specification and block informations.  
Feel free to explore and dive into this exciting projecto

## About The Project

This project is a low-power cryptographic accelerator featuring an *Advanced Encription Standard* (AES) datapath, custom clock and reset management blocks, and a *Serial Peripheral Interface* (SPI) interface for configuration, control and SoC integration. Developed as part of 2026 CIExpert RTL design track, this module is designed to be verified by a design verification member, following a standard ASIC digital design flow using the Synopsys tools. Advanced low-power techniques are exploited from power intent via UPF, architectural and RTL development, logic synthesis and formal netlist validation.

## Getting Started

Follow the steps below for setup your local machine to work with PRISM:

0. Install dependencies
```
pip install mkdocs mkdocs-material
```

1. Clone the repository
```
git clone https://github.com/thiagomoraisee/aes-spi-acc.git
```

2. Create/check reference flow structure (one time per clone):
```
cd aes-spi-acc/workspace
make flow
```
> Note: This will check artifacts and create the directories tree (if needed).

## Project Directories Structure

The project is structured according to the Reference flow, with accordance with the suggested folders of CIExpert RTL Design track.

```
aes-spi-acc             # Repository top level
├── docs                # Documentation artifacts
│   ├── architecture    # Microarchitecture and power supply architecture
│   ├── reports         # Follow-up weekly reports
│   ├── spec            # Functional specification
│   └── wiki            # MKDocs Wiki
├── formal              # Formality scripts and reports
├── model               # Imported behavioral models (memory, PLL, etc)
├── power               # UPF files and reports
├── rtl                 # RTL artifacts
│   ├── pkg             # RTL packages and dependencies
│   ├── src             # RTL source codes
│   └── tb              # Testbenches
├── scripts             # Automation flow scripts
├── synth               # SDC, scripts and synthesis repots
└── workspace           # Work directory
```
