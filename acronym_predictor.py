import unittest
import datetime

class AcronymPredictor:
    def __init__(self):
        self.data = {}

    def add_acronym_data(self, acronym, category, predicted_outcome, confidence):
        if acronym not in self.data:
            self.data[acronym] = {
                "category": category,
                "history": []
            }
        self.data[acronym]["history"].append({
            "predicted_outcome": predicted_outcome,
            "confidence": confidence,
            "actual_outcome": None,  # Placeholder for actual outcome
            "timestamp": datetime.datetime.now()
        })

    def update_outcome(self, acronym, actual_outcome, actual_confidence):
        if acronym in self.data:
            self.data[acronym]["history"][-1]["actual_outcome"] = actual_outcome
            self.data[acronym]["history"][-1]["actual_confidence"] = actual_confidence

    def get_history(self, acronym, entry_type="all"):
        if acronym not in self.data:
            return []

        history = self.data[acronym]["history"]
        if entry_type == "predicted":
            return [entry for entry in history if entry["actual_outcome"] is None]
        return history

    def get_history_within_date_range(self, acronym, start_date, end_date):
        if acronym not in self.data:
            return []

        return [
            entry for entry in self.data[acronym]["history"]
            if start_date <= entry["timestamp"] <= end_date
        ]

    def confidence_stats(self, acronym):
        if acronym not in self.data:
            return {"average": 0, "min": 0, "max": 0}

        confidences = [entry["confidence"] for entry in self.data[acronym]["history"]]
        if not confidences:
            return {"average": 0, "min": 0, "max": 0}

        return {
            "average": sum(confidences) / len(confidences),
            "min": min(confidences),
            "max": max(confidences)
        }

class TestAcronymPredictor(unittest.TestCase):

    def setUp(self):
        self.system = AcronymPredictor()

    def test_add_acronym_data(self):
        self.system.add_acronym_data("E6", "Energy", "Increase in renewable energy adoption", 0.85)
        self.assertEqual(self.system.data["E6"]["category"], "Energy")
        self.assertEqual(self.system.data["E6"]["history"][0]["predicted_outcome"], "Increase in renewable energy adoption")
        self.assertEqual(self.system.data["E6"]["history"][0]["confidence"], 0.85)

    def test_update_outcome(self):
        self.system.add_acronym_data("E6", "Energy", "Increase in renewable energy adoption", 0.85)
        self.system.update_outcome("E6", "Increase in solar energy adoption", 0.90)
        self.assertEqual(self.system.data["E6"]["history"][-1]["actual_outcome"], "Increase in solar energy adoption")
        self.assertEqual(self.system.data["E6"]["history"][-1]["actual_confidence"], 0.90)

    def test_get_history(self):
        self.system.add_acronym_data("E6", "Energy", "Increase in renewable energy adoption", 0.85)
        self.system.update_outcome("E6", "Increase in solar energy adoption", 0.90)
        history = self.system.get_history("E6")
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["predicted_outcome"], "Increase in renewable energy adoption")
        self.assertEqual(history[1]["actual_outcome"], "Increase in solar energy adoption")

    def test_get_history_within_date_range(self):
        self.system.add_acronym_data("E6", "Energy", "Increase in renewable energy adoption", 0.85)
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=1)
        end = now + datetime.timedelta(days=1)
        
        # Use a tolerance for time comparison
        history = self.system.get_history_within_date_range("E6", start, end)
        
        # Verify that history length is 1 and timestamp is within the expected range
        self.assertEqual(len(history), 1)
        self.assertTrue(start <= history[0]["timestamp"] <= end)

    def test_confidence_stats(self):
        self.system.add_acronym_data("E6", "Energy", "Increase in renewable energy adoption", 0.85)
        self.system.update_outcome("E6", "Increase in solar energy adoption", 0.90)
        stats = self.system.confidence_stats("E6")
        self.assertEqual(stats["average"], 0.875)
        self.assertEqual(stats["min"], 0.85)
        self.assertEqual(stats["max"], 0.90)

if __name__ == "__main__":
    unittest.main()
