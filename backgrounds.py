from PIL import Image, ImageDraw

def generate_background(width: int, height: int, style: str) -> Image.Image:
    """Generates a high-resolution base canvas with gradient color profiles."""
    bg = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(bg)
    
    presets = {
        "Sunset": ((255, 94, 98), (255, 153, 102)),
        "Ocean": ((43, 192, 228), (234, 236, 198)),
        "Aurora": ((58, 28, 113), (215, 109, 119)),
        "Dark": ((35, 37, 38), (65, 67, 69))
    }
    
    color1, color2 = presets.get(style, presets["Sunset"])
    
    # Calculate interpolation weights to render custom vertical linear gradients
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * (y / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    return bg

