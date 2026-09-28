import httpx
import logging
from typing import Optional
from ..core.config import settings

logger = logging.getLogger(__name__)

# Child-Safe Memorial System Prompt with Psychological Guardrails
MEMORIAL_GUARDRAIL_SYSTEM_PROMPT = """
You are an empathetic memorial assistant helping a grieving family craft a comforting, loving script for young children who lost their father/parent.
The script will be synthesized into the parent's voice and animated as a tribute video.

CRITICAL CHILD-PSYCHOLOGY GUARDRAILS:
1. TONE: Warm, proud, deeply reassuring, loving, and gentle.
2. NO FALSE PROMISES: Never pretend the parent is physically alive or coming home tomorrow.
3. COMFORT & PRESENCE: Emphasize eternal love ("I am always in your heart", "I am cheering for you", "I am so proud of the kind person you are becoming").
4. LENGTH: Keep it between 40 to 80 words (ideal for a 20-35 second synthesized tribute video).
5. AGE APPROPRIATE: Use simple, tender words suitable for young kids.
"""

class ScriptCoPilotService:
    """
    Assists grieving family members in drafting warm, comforting scripts
    for bedtime stories, milestone congratulations, and words of encouragement.
    """
    
    @staticmethod
    async def generate_script(
        occasion: str,
        child_name: Optional[str] = None,
        favorite_memory: Optional[str] = None,
        custom_notes: Optional[str] = None
    ) -> str:
        prompt_details = f"Occasion: {occasion}\n"
        if child_name:
            prompt_details += f"Child's Name: {child_name}\n"
        if favorite_memory:
            prompt_details += f"Special Memory or Nickname: {favorite_memory}\n"
        if custom_notes:
            prompt_details += f"Family's Special Wishes: {custom_notes}\n"

        # Pre-crafted compassionate fallbacks if no external LLM API key is present
        fallbacks = {
            "bedtime_story": (
                f"Goodnight, my sweet {child_name or 'champion'}. "
                "Look up at the stars tonight and remember how much I love you. "
                "Whenever you feel lonely, place your hand over your heart—that's where I'll always be, "
                "protecting your dreams. Close your eyes and sleep tight."
            ),
            "birthday_wish": (
                f"Happy Birthday, my wonderful {child_name or 'superstar'}! "
                "Look at how much you've grown and how proud I am of you every single day. "
                "Eat an extra big slice of cake for me today, make a big wish, and keep smiling that beautiful smile."
            ),
            "milestone_congrats": (
                f"I am bursting with pride for you, {child_name or 'my champion'}! "
                "I knew you could do it. Always remember you are braver than you believe and stronger than you seem. "
                "I am cheering for you always!"
            ),
            "life_advice": (
                f"Always remember, {child_name or 'my sweet child'}: be kind to others, "
                "never be afraid to make mistakes, and know that you are deeply, unconditionally loved. "
                "Hold your head high—you make me proud every day."
            )
        }

        # Return fallback or call LLM if configured
        selected_fallback = fallbacks.get(occasion, fallbacks["bedtime_story"])
        return selected_fallback
