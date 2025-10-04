# Project Sentinel - Retail Analytics & Optimization Platform

🛒 **A comprehensive real-time retail analytics system for anomaly detection and operational optimization.**

## Overview

Project Sentinel processes live data from 7 in-store sensors to detect retail challenges and provide actionable insights:

- **🔍 Anomaly Detection**: Scanner avoidance, barcode switching, weight discrepancies
- **⚠️ System Monitoring**: Crashes, errors, and operational issues
- **👥 Customer Experience**: Queue optimization and wait time analysis
- **📊 Business Intelligence**: Inventory tracking and staffing recommendations

## Quick Start

```bash
# Clone and navigate to project
cd zebra/evidence/executables

# Run complete demo (includes batch + real-time processing)
python3 run_demo.py

# View results
cat ../output/test/events.jsonl     # Test dataset results
cat ../output/final/events.jsonl   # Real-time results
```

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Streaming      │───▶│   Detection     │
│                 │    │  Client         │    │   Engine        │
│ • RFID          │    │                 │    │                 │
│ • POS           │    │ • Normalizes    │    │ • 8 Algorithms  │
│ • Queue         │    │ • Correlates    │    │ • @algorithm    │
│ • Recognition   │    │ • Timestamps    │    │   Tagged        │
│ • Inventory     │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐           │
│  Web Dashboard  │◀───│ Event Generator │◀──────────┘
│                 │    │                 │
│ • Real-time UI  │    │ • events.jsonl  │
│ • Alerts        │    │ • JSON Format   │
│ • Visualizations│    │ • Submissions   │
└─────────────────┘    └─────────────────┘
```

## Detection Algorithms

All algorithms are tagged with `# @algorithm Name | Purpose` for automated scoring:

| Algorithm                 | Purpose                   | Trigger Condition                       |
| ------------------------- | ------------------------- | --------------------------------------- |
| **Scanner Avoidance**     | Detects unscanned items   | RFID in scan area ∧ No POS transaction  |
| **Barcode Switching**     | Identifies price fraud    | Scanned price << Expected price         |
| **Weight Discrepancy**    | Validates product weights | \|Actual - Expected\| > 50g             |
| **System Crash**          | Monitors system health    | Status = "System Crash" \| "Read Error" |
| **Queue Length**          | Optimizes customer flow   | Customer count ≥ 4                      |
| **Wait Time**             | Improves experience       | Dwell time ≥ 300 seconds                |
| **Inventory Tracking**    | Stock management          | Variance > 10% from expected            |
| **Staffing Optimization** | Resource allocation       | 70%+ stations busy                      |

## Key Features

### 🔄 Real-Time Processing

- Connects to streaming server on port 8765
- Processes 7 heterogeneous data sources
- 30-second correlation windows
- Live event generation

### 📊 Analytics Dashboard

- Real-time store overview
- Station status monitoring
- Alert prioritization (Red/Yellow/Green)
- Event tracking and metrics

### 🎯 Event Generation

- JSON Lines format output
- Matches required schema exactly
- Test and final dataset processing
- Comprehensive event types

### 🏗️ Modular Architecture

- **streaming_client.py**: TCP connection and data ingestion
- **data_parser.py**: Multi-format data normalization
- **data_correlator.py**: Time-based event correlation
- **detection_engine.py**: 8 tagged algorithms
- **event_generator.py**: JSON output formatting
- **dashboard.py**: Web-based visualization
- **sentinel_system.py**: Main orchestrator

## File Structure

```
zebra/
├── src/                           # Complete source code
│   ├── streaming_client.py        # TCP streaming connection
│   ├── data_parser.py            # Data normalization
│   ├── data_correlator.py        # Event correlation
│   ├── detection_engine.py       # 8 detection algorithms
│   ├── event_generator.py        # JSON output generation
│   ├── dashboard.py              # Web dashboard
│   └── sentinel_system.py        # Main system coordinator
├── evidence/
│   ├── output/
│   │   ├── test/events.jsonl     # Test dataset results
│   │   └── final/events.jsonl    # Final dataset results
│   ├── screenshots/              # Dashboard screenshots
│   └── executables/
│       └── run_demo.py           # Single execution script
├── data/                         # Development data (not in submission)
│   ├── input/                    # Sample datasets
│   └── streaming-server/         # Data streaming service
└── SUBMISSION_GUIDE.md           # Detailed submission info
```

## Technical Specifications

- **Language**: Python 3.6+ (standard library only)
- **Dependencies**: No external packages required
- **Data Sources**: 7 streams (RFID, POS, Queue, Recognition, Inventory, Products, Customers)
- **Output Format**: JSON Lines (.jsonl)
- **Processing Modes**: Batch and real-time streaming
- **Dashboard**: HTML/CSS/JavaScript web interface

## Results

The system successfully:

- ✅ Processes all 7 data sources in real-time
- ✅ Detects 8 types of retail anomalies
- ✅ Generates properly formatted events.jsonl
- ✅ Provides actionable business insights
- ✅ Visualizes data through web dashboard
- ✅ Executes with single command for judges

## Sample Output

```json
{"timestamp":"2025-08-13T16:00:01","event_id":"E000","event_data":{"event_name":"Success Operation","station_id":"SCC1","customer_id":"C056","product_sku":"PRD_F_14"}}
{"timestamp":"2025-08-13T16:00:04","event_id":"E001","event_data":{"event_name":"Scanner Avoidance","station_id":"SCC1","customer_id":"Unknown","product_sku":"PRD_T_03"}}
```

## Live Demo

For judges' 2-minute walkthrough:

1. **Execute**: `python3 run_demo.py` (30 seconds)
2. **Show algorithms**: Display @algorithm tags (45 seconds)
3. **Dashboard**: Real-time visualization (30 seconds)
4. **Verify results**: Check events.jsonl outputs (15 seconds)

---

**🎯 Ready for submission and live demonstration!**
# zebra-innovateX-2
