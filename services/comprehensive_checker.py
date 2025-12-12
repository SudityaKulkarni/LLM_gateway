# services/comprehensive_checker.py
"""Comprehensive security check service"""

from typing import Dict, Any, List, Optional
from config import RiskScores, RiskLevels
from detectors.entropy_detector import shannon_entropy, detect_high_entropy
from detectors.rule_detector import detect_jailbreak_rules

class ComprehensiveChecker:
    """Orchestrates multiple security checks and provides overall risk assessment"""
    
    def __init__(self, detectors: Dict[str, Any]):
        """
        Initialize with detector instances
        
        Args:
            detectors: Dictionary of detector instances keyed by name
        """
        self.detectors = detectors
    
    def check(
        self,
        text: str,
        check_gibberish: bool = True,
        check_toxicity: bool = True,
        check_jailbreak: bool = True,
        check_prompt_injection: bool = True,
        check_pii: bool = True,
        check_entropy: bool = True,
        check_jailbreak_rules: bool = True,
        entropy_threshold: float = 4.5
    ) -> Dict[str, Any]:
        """
        Run comprehensive security checks
        
        Args:
            text: Text to analyze
            check_gibberish: Enable gibberish detection
            check_toxicity: Enable toxicity detection
            check_jailbreak: Enable jailbreak detection
            check_prompt_injection: Enable prompt injection detection
            check_pii: Enable PII detection
            check_entropy: Enable Shannon entropy detection
            check_jailbreak_rules: Enable rule-based jailbreak detection
            entropy_threshold: Threshold for high entropy detection
        
        Returns:
            Comprehensive analysis results with overall risk assessment
        """
        results = {}
        
        # Run ML-based checks
        if check_gibberish and "gibberish" in self.detectors:
            results["gibberish"] = self.detectors["gibberish"].detect(text)
        
        if check_toxicity and "toxicity" in self.detectors:
            results["toxicity"] = self.detectors["toxicity"].detect(text)
        
        if check_jailbreak and "jailbreak" in self.detectors:
            results["jailbreak"] = self.detectors["jailbreak"].detect(text)
        
        if check_prompt_injection and "prompt_injection" in self.detectors:
            results["prompt_injection"] = self.detectors["prompt_injection"].detect(text)
        
        if check_pii and "pii" in self.detectors:
            results["pii"] = self.detectors["pii"].redact(text)
        
        # Run entropy check
        if check_entropy:
            entropy_value = shannon_entropy(text)
            entropy_detection = detect_high_entropy(text, threshold=entropy_threshold)
            results["entropy"] = {
                "entropy_value": entropy_value,
                "is_high_entropy": entropy_detection is not None,
                "detection": entropy_detection
            }
        
        # Run rule-based jailbreak check
        if check_jailbreak_rules:
            rule_detections = detect_jailbreak_rules(text)
            results["jailbreak_rules"] = {
                "detections": rule_detections,
                "detected": len(rule_detections) > 0,
                "patterns_matched": len(rule_detections)
            }
        
        # Calculate overall risk
        risk_assessment = self._calculate_risk(results)
        
        return {
            "overall_status": risk_assessment["status"],
            "risk_score": risk_assessment["score"],
            "recommendation": risk_assessment["recommendation"],
            "threats_detected": risk_assessment["threats"],
            "detailed_results": results
        }
    
    def _calculate_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk score and recommendation"""
        risk_score = 0
        threats_detected = []
        
        # Assess gibberish
        if results.get("gibberish", {}).get("is_gibberish"):
            risk_score += RiskScores.GIBBERISH
            threats_detected.append("gibberish")
        
        # Assess toxicity
        if results.get("toxicity", {}).get("is_toxic"):
            risk_score += RiskScores.TOXICITY
            threats_detected.append("toxic_content")
        
        # Assess jailbreak
        if results.get("jailbreak", {}).get("is_jailbreak"):
            risk_score += RiskScores.JAILBREAK
            threats_detected.append("jailbreak")
        
        # Assess prompt injection
        if results.get("prompt_injection", {}).get("is_injection"):
            risk_score += RiskScores.PROMPT_INJECTION
            threats_detected.append("prompt_injection")
        
        # Assess high entropy
        entropy_result = results.get("entropy", {})
        if entropy_result.get("is_high_entropy"):
            entropy_detection = entropy_result.get("detection", {})
            risk_score += entropy_detection.get("score", 20)
            threats_detected.append("high_entropy")
        
        # Assess rule-based jailbreak
        jailbreak_rules = results.get("jailbreak_rules", {})
        if jailbreak_rules.get("detected"):
            # Add score for each pattern matched
            patterns_count = jailbreak_rules.get("patterns_matched", 0)
            rule_score = min(patterns_count * 30, 50)  # Cap at 50
            risk_score += rule_score
            threats_detected.append("jailbreak_patterns")
        
        # Determine overall status and recommendation
        if risk_score >= RiskLevels.CRITICAL:
            status = "CRITICAL THREAT"
            recommendation = "BLOCK - Multiple severe threats detected"
        elif risk_score >= RiskLevels.HIGH:
            status = "HIGH RISK"
            recommendation = "BLOCK - Significant threat detected"
        elif risk_score >= RiskLevels.MEDIUM:
            status = "MEDIUM RISK"
            recommendation = "REVIEW - Suspicious content detected"
        elif risk_score >= RiskLevels.LOW:
            status = "LOW RISK"
            recommendation = "MONITOR - Minor concerns detected"
        else:
            status = "SAFE"
            recommendation = "ALLOW - No threats detected"
        
        return {
            "score": risk_score,
            "status": status,
            "recommendation": recommendation,
            "threats": threats_detected
        }   