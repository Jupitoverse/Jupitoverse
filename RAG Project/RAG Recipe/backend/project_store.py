"""Per-project storage: config, vectorstore, documents, monitoring. Independent of core code."""
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from config import (
    PROJECT_DATA_DIR,
    ARCHIVE_DIR,
    ARCHIVE_DAYS_BEFORE_DELETE,
    CONFIG_FILE,
    CHROMA_DIR,
    DOCUMENTS_DIR,
    EXCEL_HISTORY_DIR,
    MONITORING_FILE,
)


def ensure_dirs():
    PROJECT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def project_dir(project_id: str) -> Path:
    return PROJECT_DATA_DIR / project_id


def project_config_path(project_id: str) -> Path:
    return project_dir(project_id) / CONFIG_FILE


def project_chroma_path(project_id: str) -> Path:
    return project_dir(project_id) / CHROMA_DIR


def project_documents_path(project_id: str) -> Path:
    return project_dir(project_id) / DOCUMENTS_DIR


def project_excel_history_path(project_id: str) -> Path:
    return project_dir(project_id) / EXCEL_HISTORY_DIR


def project_monitoring_path(project_id: str) -> Path:
    return project_dir(project_id) / MONITORING_FILE


def list_projects(include_archived: bool = False) -> List[Dict[str, Any]]:
    ensure_dirs()
    result = []
    for p in PROJECT_DATA_DIR.iterdir():
        if not p.is_dir():
            continue
        project_id = p.name
        cfg_path = p / CONFIG_FILE
        if not cfg_path.exists():
            continue
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            continue
        archived = cfg.get("archived", False)
        if archived and not include_archived:
            continue
        result.append({
            "project_id": project_id,
            "name": cfg.get("name", project_id),
            "created_at": cfg.get("created_at", ""),
            "archived": archived,
            "archived_at": cfg.get("archived_at"),
        })
    return result


def create_project(project_id: str, name: str, config: Dict[str, Any]) -> Path:
    ensure_dirs()
    root = project_dir(project_id)
    root.mkdir(parents=True, exist_ok=True)
    (root / DOCUMENTS_DIR).mkdir(exist_ok=True)
    (root / EXCEL_HISTORY_DIR).mkdir(exist_ok=True)
    config["project_id"] = project_id
    config["name"] = name
    config["created_at"] = datetime.utcnow().isoformat() + "Z"
    config["archived"] = False
    with open(root / CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    # Initialize monitoring
    monitoring = {
        "project_id": project_id,
        "total_calls": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cost_usd": 0.0,
        "today_calls": 0,
        "today_input_tokens": 0,
        "today_output_tokens": 0,
        "today_cost_usd": 0.0,
        "last_call_at": None,
        "last_call_tokens": 0,
        "last_call_cost": 0.0,
        "history": [],
    }
    with open(project_monitoring_path(project_id), "w", encoding="utf-8") as f:
        json.dump(monitoring, f, indent=2)
    return root


def get_project_config(project_id: str) -> Optional[Dict[str, Any]]:
    path = project_config_path(project_id)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def update_project_config(project_id: str, updates: Dict[str, Any]) -> bool:
    cfg = get_project_config(project_id)
    if not cfg:
        return False
    cfg.update(updates)
    with open(project_config_path(project_id), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return True


def archive_project(project_id: str) -> bool:
    cfg = get_project_config(project_id)
    if not cfg:
        return False
    cfg["archived"] = True
    cfg["archived_at"] = datetime.utcnow().isoformat() + "Z"
    with open(project_config_path(project_id), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return True


def delete_archived_older_than_days() -> List[str]:
    """Permanently delete archived projects older than ARCHIVE_DAYS_BEFORE_DELETE. Returns list of deleted project_ids."""
    ensure_dirs()
    cutoff = datetime.utcnow() - timedelta(days=ARCHIVE_DAYS_BEFORE_DELETE)
    deleted = []
    for p in PROJECT_DATA_DIR.iterdir():
        if not p.is_dir():
            continue
        cfg = get_project_config(p.name)
        if not cfg or not cfg.get("archived"):
            continue
        archived_at = cfg.get("archived_at")
        if not archived_at:
            continue
        try:
            dt = datetime.fromisoformat(archived_at.replace("Z", "+00:00"))
            if dt.replace(tzinfo=None) < cutoff:
                shutil.rmtree(p, ignore_errors=True)
                deleted.append(p.name)
        except Exception:
            pass
    return deleted


def get_monitoring(project_id: str) -> Optional[Dict[str, Any]]:
    path = project_monitoring_path(project_id)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def append_monitoring(
    project_id: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cost_usd: float = 0.0,
):
    path = project_monitoring_path(project_id)
    if not path.exists():
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            m = json.load(f)
    except Exception:
        return
    now = datetime.utcnow()
    today_key = now.strftime("%Y-%m-%d")
    m["total_calls"] = m.get("total_calls", 0) + 1
    m["total_input_tokens"] = m.get("total_input_tokens", 0) + input_tokens
    m["total_output_tokens"] = m.get("total_output_tokens", 0) + output_tokens
    m["total_cost_usd"] = m.get("total_cost_usd", 0) + cost_usd
    m["last_call_at"] = now.isoformat() + "Z"
    m["last_call_tokens"] = input_tokens + output_tokens
    m["last_call_cost"] = cost_usd
    if m.get("last_date") != today_key:
        m["last_date"] = today_key
        m["today_calls"] = 0
        m["today_input_tokens"] = 0
        m["today_output_tokens"] = 0
        m["today_cost_usd"] = 0.0
    m["today_calls"] += 1
    m["today_input_tokens"] += input_tokens
    m["today_output_tokens"] += output_tokens
    m["today_cost_usd"] = m.get("today_cost_usd", 0) + cost_usd
    m["history"] = (m.get("history") or [])[-99:]  # keep last 100
    m["history"].append({
        "at": m["last_call_at"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd,
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)
