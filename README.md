
# Healthcare Digital Queue Management System (DQMS)

An intelligent, priority-based digital queue management system designed for healthcare facilities, outpatient departments (OPDs), and emergency triage centers. The system minimizes patient wait times, prevents waiting area congestion, and ensures urgent medical cases are prioritized dynamically over routine checkups.

---

## 📌 Problem Statement

Traditional first-come, first-served queue setups in hospitals lead to:
- Long, unmanaged physical queues in reception and OPD zones.
- Delays in identifying and serving high-risk, elderly, or critical emergency patients.
- Lack of real-time visibility for both patients in waiting halls and doctors inside consultation rooms.

This system resolves this by combining triage-based priority queuing with automated department routing and live status screens.

---

## 🚀 Key Features

- **Triage-Driven Scheduling:** Uses priority-heap data structures to automatically surface high-urgency patients ahead of routine appointments.
  - **Level 1 (Emergency):** Bypasses standard waitlists for immediate attention.
  - **Level 2 (Priority):** Senior citizens, pregnant women, and pediatric cases.
  - **Level 3 (Normal OP):** Standard checkup consultations ordered by arrival time.
- **Multi-Department Support:** Manages isolated queues for General Medicine, Pediatrics, Orthopedics, Cardiology, and Emergency units.
- **Live Waiting Hall Display:** Auto-refreshes active consultations and displays the next patients in line.
- **Doctor Consultation Controls:** One-click token calling that updates consultation records and moves the queue forward.
- **RESTful Architecture:** Ready for integration with registration kiosks, hospital management information systems (HMIS), or SMS notification gateways.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask
- **Algorithm & Data Structures:** Python standard `heapq` (Min-Heap for O(log n) insertion and removal), `datetime` for FIFO tie-breaking
- **Frontend:** HTML5, Vanilla JavaScript (Fetch API polling), Bootstrap 5

---

## 📁 Repository Structure

```text
DIGITAL_QUEUE_MANAGEMENT/
├── .gitignore          # Git exclusion rules
├── LICENSE             # Project licensing terms
├── README.md           # System documentation and operational runbook
├── model.py            # Patient models, priority logic, and queue operations
└── app.py              # Flask REST API endpoints and dashboard UI