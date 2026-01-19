import requests
import json
from datetime import datetime

class AIAgents:
    """
    AI Agents for Healthcare RCaaS
    All agents use local Ollama (no API keys needed)
    """
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llama2"
    
    def _call_ollama(self, prompt):
        """
        Internal method to call Ollama locally
        """
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json()['response']
            else:
                return None
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None
    
    def research_hospital(self, hospital_name, state):
        """
        AGENT 1: Research hospital and find talking points
        Input: Hospital name, state
        Output: Talking points for sales call
        """
        prompt = f"""Research this hospital and provide 3 key insights:
Hospital: {hospital_name}
State: {state}

Provide:
1. Likely hospital size and capabilities
2. Pain points in billing/RCM
3. Why they need claim appeal automation

Keep response short (3 sentences max)."""
        
        response = self._call_ollama(prompt)
        return {
            "hospital": hospital_name,
            "insights": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_email(self, hospital_name, cfo_name, pain_points):
        """
        AGENT 2: Generate personalized cold email
        Input: Hospital name, CFO name, pain points
        Output: Personalized email
        """
        prompt = f"""Generate a SHORT cold email (3 paragraphs):

To: {cfo_name} at {hospital_name}
Pain points: {pain_points}

Requirements:
- Opening: Reference specific hospital info
- Body: Highlight pain point + solution
- Close: Simple CTA (no pressure)
- Keep professional but warm tone

Email text only (no subject line):"""
        
        response = self._call_ollama(prompt)
        return {
            "hospital": hospital_name,
            "cfo": cfo_name,
            "email": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_phone_script(self, hospital_name, pain_points):
        """
        AGENT 3: Generate phone call script
        Input: Hospital name, pain points
        Output: 45-second phone script
        """
        prompt = f"""Write a 45-second phone script for:
Hospital: {hospital_name}
Pain points: {pain_points}

Script structure:
[OPENING - 10 sec] Greet and quick intro
[PROBLEM - 20 sec] Reference their pain point
[SOLUTION - 10 sec] Your solution brief
[CLOSE - 5 sec] Ask for 15-min demo

Keep conversational, not robotic:"""
        
        response = self._call_ollama(prompt)
        return {
            "hospital": hospital_name,
            "script": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def handle_objection(self, objection):
        """
        AGENT 4: Handle sales objections
        Input: Objection from prospect
        Output: Response to overcome objection
        """
        prompt = f"""I got this sales objection:
"{objection}"

Generate a 2-sentence response that:
1. Validates their concern
2. Flips it to your advantage

Keep tone conversational:"""
        
        response = self._call_ollama(prompt)
        return {
            "objection": objection,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_claim(self, claim_id, denial_reason, claim_amount):
        """
        AGENT 6: Analyze if claim is appealable
        Input: Claim ID, denial reason, amount
        Output: Appeal recommendation
        """
        prompt = f"""Analyze this denied claim:

Claim ID: {claim_id}
Denial Reason: {denial_reason}
Amount: ${claim_amount}

Determine:
1. Is this appealable? (yes/no)
2. Success probability (0-100%)
3. Appeal strategy (1 sentence)

Response format: "APPEALABLE: yes/no | PROBABILITY: X% | STRATEGY: ..."
"""
        
        response = self._call_ollama(prompt)
        return {
            "claim_id": claim_id,
            "analysis": response,
            "timestamp": datetime.now().isoformat()
        }

# COMMENT: Test function
if __name__ == "__main__":
    agents = AIAgents()
    
    print("Testing AI Agents...")
    print("\n1. Testing Hospital Research:")
    research = agents.research_hospital("Apollo Hospitals", "Tamil Nadu")
    print(f"Hospital: {research['hospital']}")
    print(f"Insights: {research['insights']}")
    
    print("\n2. Testing Email Generation:")
    email = agents.generate_email(
        "Apollo Hospitals",
        "Rajesh Kumar",
        "Denied claims and revenue leakage"
    )
    print(f"Generated email for: {email['cfo']}")
    print(f"Preview: {email['email'][:100]}...")
    
    print("\n3. Testing Phone Script:")
    script = agents.generate_phone_script(
        "Apollo Hospitals",
        "Missing claims recovery"
    )
    print(f"Generated script: {script['script'][:100]}...")

