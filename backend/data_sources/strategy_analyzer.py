import re

class StrategyAnalyzer:
    def __init__(self):
        self.forward_patterns = [
            r"\bgrowth\b", r"\bexpansion\b", r"\broadmap\b", r"\binvestment\b", 
            r"\blong-term\b", r"\baccelerat\w+", r"\binnovat\w+", r"\bstrategic\b",
            r"\bfuture\b", r"\bopportunit\w+"
        ]
        self.defensive_patterns = [
            r"\bchallenges\b", r"\bheadwinds\b", r"\bpressure\b", r"\brestructuring\b", 
            r"\bcost optimization\b", r"\bslowdown\b", r"\bdifficult\b", r"\befficiency\b",
            r"\balign resources\b", r"\bbottom line\b"
        ]

    def analyze_strategy(self, text_list):
        """
        Analyzes a list of text strings (e.g., articles) and returns aggregate scores.
        """
        if not text_list:
            return {
                "forward_score": 0.0,
                "defensive_score": 0.0,
                "sentiment_trend": "neutral"
            }

        combined_text = " ".join(text_list).lower()
        
        forward_count = sum(len(re.findall(p, combined_text)) for p in self.forward_patterns)
        defensive_count = sum(len(re.findall(p, combined_text)) for p in self.defensive_patterns)
        
        # Normalize simple score (density per 1000 characters or just raw ratio)
        # Here we use raw count for simplicity but could normalize if volume varies wildly
        
        # Determine trend based on balance
        if forward_count > defensive_count * 1.5:
            sentiment_trend = "positive"
        elif defensive_count > forward_count * 1.5:
            sentiment_trend = "negative"
        else:
            sentiment_trend = "neutral"

        return {
            "forward_score": float(forward_count),
            "defensive_score": float(defensive_count),
            "sentiment_trend": sentiment_trend
        }
