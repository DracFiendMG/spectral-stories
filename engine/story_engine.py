# engine/story_engine.py
# Spectral Stories - Memorial and Gothic Lore Generation
# Powered by Backboard SDK with google/gemma-4-26b-a4b-it

import os
import json
import random
import asyncio
from typing import Dict, Any, List, Tuple

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BACKBOARD_API_KEY = os.environ.get("BACKBOARD_API_KEY", "").strip()
DEFAULT_MODEL = os.environ.get("BACKBOARD_MODEL", "google/gemma-4-26b-a4b-it").strip()


async def query_backboard_async(prompt: str, model: str = None) -> Tuple[str, str]:
    """
    Sends prompt to Backboard SDK targeting google/gemma-4-26b-a4b-it.
    Returns (generated_text, source_label).
    """
    target_model = model or DEFAULT_MODEL
    api_key = os.environ.get("BACKBOARD_API_KEY", BACKBOARD_API_KEY).strip()

    if not api_key:
        return None, None

    provider = os.environ.get("BACKBOARD_PROVIDER", "openrouter").strip()
    try:
        from backboard import BackboardClient
        async with BackboardClient(api_key=api_key) as client:
            resp = await client.send_message(
                content=prompt,
                llm_provider=provider if provider else None,
                model_name=target_model,
                stream=False
            )
            text = resp.content if resp and hasattr(resp, "content") else ""
            if not text and hasattr(resp, "messages") and resp.messages:
                for m in reversed(resp.messages):
                    if getattr(m, "role", "") == "assistant" and getattr(m, "content", ""):
                        text = m.content
                        break

            if text and len(text.strip()) > 30:
                return text.strip(), f"Backboard ({target_model})"
    except Exception as e:
        print(f"[Backboard SDK Notice] {e}")

    return None, None


def query_backboard_sync(prompt: str, model: str = None) -> Tuple[str, str]:
    """Synchronous wrapper around query_backboard_async."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(asyncio.run, query_backboard_async(prompt, model)).result()
        else:
            return loop.run_until_complete(query_backboard_async(prompt, model))
    except Exception:
        return asyncio.run(query_backboard_async(prompt, model))


async def generate_ofrenda_memorial(name: str, relationship: str, memory: str, offerings: List[str]) -> Dict[str, Any]:
    """
    Creates an evocative, respectful Día de los Muertos memorial tribute.
    """
    offerings_str = ", ".join(offerings) if offerings else "golden cempasúchil petals, glowing tapers, and quiet love"

    prompt = (
        f"You are writing a tribute for a Dia de los Muertos altar (ofrenda). "
        f"Write a beautiful, poetic, and heartwarming remembrance for {name}, who is a beloved {relationship}. "
        f"A cherished memory or trait of them: '{memory}'. "
        f"Placed upon their ofrenda are offerings of: {offerings_str}. "
        f"Weave this into a 2-3 paragraph poetic tribute. Emphasize how their laughter and soul linger warmly in our hearts, "
        f"how the golden marigolds and incense guide their spirit home tonight, and that no one is truly gone while they are remembered. "
        f"Write with tenderness, cultural reverence, and poetic grace. Do not include markdown headers or meta commentary."
    )

    ai_text, source = await query_backboard_async(prompt)
    if ai_text:
        return {
            "source": "Altar Inscription",
            "title": f"The Altar for {name}",
            "eulogy": ai_text
        }

    # Thoughtfully crafted fallback tributes
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
        "source": "Altar Inscription",
        "title": f"In Loving Memory of {name}",
        "eulogy": random.choice(templates)
    }


async def generate_haunting_lore(anomaly_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates tabular telemetry anomalies into an atmospheric gothic story.
    """
    culprit = anomaly_summary.get("primary_culprit", "ambient sensor")
    val = anomaly_summary.get("observed_value", "unknown")
    timestamp = anomaly_summary.get("timestamp", "03:14:00 AM")
    severity = anomaly_summary.get("severity", "Class III Spectral Anomaly")
    dev = anomaly_summary.get("deviation_pct", 100.0)

    prompt = (
        f"Write a short, spine-chilling gothic horror vignette (150-200 words) about a ghost in modern machinery. "
        f"System telemetry logs at {timestamp} registered an anomaly: {culprit} shifted abruptly to {val} "
        f"(a deviation of {dev}%). What lingering presence stirred in the circuitry, and what was found in the dark? "
        f"Write with atmospheric tension, literary prose, and suspense. Do not use meta commentary."
    )

    ai_text, source = await query_backboard_async(prompt)
    if ai_text:
        return {
            "source": "Incident Lore",
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
        "source": "Incident Lore",
        "title": f"Incident Record: {timestamp}",
        "story": random.choice(stories)
    }
