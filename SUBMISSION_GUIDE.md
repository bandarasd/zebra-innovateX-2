# Team##\_sentinel Submission Guide

> **Prerequisites completed:** ✅ Reviewed project-sentinel.pdf ✅ Set up development environment ✅ Tested with sample data

## Team Information

**Team ID:** <ENTER TEAM ID>  
**Team Name:** <ENTER TEAM NAME>  
**Team Members:**

- <ENTER MEMBER 1 NAME> - <ENTER ROLE>
- <ENTER MEMBER 2 NAME> - <ENTER ROLE>
- <ENTER MEMBER 3 NAME> - <ENTER ROLE>
- <ENTER MEMBER 4 NAME> - <ENTER ROLE>

## Solution Overview

Our Project Sentinel solution implements a comprehensive retail analytics system that processes 7 real-time data streams to detect anomalies and provide actionable insights. The system successfully identifies:

- **Scanner Avoidance**: Correlates RFID readings with POS transactions to detect unscanned items
- **Barcode Switching**: Compares actual product prices with scanned prices to identify fraud
- **Weight Discrepancies**: Validates product weights against expected values
- **System Crashes**: Monitors system status for failures and errors
- **Queue Management**: Analyzes customer counts and wait times for optimization
- **Inventory Discrepancies**: Compares expected vs actual inventory levels
- **Staffing Optimization**: Recommends staffing adjustments based on traffic patterns

## Technical Architecture

**Core Components:**

- **Streaming Client**: Connects to TCP port 8765 for real-time data ingestion
- **Data Parser**: Normalizes 7 heterogeneous data sources (RFID, POS, Queue, Recognition, Inventory, Products, Customers)
- **Data Correlator**: Time-based correlation engine with 30-second windows
- **Detection Engine**: 8 algorithms with proper @algorithm tags for automated scoring
- **Event Generator**: Produces events.jsonl in required format
- **Web Dashboard**: Real-time visualization of store status and alerts

**Programming Languages:** Python 3.6+ (backend), HTML/CSS/JavaScript (dashboard)
**Dependencies:** Python standard library only - no external packages required

## Algorithm Implementation

All algorithms are properly tagged with `# @algorithm Name | Purpose` format:

1. **Scanner Avoidance Detection**: Correlates RFID readings with POS transactions
2. **Barcode Switching Detection**: Price comparison analysis between products
3. **Weight Discrepancy Detection**: Weight validation against product database
4. **System Crash Detection**: Status monitoring for system failures
5. **Queue Length Analysis**: Customer count threshold monitoring
6. **Wait Time Analysis**: Dwell time analysis for customer experience
7. **Inventory Discrepancy Detection**: Stock level variance analysis
8. **Staffing Optimization**: Traffic-based staffing recommendations

## Dashboard Features

Our web dashboard provides:

- **Real-time Store Overview**: Station status, customer counts, event metrics
- **Alert System**: Color-coded priority alerts (Red: Critical, Yellow: Warning, Green: Normal)
- **Station Monitoring**: Individual station status with customer and wait time metrics
- **Event Tracking**: Live event feed with timestamps and details
- **Performance Metrics**: System-wide analytics and insights

## Execution Instructions

**Single Command Execution:**

```bash
cd evidence/executables
python3 run_demo.py
```

**What the demo does:**

1. Validates system dependencies and file structure
2. Runs batch processing on sample data → generates `evidence/output/test/events.jsonl`
3. Starts streaming server for real-time demo
4. Processes live data streams for 30 seconds → generates `evidence/output/final/events.jsonl`
5. Displays comprehensive results summary

**System Requirements:**

- Python 3.6 or higher
- No external dependencies (uses standard library only)
- Approximately 50MB disk space
- Network access for streaming server (localhost:8765)

## Results Summary

**Test Dataset Results:**

- Successfully processed <ENTER NUMBER> events from sample data
- Detected <ENTER NUMBER> anomalies across all categories
- Generated properly formatted events.jsonl output

**Final Dataset Results:**

- Real-time processing of live data streams
- <ENTER NUMBER> events generated during 30-second demo
- All detection algorithms functioning correctly

**Key Achievements:**
✅ Real-time data stream processing  
✅ Multi-source data correlation  
✅ 8 detection algorithms with proper tagging  
✅ Event generation in required JSON format  
✅ Web dashboard with live visualization  
✅ Modular, well-documented codebase  
✅ Single-command execution for judges

## Files Generated

- `evidence/output/test/events.jsonl` - Test dataset results
- `evidence/output/final/events.jsonl` - Final dataset results
- `evidence/screenshots/` - Dashboard screenshots (to be added)
- `src/` - Complete source code with algorithm tags
- `evidence/executables/run_demo.py` - Single execution script

## Judging Preparation

**For the 2-minute walkthrough:**

1. **Demo execution** (30 seconds): Run `python3 run_demo.py`
2. **Algorithm explanation** (45 seconds): Show @algorithm tags in detection_engine.py
3. **Dashboard showcase** (30 seconds): Display real-time analytics interface
4. **Results verification** (15 seconds): Confirm events.jsonl outputs

**Judge Commands:**

```bash
# Navigate to submission folder
cd Team##_sentinel/evidence/executables

# Single command to run complete demo
python3 run_demo.py

# View generated events
cat ../output/test/events.jsonl
cat ../output/final/events.jsonl

# Optional: Check algorithm tags
grep -r "@algorithm" ../../src/
```

## Contact Information

**Primary Contact:** <ENTER PRIMARY CONTACT NAME>  
**Email:** <ENTER EMAIL>  
**Phone:** <ENTER PHONE>

---

_This submission demonstrates a production-ready retail analytics system capable of real-time anomaly detection and operational optimization._
