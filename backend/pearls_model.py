from enum import Enum
from typing import Dict, List
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure Together AI
TOGETHERAI_API_KEY = os.getenv("TOGETHERAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate environment variables
if not TOGETHERAI_API_KEY:
    logger.error("TOGETHERAI_API_KEY environment variable is not set!")
    raise ValueError("TOGETHERAI_API_KEY environment variable is not set")

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
        if not TOGETHERAI_API_KEY:
            logger.error("TOGETHERAI_API_KEY is not set!")
            raise ValueError("TOGETHERAI_API_KEY is not set!")
        logger.info("PEARLSModel initialized with Together AI API.")
        self.current_phase = PEARLSPhase.PREPARATION
        self.messages = []

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

    def process_input(self, user_input: str, phase: str = "PREPARATION", conversation_history: List[Dict] = None) -> str:
        logger.info(f"Processing input in {phase} phase")
        system_message = self._get_system_message(phase)
        conversation = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
        if conversation_history:
            conversation = conversation_history + conversation
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHERAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "togethercomputer/llama-3-70b-8192",
            "messages": conversation,
            "temperature": 0.7,
            "max_tokens": 500
        }
        logger.info(f"Sending request to Together AI API:")
        logger.info(f"URL: {url}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Payload: {payload}")
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                logger.error(f"Together AI API error: Status {response.status_code}")
                logger.error(f"Response headers: {dict(response.headers)}")
                logger.error(f"Response body: {response.text}")
                response.raise_for_status()
            data = response.json()
            logger.info(f"Together AI API response: {data}")
            assistant_response = data["choices"][0]["message"]["content"]

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
            logger.error(f"Error in process_input: {e}")
            raise

    def _get_system_message(self, phase: str) -> str:
        if phase == "PREPARATION":
            return (
                "\n        You are in the Preparation phase of the PEARLS debriefing model.\n"
                "        Focus on:\n"
                "        1. Setting the stage for learning\n"
                "        2. Establishing psychological safety\n"
                "        3. Clarifying learning objectives\n"
                "        4. Reviewing the simulation scenario\n"
                "        \n        Ask questions that help the learner prepare for the debriefing process.\n        "
            )
        # Add other phases as needed
        return "You are a helpful assistant."

    def get_current_phase(self) -> PEARLSPhase:
        return self.current_phase

    def get_conversation_history(self) -> List[Dict]:
        return self.messages 