"""Generate and analyze a fixed HR attrition practice dataset."""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED = 20250830
EMPLOYEES = 1_470


def choose(rng: random.Random, values: list[str], weights: list[float]) -> str:
    return rng.choices(values, weights=weights, k=1)[0]


def generate() -> list[dict[str, object]]:
    rng = random.Random(SEED)
    roles = {
        "Sales": ["Sales Executive", "Sales Representative"],
        "Research & Development": ["Research Scientist", "Laboratory Technician", "Research Director"],
        "Human Resources": ["Human Resources", "Manager"],
    }
    rows: list[dict[str, object]] = []
    for index in range(1, EMPLOYEES + 1):
        department = choose(rng, list(roles), [0.31, 0.63, 0.06])
        job_role = rng.choice(roles[department])
        age = max(18, min(60, round(rng.gauss(36, 8))))
        years = min(age - 18, max(0, round(rng.triangular(0, 32, 4))))
        overtime = "Yes" if rng.random() < 0.29 else "No"
        marital = choose(rng, ["Single", "Married", "Divorced"], [0.32, 0.48, 0.20])
        monthly_income = round(2300 + years * 310 + rng.uniform(-900, 4600), 2)

        probability = 0.055
        if overtime == "Yes":
            probability += 0.145
        if years < 2:
            probability += 0.115
        if job_role == "Sales Representative":
            probability += 0.085
        if job_role == "Laboratory Technician":
            probability += 0.050
        if age < 30:
            probability += 0.045
        if marital == "Single":
            probability += 0.030
        attrition = "Yes" if rng.random() < min(probability, 0.72) else "No"

        rows.append({
            "employee_id": f"EMP-{index:04d}",
            "age": age,
            "department": department,
            "job_role": job_role,
            "overtime": overtime,
            "years_at_company": years,
            "monthly_income": monthly_income,
            "marital_status": marital,
            "attrition": attrition,
        })
    return rows


def attrition_rate(rows: list[dict[str, object]]) -> float:
    return sum(row["attrition"] == "Yes" for row in rows) / len(rows)


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    by_overtime: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_department: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_role: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_overtime[str(row["overtime"])].append(row)
        by_department[str(row["department"])].append(row)
        by_role[str(row["job_role"])].append(row)
    attrited = [row for row in rows if row["attrition"] == "Yes"]
    return {
        "data_type": "generated",
        "seed": SEED,
        "employees": len(rows),
        "overall_attrition_rate": round(attrition_rate(rows), 6),
        "overtime_attrition_rates": {key: round(attrition_rate(value), 6) for key, value in sorted(by_overtime.items())},
        "department_attrition_rates": {key: round(attrition_rate(value), 6) for key, value in sorted(by_department.items())},
        "role_attrition_rates": {key: round(attrition_rate(value), 6) for key, value in sorted(by_role.items())},
        "under_2_year_share_of_attrition": round(sum(int(row["years_at_company"]) < 2 for row in attrited) / len(attrited), 6),
    }


def write_dashboard(summary: dict[str, object]) -> None:
    overall = float(summary["overall_attrition_rate"])
    overtime = summary["overtime_attrition_rates"]
    departments = summary["department_attrition_rates"]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="610" viewBox="0 0 1100 610">',
        '<rect width="1100" height="610" fill="#F5F7FA"/>',
        '<rect x="0" y="0" width="1100" height="92" fill="#11233F"/>',
        '<text x="55" y="57" font-family="Arial" font-size="30" font-weight="700" fill="#FFFFFF">HR Attrition Dashboard</text>',
        '<text x="55" y="125" font-family="Arial" font-size="15" fill="#5B6577">1,470 employees | fixed practice dataset</text>',
        '<rect x="55" y="155" width="300" height="120" rx="8" fill="#E7F4F2" stroke="#0F766E"/>',
        '<text x="78" y="193" font-family="Arial" font-size="17" font-weight="700" fill="#0F766E">Overall attrition</text>',
        f'<text x="78" y="246" font-family="Arial" font-size="42" font-weight="700" fill="#172033">{overall:.1%}</text>',
        '<rect x="385" y="155" width="300" height="120" rx="8" fill="#FFF0E7" stroke="#E07A3F"/>',
        '<text x="408" y="193" font-family="Arial" font-size="17" font-weight="700" fill="#E07A3F">Overtime attrition</text>',
        f'<text x="408" y="246" font-family="Arial" font-size="42" font-weight="700" fill="#172033">{float(overtime["Yes"]):.1%}</text>',
        '<rect x="715" y="155" width="330" height="120" rx="8" fill="#EAF0F6" stroke="#375A7F"/>',
        '<text x="738" y="193" font-family="Arial" font-size="17" font-weight="700" fill="#375A7F">No-overtime attrition</text>',
        f'<text x="738" y="246" font-family="Arial" font-size="42" font-weight="700" fill="#172033">{float(overtime["No"]):.1%}</text>',
        '<text x="55" y="330" font-family="Arial" font-size="23" font-weight="700" fill="#11233F">Attrition rate by department</text>',
    ]
    labels = ["Human Resources", "Research & Development", "Sales"]
    for index, label in enumerate(labels):
        value = float(departments[label])
        y = 370 + index * 66
        width = value * 2600
        parts.extend([
            f'<text x="55" y="{y + 25}" font-family="Arial" font-size="16" fill="#172033">{escape(label)}</text>',
            f'<rect x="285" y="{y}" width="{width:.1f}" height="34" rx="4" fill="#0F766E"/>',
            f'<text x="{300 + width:.1f}" y="{y + 24}" font-family="Arial" font-size="16" font-weight="700" fill="#172033">{value:.1%}</text>',
        ])
    parts.append('<text x="55" y="585" font-family="Arial" font-size="13" fill="#5B6577">Generated by scripts/generate_and_analyze.py with fixed seed 20250830.</text>')
    parts.append("</svg>")
    (ROOT / "visuals" / "dashboard.svg").write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    for folder in ["data", "outputs", "visuals"]:
        (ROOT / folder).mkdir(exist_ok=True)
    rows = generate()
    with (ROOT / "data" / "hr_attrition.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = summarize(rows)
    (ROOT / "outputs" / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_dashboard(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
