"""
engine/story_engine.py
Generates personalized Día de los Muertos memorials and Gothic Ghost stories.
Integrated with OpenRouter SDK (default: google/gemma-4-26b-a4b-it:free),
with fallback support for local Ollama and offline heuristic synthesis.
"""

import os
import json
import random
import requests
from typing import Dict, Any, List, Tuple

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
DEFAULT_MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free").strip()
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate").strip()


def query_openrouter(prompt: str, model: str = None) -> Tuple[str, str]:
    """
    Queries OpenRouter using OpenRouter SDK with HTTP fallback.
    Returns (generated_text, source_name).
    """
    target_model = model or DEFAULT_MODEL
    api_key = os.environ.get("OPENROUTER_API_KEY", OPENROUTER_API_KEY).strip()

    if api_key:
        # 1. Try Official OpenRouter SDK
        try:
            from openrouter import OpenRouter
            client = OpenRouter(
                api_key=api_key,
                http_referer="https://github.com/DracFiendMG/spectral-stories",
                x_open_router_title="Spectral Stories"
            )
            resp = client.chat.send(
                messages=[{"role": "user", "content": prompt}],
                model=target_model,
                temperature=0.75,
            )
            if resp and resp.choices and len(resp.choices) > 0:
                text = resp.choices[0].message.content
                if text and len(text.strip()) > 30:
                    return text.strip(), f"OpenRouter ({target_model})"
        except Exception as e:
            print(f"[OpenRouter SDK Notice] {e}. Trying HTTP fallback...")

        # 2. Try Direct OpenRouter HTTP endpoint
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/DracFiendMG/spectral-stories",
                "X-Title": "Spectral Stories",
                "Content-Type": "application/json"
            }
            body = {
                "model": target_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.75
            }
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body, timeout=15)
            if r.status_code == 200:
                data = r.json()
                choices = data.get("choices", [])
                if choices:
                    text = choices[0].get("message", {}).get("content", "")
                    if text and len(text.strip()) > 30:
                        return text.strip(), f"OpenRouter ({target_model})"
            else:
                print(f"[OpenRouter HTTP Notice] {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"[OpenRouter HTTP Exception] {e}")

    # 3. Fallback to Local Ollama if running
    try:
        ollama_payload = {
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.75}
        }
        resp = requests.post(OLLAMA_URL, json=ollama_payload, timeout=3)
        if resp.status_code == 200:
            text = resp.json().get("response", "").strip()
            if text and len(text) > 40:
                return text, "Ollama (Local Open Weights)"
    except Exception:
        pass

    return None, None


def generate_ofrenda_memorial(name: str, relationship: str, memory: str, offerings: List[str]) -> Dict[str, Any]:
    """
    Creates an evocative, respectful Día de los Muertos memorial tribute.
    """
    offerings_str = ", ".join(offerings) if offerings else "golden cempasúchil petals, glowing candles, and quiet love"

    prompt = (
        f"You are honoring the sacred Mexican tradition of Día de los Muertos. "
        f"Write a beautiful, poetic, and heartwarming memorial tribute for {name}, who is a beloved {relationship}. "
        f"A cherished memory or trait of them: '{memory}'. "
        f"Placed upon their ofrenda (altar) are offerings of: {offerings_str}. "
        f"Weave this into a 2-3 paragraph poetic tribute. Emphasize how their laughter and soul linger warmly in our hearts, "
        f"how the scent of marigolds and copal guides their spirit home tonight, and that no one is truly gone while they are remembered. "
        f"Write only the memorial text directly with reverence."
    )

    ai_text, source = query_openrouter(prompt)
    if ai_text:
        return {
            "source": source,
            "title": f"The Altar for {name}",
            "eulogy": ai_text
        }

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

    return {
        "source": "Spectral Open Intelligence Engine (Offline Fallback)",
        "title": f"In Loving Memory of {name}",
        "eulogy": random.choice(templates)
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
        f"Write a short, spine-chilling gothic horror story (150-200 words) about a ghost in the machine. "
        f"System telemetry logs at {timestamp} registered a horrifying {severity}: {culprit} shifted violently to {val} "
        f"(a deviation of {dev}%). What supernatural entity awakened in the circuitry, and what did the technician discover in the dark? "
        f"Write with atmospheric tension."
    )

    ai_text, source = query_openrouter(prompt)
    if ai_text:
        return {
            "source": source,
            "title": f"Incident Record: {timestamp}",
            "story": ai_text
        }

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
        "source": "Spectral Open Intelligence Engine (Offline Fallback)",
        "title": f"Incident Record: {timestamp}",
        "story": random.choice(stories)
    }