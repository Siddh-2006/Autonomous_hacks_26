import re

class LinguisticAnalyzer:
    def __init__(self):
        # Research-backed indicators of financial distress/deception
        self.hedging_patterns = [
            r"we aim to", r"subject to", r"headwinds", r"challenging environment",
            r"macroeconomic factors", r"optimistic that", r"believe that", r"intend to"
        ]
        
        self.passive_patterns = [
            r"decisions were made", r"delays were encountered", r"was impacted by",
            r"has been reduced", r"are expected to be"
        ]
        
        self.bloat_words = [
            r"synergy", r"transformation", r"realignment", r"restructuring",
            r"strategic review", r"right-sizing"
        ]

    def analyze_text(self, text: str) -> dict:
        """
        Scans text for forensic markers.
        """
        text_lower = text.lower()
        
        hedging_count = sum(1 for p in self.hedging_patterns if re.search(p, text_lower))
        passive_count = sum(1 for p in self.passive_patterns if re.search(p, text_lower))
        bloat_count = sum(1 for p in self.bloat_words if re.search(p, text_lower))
        
        risk_score = (hedging_count * 2) + passive_count + bloat_count
        
        return {
            "hedging_count": hedging_count,
            "passive_count": passive_count,
            "bloat_word_count": bloat_count,
            "linguistic_risk_score": risk_score,
            "verdict": "High Risk" if risk_score > 3 else "Normal"
        }

# Example usage (for testing)
if __name__ == "__main__":
    analyzer = LinguisticAnalyzer()
    sample_pr = "We aim to improve margins, but results were impacted by macroeconomic headwinds."
    print(analyzer.analyze_text(sample_pr))
