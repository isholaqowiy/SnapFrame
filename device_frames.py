from PIL import Image, ImageDraw

def wrap_device_frame(img: Image.Image, frame_type: str) -> Image.Image:
    """Draws a minimalist hardware outline constraint boundary wrapping the viewport image asset."""
    if frame_type == "No Frame":
        return img
        
    w, h = img.size
    # Expand viewport parameters slightly to create hardware edge bounds
    canvas_w, canvas_h = w + 20, h + 40
    frame_img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(frame_img)
    # Draw minimalist device mock frame container layout
    draw.rounded_rectangle([0, 0, canvas_w, canvas_h], radius=25, fill=(20, 20, 20, 255))
    draw.rounded_rectangle([5, 20, canvas_w-5, canvas_h-10], radius=15, fill=(0, 0, 0, 0))
    
    # Paste user mobile image canvas inside boundaries
    frame_img.paste(img, (5, 20))
    return frame_img

