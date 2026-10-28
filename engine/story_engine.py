"""
engine/story_engine.py
Generates personalized Día de los Muertos memorials and Gothic Ghost stories.
Supports local Ollama LLMs with intelligent offline generation fallback.
"""

import json
import random
import requests
from typing import Dict, Any, List

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt: str, model: str = "llama3.1") -> str:
    """Attempts to generate text using local Ollama instance."""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.75, "top_p": 0.9}
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=6)
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
    except Exception:
        pass
    return None


def generate_ofrenda_memorial(name: str, relationship: str, memory: str, offerings: List[str]) -> Dict[str, Any]:
    """
    Creates an evocative, respectful Día de los Muertos memorial piece.
    """
    offerings_str = ", ".join(offerings) if offerings else "golden cempasúchil petals, glowing candles, and quiet love"

    prompt = (
        f"You are honoring the sacred Mexican tradition of Día de los Muertos. "
        f"Write a beautiful, poetic, and heartwarming memorial for {name}, who is a beloved {relationship}. "
        f"A cherished memory of them: '{memory}'. "
        f"Placed upon their altar are offerings of: {offerings_str}. "
        f"Weave this into a 2-3 paragraph poetic tribute. Emphasize how their laughter and soul linger warmly in our hearts, "
        f"how the scent of marigolds guides their spirit home tonight, and that no one is truly gone while they are remembered."
    )

    ollama_result = query_ollama(prompt)
    if ollama_result and len(ollama_result) > 100:
        return {
            "source": "Ollama (Llama 3.1 Open Weights)",
            "title": f"The Altar for {name}",
            "eulogy": ollama_result
        }

    # Rich poetic local generation fallback
    templates = [
        (
            f"Tonight, the boundary between worlds softens into amber warmth. Upon this altar, we spread vibrant "
            f"orange cempasúchil petals and light flickering tapers to guide your gentle spirit back across the veil, "
            f"dearest {name}. Though time has carried you beyond our physical touch, your presence as our beloved {relationship} "
            f"remains etched into the very foundation of who we are.\n\n"
            f"We still hold close the memory of {memory.rstrip('.')}. When we close our eyes, the sound of your voice and "
            f"the warmth of your companionship return as vivid as sunlight through morning glass. Before your portrait rest "
            f"the offerings of {offerings_str}—tokens of our enduring gratitude and love.\n\n"
            f"In the sacred wisdom of our ancestors, a soul never truly perishes so long as their name is spoken with fondness "
            f"and their deeds remembered with a smile. Tonight, {name}, the candles dance in celebration of your life. Welcome home."
        ),
        (
            f"The golden petals of the marigold pave a luminous pathway through the autumn twilight, beckoning you home, {name}. "
            f"To have known you as our {relationship} was a blessing that neither sorrow nor years can ever diminish.\n\n"
            f"Gathered here around the glowing candles, we reminisce about {memory.rstrip('.')}. It is in these quiet, sacred "
            f"recollections that you continue to walk beside us—teaching us, comforting us, and making our burdens lighter. "
            f"Upon your ofrenda, we have laid out {offerings_str}, carrying our deepest prayers and unconditional love.\n\n"
            f"May the copal incense carry our whispered thanks to the stars. You are remembered, you are celebrated, and you will forever "
            f"be loved, {name}. Rest in eternal serenity, surrounded by light."
        )
    ]

    selected_text = random.choice(templates)
    return {
        "source": "Spectral Open Intelligence Engine",
        "title": f"In Loving Memory of {name}",
        "eulogy": selected_text
    }


def generate_haunting_lore(anomaly_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates tabular telemetry anomalies into a chilling gothic ghost story.
    """
    culprit = anomaly_summary.get("primary_culprit", "ambient sensor")
    val = anomaly_summary.get("observed_value", "unknown")
    timestamp = anomaly_summary.get("timestamp", "03:14:00 AM")
    severity = anomaly_summary.get("severity", "Class III Spectral Anomaly")
    dev = anomaly_summary.get("deviation_pct", 100.0)

    prompt = (
        f"Write a short, spine-chilling gothic horror story (150-250 words) about a ghost haunting modern technology. "
        f"Telemetry logs at {timestamp} registered a horrifying {severity}: {culprit} shifted violently to {val} "
        f"(a deviation of {dev}%). What supernatural entity awakened in the circuitry, and what did the human discover in the dark?"
    )

    ollama_result = query_ollama(prompt)
    if ollama_result and len(ollama_result) > 80:
        return {
            "source": "Ollama (Llama 3.1 Open Weights)",
            "title": f"The Entity of {timestamp}",
            "story": ollama_result
        }

    # High-atmosphere gothic fallback lore
    stories = [
        (
            f"It was precisely {timestamp} when the silent monitors flickered with impossible numbers. The sensors registered a sudden, "
            f"violent anomaly: {culprit} shifted to {val}, drifting {dev}% beyond the laws of thermal equilibrium.\n\n"
            f"In the darkness of the empty corridor, the air grew frigid. Condensation formed in geometric fractures against the server glass. "
            f"It was not a circuit malfunction. It was an exhalation.\n\n"
            f"Someone—or something—that had once inhabited the physical halls of this ground had found its way into the copper veins of the machine. "
            f"The status light blinked twice in the dark: a slow, rhythmic pulse. Like a trapped heart remembering how to beat."
        ),
        (
            f"The logs never lie, yet the night technician stared in disbelief at the entry stamped {timestamp}. A {severity} had cascaded "
            f"across the array, dragging {culprit} to an aberrant reading of {val}.\n\n"
            f"A quiet hum vibrated through the floorboards. On the security camera feeds, the hallway was still, yet the digital motion flags "
            f"were screaming. Step by invisible step, something was pacing between the racks.\n\n"
            f"When the terminal fan ground to an abrupt, breathless halt, a single line appeared in the command buffer unprompted: "
            f"'I STILL LIVE HERE.' And then, the room plunged into ice."
        )
    ]

    return {
        "source": "Spectral Open Intelligence Engine",
        "title": f"Incident Record: {timestamp}",
        "story": random.choice(stories)
    }
