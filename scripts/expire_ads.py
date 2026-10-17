import json
from datetime import datetime, timezone
from pathlib import Path

path = Path("ads.json")
document = json.loads(path.read_text(encoding="utf-8"))
now = datetime.now(timezone.utc)


def is_expired(item: dict) -> bool:
    raw = item.get("expires_at")
    if not isinstance(raw, str) or not raw.strip():
        return False
    try:
        moment = datetime.fromisoformat(raw.strip())
    except ValueError:
        return False
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment <= now


original = document.get("ads", [])
kept = [item for item in original if not is_expired(item)]
document["ads"] = kept
path.write_text(
    json.dumps(document, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"removed {len(original) - len(kept)} expired advertisement(s), {len(kept)} remaining")
