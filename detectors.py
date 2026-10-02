"""Three PII detectors. Each returns a list of (entity_type, start, end) for one text."""
import re

TARGETS = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN", "IN_AADHAAR", "IN_PAN"]

class RegexDetector:
    """Simple hand-written regex baseline (what a student would write in 20 minutes)."""
    name = "Regex baseline"
    PATTERNS = {
        "EMAIL_ADDRESS": r"[\w.+-]+@[\w-]+\.[\w.-]+",
        "PHONE_NUMBER": r"(?:\+?\d{1,2}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}",
        "CREDIT_CARD": r"\b(?:\d[ -]?){13,16}\b",
        "US_SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "IN_AADHAAR": r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b",
        "IN_PAN": r"\b[A-Z]{5}\d{4}[A-Z]\b",
        "PERSON": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    }
    def __init__(self): self.rx = {k: re.compile(v) for k, v in self.PATTERNS.items()}
    def detect(self, text):
        return [(k, m.start(), m.end()) for k, r in self.rx.items() for m in r.finditer(text)]

def _make_analyzer(model, india):
    from presidio_analyzer import AnalyzerEngine
    from presidio_analyzer.nlp_engine import NlpEngineProvider
    nlp = NlpEngineProvider(nlp_configuration={"nlp_engine_name": "spacy",
          "models": [{"lang_code": "en", "model_name": model}]}).create_engine()
    eng = AnalyzerEngine(nlp_engine=nlp, supported_languages=["en"])
    if india:
        from presidio_analyzer.predefined_recognizers import InAadhaarRecognizer, InPanRecognizer
        eng.registry.add_recognizer(InAadhaarRecognizer()); eng.registry.add_recognizer(InPanRecognizer())
    return eng

class PresidioDetector:
    def __init__(self, model="en_core_web_sm", india=False):
        self.eng = _make_analyzer(model, india)
        self.name = "Presidio + India recognizers" if india else "Presidio (default)"
    def detect(self, text):
        res = self.eng.analyze(text=text, language="en", entities=TARGETS)
        return [(r.entity_type, r.start, r.end) for r in res]
