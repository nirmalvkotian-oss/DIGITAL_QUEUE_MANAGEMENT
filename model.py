import heapq
from datetime import datetime
from enum import IntEnum
from typing import Dict, List, Optional


class PriorityLevel(IntEnum):
    EMERGENCY = 1  # Highest priority
    PRIORITY = 2  # Elderly, infants, pregnant patients
    NORMAL = 3  # Standard OP consultation


class Patient:

    def __init__(
        self,
        token_id: str,
        name: str,
        age: int,
        department: str,
        priority: PriorityLevel,
    ):
        self.token_id = token_id
        self.name = name
        self.age = age
        self.department = department
        self.priority = priority
        self.timestamp = datetime.now()
        self.status = "Waiting"  # 'Waiting', 'In-Consultation', 'Completed'

    def __lt__(self, other: "Patient"):
        # Emergency and priority cases served first; ties broken by arrival time
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.timestamp < other.timestamp

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "priority": self.priority.name,
            "status": self.status,
            "arrival_time": self.timestamp.strftime("%H:%M:%S"),
        }


class QueueManager:

    def __init__(self):
        self.queues: Dict[str, List[Patient]] = {
            "General Medicine": [],
            "Pediatrics": [],
            "Orthopedics": [],
            "Cardiology": [],
            "Emergency": [],
        }
        self.active_consultations: Dict[str, Optional[Patient]] = {
            dept: None for dept in self.queues
        }
        self.token_counters: Dict[str, int] = {
            dept: 100 for dept in self.queues
        }
        self.completed_patients: List[Patient] = []

    def generate_token(
        self,
        name: str,
        age: int,
        department: str,
        priority: PriorityLevel = PriorityLevel.NORMAL,
    ) -> Patient:
        if department not in self.queues:
            raise ValueError(f"Department '{department}' does not exist.")

        self.token_counters[department] += 1
        prefix = department[:3].upper()
        token_id = f"{prefix}-{self.token_counters[department]}"

        patient = Patient(
            token_id=token_id,
            name=name,
            age=age,
            department=department,
            priority=priority,
        )
        heapq.heappush(self.queues[department], patient)
        return patient

    def call_next_patient(self, department: str) -> Optional[Patient]:
        if department not in self.queues:
            return None

        # Mark active consultation as completed
        if self.active_consultations[department]:
            prev = self.active_consultations[department]
            prev.status = "Completed"
            self.completed_patients.append(prev)
            self.active_consultations[department] = None

        if self.queues[department]:
            next_patient = heapq.heappop(self.queues[department])
            next_patient.status = "In-Consultation"
            self.active_consultations[department] = next_patient
            return next_patient

        return None

    def get_waiting_list(self, department: str) -> List[dict]:
        if department not in self.queues:
            return []
        sorted_queue = sorted(self.queues[department])
        return [p.to_dict() for p in sorted_queue]

    def get_system_overview(self) -> dict:
        return {
            dept: {
                "active": (
                    self.active_consultations[dept].to_dict()
                    if self.active_consultations[dept]
                    else None
                ),
                "waiting_count": len(self.queues[dept]),
                "waiting_list": self.get_waiting_list(dept),
            }
            for dept in self.queues
        }