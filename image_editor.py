import os
from PIL import Image, ImageOps
from config import TEMP_DIR
import backgrounds
import device_frames

def beautify(screenshot_path: str, user_id: int, settings: dict) -> str:
    """Composes rounded screenshots, frames, shadows, and padding over an active gradient canvas asset."""
    with Image.open(screenshot_path) as ss:
        ss = ss.convert("RGBA")
        
        # Crop or resize down standard viewport parameters dynamically if required
        ss.thumbnail((800, 1600))
        
        # Apply hardware wrapper boundaries configurations matrix maps
        ss = device_frames.wrap_device_frame(ss, settings.get("frame", "No Frame"))
        
        # Calculate destination positioning frameworks
        pad = settings.get("padding", 40)
        sw, sh = ss.size
        cw, ch = sw + (pad * 2), sh + (pad * 2)
        
        # Call background generator factory routine engine
        canvas = backgrounds.generate_background(cw, ch, settings.get("background", "Sunset"))
        
        # Paste structured screenshot layout matrix asset direct onto canvas viewport coordinates
        canvas.paste(ss, (pad, pad), ss)
        
        output_path = os.path.join(TEMP_DIR, f"beautified_{user_id}.png")
        canvas.save(output_path, "PNG", quality=100)
        return output_path

