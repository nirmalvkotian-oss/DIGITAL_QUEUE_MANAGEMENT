from flask import Flask, jsonify, render_template_string, request
from model import PriorityLevel, QueueManager

app = Flask(__name__)
manager = QueueManager()

# Pre-seed initial sample queue data
manager.generate_token(
    "Anita Sharma", 68, "General Medicine", PriorityLevel.PRIORITY
)
manager.generate_token(
    "Rahul Verma", 32, "General Medicine", PriorityLevel.NORMAL
)
manager.generate_token(
    "Baby Aarav", 2, "Pediatrics", PriorityLevel.EMERGENCY
)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Digital Queue System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .token-display { font-size: 2.2rem; font-weight: 700; color: #0d6efd; }
        .emergency-badge { background-color: #dc3545; color: #fff; }
        .priority-badge { background-color: #ffc107; color: #000; }
        .card { border-radius: 10px; border: none; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    </style>
</head>
<body class="p-4">
<div class="container-fluid">
    <header class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold text-dark">Central Healthcare Queue Display</h2>
        <span class="badge bg-success fs-6">Live Display Active</span>
    </header>

    <div class="row g-4">
        <!-- Token Registration Form -->
        <div class="col-md-4">
            <div class="card p-3">
                <h5 class="card-title fw-bold">Issue Patient Token</h5>
                <form id="tokenForm">
                    <div class="mb-2">
                        <label class="form-label">Patient Name</label>
                        <input type="text" class="form-control" id="pName" required placeholder="e.g. Ramesh Kumar">
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Age</label>
                        <input type="number" class="form-control" id="pAge" required placeholder="e.g. 45">
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Department</label>
                        <select class="form-select" id="pDept">
                            <option>General Medicine</option>
                            <option>Pediatrics</option>
                            <option>Orthopedics</option>
                            <option>Cardiology</option>
                            <option>Emergency</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Triage Priority</label>
                        <select class="form-select" id="pPriority">
                            <option value="3">Normal OP</option>
                            <option value="2">Priority (Senior Citizen / Infant)</option>
                            <option value="1">Emergency (Immediate)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Issue Token</button>
                </form>
            </div>
        </div>

        <!-- Department Queue Displays -->
        <div class="col-md-8">
            <div class="row g-3" id="departmentContainer"></div>
        </div>
    </div>
</div>

<script>
async function fetchQueueData() {
    try {
        const res = await fetch('/api/overview');
        const data = await res.json();
        const container = document.getElementById('departmentContainer');
        container.innerHTML = '';

        for (const [dept, info] of Object.entries(data)) {
            const activeToken = info.active ? info.active.token_id : '---';
            const activeName = info.active ? info.active.name : 'Waiting for next patient';
            
            let waitingRows = info.waiting_list.map(p => `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span><strong>${p.token_id}</strong> - ${p.name} (${p.age}y)</span>
                    <span class="badge ${p.priority === 'EMERGENCY' ? 'emergency-badge' : (p.priority === 'PRIORITY' ? 'priority-badge' : 'bg-secondary')}">${p.priority}</span>
                </li>
            `).join('');

            if (info.waiting_list.length === 0) {
                waitingRows = '<li class="list-group-item text-muted text-center">No patients in queue</li>';
            }

            container.innerHTML += `
                <div class="col-md-6">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="fw-bold mb-0">${dept}</h6>
                            <span class="badge bg-primary">Waiting: ${info.waiting_count}</span>
                        </div>
                        <hr class="my-2">
                        <div class="text-center py-2 bg-light rounded">
                            <small class="text-muted d-block">CURRENT CONSULTATION</small>
                            <div class="token-display">${activeToken}</div>
                            <small class="text-secondary fw-semibold">${activeName}</small>
                        </div>
                        <div class="mt-2 text-center">
                            <button class="btn btn-sm btn-outline-success w-100" onclick="callNext('${dept}')">Call Next Patient</button>
                        </div>
                        <h6 class="mt-3 mb-1 text-muted small fw-bold">NEXT IN QUEUE:</h6>
                        <ul class="list-group list-group-flush small" style="max-height: 150px; overflow-y: auto;">
                            ${waitingRows}
                        </ul>
                    </div>
                </div>
            `;
        }
    } catch (err) {
        console.error('Queue sync error:', err);
    }
}

document.getElementById('tokenForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('pName').value,
        age: parseInt(document.getElementById('pAge').value),
        department: document.getElementById('pDept').value,
        priority: parseInt(document.getElementById('pPriority').value)
    };

    const res = await fetch('/api/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    if (res.ok) {
        document.getElementById('tokenForm').reset();
        fetchQueueData();
    }
});

async function callNext(dept) {
    await fetch(`/api/next?department=${encodeURIComponent(dept)}`, { method: 'POST' });
    fetchQueueData();
}

setInterval(fetchQueueData, 3000);
fetchQueueData();
</script>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/overview", methods=["GET"])
def get_overview():
    return jsonify(manager.get_system_overview())


@app.route("/api/token", methods=["POST"])
def issue_token():
    data = request.json or {}
    name = data.get("name")
    age = data.get("age")
    dept = data.get("department")
    priority_val = int(data.get("priority", PriorityLevel.NORMAL))

    if not name or not age or not dept:
        return jsonify({"error": "Missing required fields"}), 400

    priority = PriorityLevel(priority_val)
    patient = manager.generate_token(name, age, dept, priority)
    return jsonify(patient.to_dict()), 201


@app.route("/api/next", methods=["POST"])
def call_next():
    dept = request.args.get("department")
    if not dept:
        return jsonify({"error": "Department is required"}), 400

    patient = manager.call_next_patient(dept)
    if not patient:
        return jsonify({"message": "No patients in queue", "patient": None}), 200

    return jsonify({"patient": patient.to_dict()}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)