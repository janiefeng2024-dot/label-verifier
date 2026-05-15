import re
from typing import Dict, Any, List, Optional


class LabelMatcher:
    """
    Alcohol label compliance checker (OCR-tolerant, production-ready single file).

    Key design:
    - Normalize OCR noise once
    - Use ONE shared ABV detector
    - Keep rules simple and deterministic
    """

    def __init__(self):
        self.rules = [
            self._check_brand_name,
            self._check_class_type,
            self._check_net_contents,
            self._check_bottler_info,
            self._check_alcohol_presence,
            self._check_alcohol_percentage,
            self._check_origin_info,
            self._check_government_warning
        ]

    # =====================================================
    # PUBLIC API
    # =====================================================
    def validate(self, text: str) -> Dict[str, Any]:
        text = self._normalize(text)

        issues: List[str] = []
        confidence = 1.0

        for rule in self.rules:
            result = rule(text)
            if not result["passed"]:
                issues.append(result["message"])
                confidence -= result["penalty"]

        confidence = max(0.0, round(confidence, 2))

        return {
            "is_valid": len(issues) == 0,
            "confidence": confidence,
            "issues": issues
        }

    # =====================================================
    # OCR NORMALIZATION
    # =====================================================
    def _normalize(self, text: str) -> str:
        text = text.upper()

        replacements = {
            "ALC./VOL.": "ALC/VOL",
            "ALC./VOL": "ALC/VOL",
            "ALC . VOL": "ALC/VOL",
            "ALC VOL": "ALC/VOL",
            "ALCOHOL BY VOLUME": "ABV",
            "PERCENT": "%"
        }

        for k, v in replacements.items():
            text = text.replace(k, v)

        # remove OCR noise but keep structure
        text = re.sub(r"[^\w%/.,() ]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =====================================================
    # SHARED ABV DETECTOR
    # =====================================================
    def _extract_abv(self, text: str) -> Optional[float]:
        """
        Handles ALL real-world cases:
        - 45% ALC/VOL
        - ALC/VOL 45%
        - 45% ABV
        - ABV 45%
        - 45% ALCOHOL
        """

        patterns = [
            r"(\d+(\.\d+)?)\s*%\s*(ALC/VOL|ABV|ALCOHOL)",
            r"(ALC/VOL|ABV|ALCOHOL)\s*(\d+(\.\d+)?)\s*%",
        ]

        for p in patterns:
            match = re.search(p, text)
            if match:
                # extract numeric safely from either group
                for g in match.groups():
                    if g and re.match(r"^\d+(\.\d+)?$", g):
                        return float(g)

        return None

    # =====================================================
    # RULES
    # =====================================================

    def _check_brand_name(self, text: str) -> Dict[str, Any]:
        STOPWORDS = {
            "GOVERNMENT", "WARNING", "PRODUCT", "OF", "MADE", "IN",
            "DISTILLED", "BOTTLED", "PRODUCED", "PACKED", "BY",
            "ALCOHOL", "ABV", "VOL", "PROOF",
            "ML", "L", "CL", "OZ", "FL",
            "USA", "CANADA", "EU"
        }

        candidates = re.findall(r"\b([A-Z]{3,}(?:\s+[A-Z]{3,}){1,3})\b", text)

        for phrase in candidates:
            words = phrase.split()
            if sum(1 for w in words if w in STOPWORDS) < len(words) / 2:
                return {"passed": True, "message": "", "penalty": 0.0}

        single_words = re.findall(r"\b[A-Z]{5,}\b", text)

        for word in single_words:
            if word not in STOPWORDS:
                return {"passed": True, "message": "", "penalty": 0.0}

        return {"passed": False, "message": "Missing brand name", "penalty": 0.1}

    def _check_class_type(self, text: str) -> Dict[str, Any]:
        keywords = [
            "BOURBON", "WHISKEY", "WHISKY", "VODKA", "GIN",
            "RUM", "TEQUILA", "WINE", "BEER",
            "IPA", "LAGER", "ALE", "CIDER"
        ]

        if any(k in text for k in keywords):
            return {"passed": True, "message": "", "penalty": 0.0}

        return {"passed": False, "message": "Missing class/type designation", "penalty": 0.15}

    def _check_net_contents(self, text: str) -> Dict[str, Any]:
        if re.search(r"\b\d+(\.\d+)?\s*(ML|L|CL|OZ)\b", text):
            return {"passed": True, "message": "", "penalty": 0.0}

        return {"passed": False, "message": "Missing net contents", "penalty": 0.2}

    def _check_bottler_info(self, text: str) -> Dict[str, Any]:
        if re.search(r"(BOTTLED BY|DISTILLED BY|PRODUCED BY|PACKED BY)", text):
            return {"passed": True, "message": "", "penalty": 0.0}

        return {"passed": False, "message": "Missing bottler/producer info", "penalty": 0.2}

    def _check_alcohol_presence(self, text: str) -> Dict[str, Any]:
        if self._extract_abv(text) is not None:
            return {"passed": True, "message": "", "penalty": 0.0}

        return {
            "passed": False,
            "message": "Missing valid alcohol declaration",
            "penalty": 0.35
        }

    def _check_alcohol_percentage(self, text: str) -> Dict[str, Any]:
        if self._extract_abv(text) is not None:
            return {"passed": True, "message": "", "penalty": 0.0}

        return {
            "passed": False,
            "message": "Missing or invalid alcohol percentage format",
            "penalty": 0.25
        }

    def _check_origin_info(self, text: str) -> Dict[str, Any]:
        if re.search(r"(PRODUCT OF|MADE IN|IMPORTED|USA|CANADA|EU)", text):
            return {"passed": True, "message": "", "penalty": 0.0}

        return {"passed": False, "message": "Missing origin information", "penalty": 0.15}

    def _check_government_warning(self, text: str) -> Dict[str, Any]:
        """
        OCR-tolerant Government Warning detection
        """

        # normalize OCR spacing issues
        normalized = re.sub(r"\s+", " ", text.upper())

        if "GOVERNMENT WARNING" in normalized:
            return {"passed": True, "message": "", "penalty": 0.0}

        return {
            "passed": False,
            "message": "Missing government warning",
            "penalty": 0.45
        }