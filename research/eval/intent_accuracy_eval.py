import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "backend"))
from app.nlu.intent_classifier import classify_intent

dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "codemix_test_set.json")

with open(dataset_path, encoding="utf-8") as f:
    data = json.load(f)

buckets = {}
overall_correct = 0

for item in data:
    bucket = item["cmi_bucket"]
    predicted = classify_intent(item["text"])["intent"]
    correct = predicted == item["intent"]

    buckets.setdefault(bucket, {"correct": 0, "total": 0})
    buckets[bucket]["total"] += 1
    buckets[bucket]["correct"] += int(correct)
    overall_correct += int(correct)

print("\n=== Intent Accuracy by CMI Bucket ===\n")
for bucket in ["pure_en", "light_mix", "heavy_mix"]:
    if bucket in buckets:
        stats = buckets[bucket]
        acc = stats["correct"] / stats["total"]
        print(f"{bucket:12s}: {acc:.1%}  ({stats['correct']}/{stats['total']})")

overall_acc = overall_correct / len(data)
print(f"\n{'OVERALL':12s}: {overall_acc:.1%}  ({overall_correct}/{len(data)})")