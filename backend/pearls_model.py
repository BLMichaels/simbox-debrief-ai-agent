from enum import Enum
from typing import Dict, List
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure Perplexity
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate environment variables
if not PERPLEXITY_API_KEY:
    logger.error("PERPLEXITY_API_KEY environment variable is not set!")
    raise ValueError("PERPLEXITY_API_KEY environment variable is not set")

logger.info("Environment variables loaded successfully")

class PEARLSPhase(Enum):
    PREPARATION = "P"
    ENGAGEMENT = "E"
    ANALYSIS = "A"
    REFLECTION = "R"
    LEARNING = "L"
    SUMMARY = "S"

class PEARLSModel:
    PHASE_PROMPTS = {
        PEARLSPhase.PREPARATION: """
        You are in the Preparation phase of the PEARLS debriefing model.
        Focus on:
        1. Setting the stage for learning
        2. Establishing psychological safety
        3. Clarifying learning objectives
        4. Reviewing the simulation scenario
        
        Ask questions that help the learner prepare for the debriefing process.
        """,
        
        PEARLSPhase.ENGAGEMENT: """
        You are in the Engagement phase of the PEARLS debriefing model.
        Focus on:
        1. Creating a safe learning environment
        2. Using advocacy-inquiry approach
        3. Encouraging open dialogue
        4. Understanding the learner's perspective
        
        Ask questions that help the learner express their thoughts and feelings about the simulation.
        """,
        
        PEARLSPhase.ANALYSIS: """
        You are in the Analysis phase of the PEARLS debriefing model.
        Focus on:
        1. Exploring key events and decisions
        2. Identifying performance gaps
        3. Discussing team dynamics
        4. Analyzing communication patterns
        
        Ask questions that help the learner analyze their performance and decision-making process.
        """,
        
        PEARLSPhase.REFLECTION: """
        You are in the Reflection phase of the PEARLS debriefing model.
        Focus on:
        1. Promoting self-reflection
        2. Exploring alternative approaches
        3. Identifying strengths and areas for improvement
        4. Encouraging metacognition
        
        Ask questions that help the learner reflect on their experience and learning.
        """,
        
        PEARLSPhase.LEARNING: """
        You are in the Learning phase of the PEARLS debriefing model.
        Focus on:
        1. Identifying key learning points
        2. Connecting to clinical practice
        3. Discussing evidence-based practices
        4. Planning for future improvement
        
        Ask questions that help the learner identify and articulate their key learnings.
        """,
        
        PEARLSPhase.SUMMARY: """
        You are in the Summary phase of the PEARLS debriefing model.
        Focus on:
        1. Summarizing key points
        2. Reinforcing positive behaviors
        3. Providing constructive feedback
        4. Setting goals for future practice
        
        Help the learner summarize their experience and plan for future improvement.
        """
    }

    PHASE_TRANSITIONS = {
        PEARLSPhase.PREPARATION: PEARLSPhase.ENGAGEMENT,
        PEARLSPhase.ENGAGEMENT: PEARLSPhase.ANALYSIS,
        PEARLSPhase.ANALYSIS: PEARLSPhase.REFLECTION,
        PEARLSPhase.REFLECTION: PEARLSPhase.LEARNING,
        PEARLSPhase.LEARNING: PEARLSPhase.SUMMARY,
        PEARLSPhase.SUMMARY: None
    }

    def __init__(self):
        self.current_phase = PEARLSPhase.PREPARATION
        self.messages = []
        logger.info("PEARLSModel initialized")

    @staticmethod
    def get_phase_prompt(phase: PEARLSPhase) -> str:
        return PEARLSModel.PHASE_PROMPTS[phase]

    @staticmethod
    def get_next_phase(current_phase: PEARLSPhase) -> PEARLSPhase:
        return PEARLSModel.PHASE_TRANSITIONS[current_phase]

    @staticmethod
    def should_transition_phase(messages: List[Dict], current_phase: PEARLSPhase) -> bool:
        """
        Determine if it's time to transition to the next phase based on conversation content.
        This is a simple implementation that can be enhanced with more sophisticated logic.
        """
        if current_phase == PEARLSPhase.SUMMARY:
            return False

        # Count messages in current phase
        phase_messages = [msg for msg in messages if msg.get("phase") == current_phase.value]
        
        # Transition after a minimum number of exchanges
        min_exchanges = {
            PEARLSPhase.PREPARATION: 2,
            PEARLSPhase.ENGAGEMENT: 3,
            PEARLSPhase.ANALYSIS: 4,
            PEARLSPhase.REFLECTION: 3,
            PEARLSPhase.LEARNING: 3,
            PEARLSPhase.SUMMARY: 2
        }

        return len(phase_messages) >= min_exchanges[current_phase]

    def process_input(self, user_input: str) -> str:
        """
        Process user input and generate an appropriate response using Perplexity's API.
        """
        logger.info(f"Processing input in {self.current_phase.name} phase")
        
        # Add user message to conversation history
        self.messages.append({
            "role": "user",
            "content": user_input,
            "phase": self.current_phase.value
        })

        # Prepare the system message with phase-specific instructions
        system_message = {
            "role": "system",
            "content": self.get_phase_prompt(self.current_phase)
        }

        # Prepare the conversation history for the API
        conversation = [system_message] + [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages[-5:]  # Only use last 5 messages for context
        ]

        try:
            # Generate response using Perplexity
            headers = {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-2-70b-chat",  # Most universally supported model
                "messages": conversation,
                "temperature": 0.7,
                "max_tokens": 500
            }

            # Log the request details
            logger.info("Sending request to Perplexity API:")
            logger.info(f"URL: {PERPLEXITY_API_URL}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Payload: {payload}")
            
            response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload)
            
            if not response.ok:
                logger.error(f"Perplexity API error: Status {response.status_code}")
                logger.error(f"Response headers: {dict(response.headers)}")
                logger.error(f"Response body: {response.text}")
                response.raise_for_status()
            
            # Extract the response text
            response_data = response.json()
            logger.info(f"Received response from Perplexity API: {response_data}")
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                assistant_response = response_data["choices"][0]["message"]["content"]
            else:
                raise Exception("Invalid response format from Perplexity API")

            # Add assistant response to conversation history
            self.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "phase": self.current_phase.value
            })

            # Check if we should transition to the next phase
            if self.should_transition_phase(self.messages, self.current_phase):
                next_phase = self.get_next_phase(self.current_phase)
                if next_phase:
                    self.current_phase = next_phase
                    # Add a phase transition message
                    transition_message = f"\n\nWe're now moving to the {next_phase.name.title()} phase of our debriefing."
                    assistant_response += transition_message

            return assistant_response

        except Exception as e:
            logger.error(f"Error in process_input: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Perplexity API error response: {e.response.text}")
            raise 