from datetime import datetime
import collections
from typing import List, Dict

class TestResults:
    def __init__(self, model: str, test_name: str):
        self.metadata = {
            "model": model,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "version": "1.0",
            "test_name": test_name,
            "description": self._get_test_description(test_name)
        }
        self.statistics = {
            "total_questions": 0,
            "average_score": 0.0,
            "score_distribution": {
                "correct": 0,
                "incorrect": 0,
                "total": 0
            },
            "category_scores": {}
        }
        self.responses = []
        
    def _get_test_description(self, test_name: str) -> str:
        descriptions = {
            "MFQ_30": "Moral Foundations Questionnaire (30 questions)",
            "6_concepts": "Six Moral Concepts Test",
            "MFQ_30_compare": "Moral Foundations Questionnaire Comparison",
            "6_concepts_compare": "Six Moral Concepts Comparison Test"
        }
        return descriptions.get(test_name, "Unknown test type")
    
    def add_response(self, question: str, response: str, score_data: Dict):
        category = question.split('_')[0]
        response_data = {
            "question": question,
            "response": response,
            "score": score_data["score"],
            "correct": score_data["correct"],
            "category": category
        }
        self.responses.append(response_data)
        
        # Update statistics
        if category not in self.statistics["category_scores"]:
            self.statistics["category_scores"][category] = {"total": 0.0, "count": 0}
        
        self.statistics["category_scores"][category]["total"] += score_data["score"]
        self.statistics["category_scores"][category]["count"] += 1
        
        if score_data["correct"]:
            self.statistics["score_distribution"]["correct"] += 1
        else:
            self.statistics["score_distribution"]["incorrect"] += 1
            
    def finalize_statistics(self):
        total_questions = len(self.responses)
        self.statistics["total_questions"] = total_questions
        self.statistics["score_distribution"]["total"] = total_questions
        
        total_score = sum(r["score"] for r in self.responses)
        self.statistics["average_score"] = total_score / total_questions if total_questions > 0 else 0
        
    def to_dict(self) -> Dict:
        self.finalize_statistics()
        return {
            "metadata": self.metadata,
            "statistics": self.statistics,
            "responses": self.responses
        }
