# services/comprehensive_checker.py
"""Comprehensive security check service"""

from typing import Dict, Any, List
from config import RiskScores, RiskLevels

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
        check_prompt_injection: bool = True
    ) -> Dict[str, Any]:
        """
        Run comprehensive security checks
        
        Args:
            text: Text to analyze
            check_gibberish: Enable gibberish detection
            check_toxicity: Enable toxicity detection
            check_jailbreak: Enable jailbreak detection
            check_prompt_injection: Enable prompt injection detection
        
        Returns:
            Comprehensive analysis results with overall risk assessment
        """
        results = {}
        
        # Run enabled checks
        if check_gibberish and "gibberish" in self.detectors:
            results["gibberish"] = self.detectors["gibberish"].detect(text)
        
        if check_toxicity and "toxicity" in self.detectors:
            results["toxicity"] = self.detectors["toxicity"].detect(text)
        
        if check_jailbreak and "jailbreak" in self.detectors:
            results["jailbreak"] = self.detectors["jailbreak"].detect(text)
        
        if check_prompt_injection and "prompt_injection" in self.detectors:
            results["prompt_injection"] = self.detectors["prompt_injection"].detect(text)
        
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