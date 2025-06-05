from PIL import Image, ImageDraw
import os

def create_favicon():
    # Create a 32x32 image with a white background
    img = Image.new('RGB', (32, 32), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple ticket icon (a rectangle with a dashed line)
    draw.rectangle([4, 4, 28, 28], outline='blue', width=2)
    draw.line([8, 16, 24, 16], fill='blue', width=2)
    
    # Create static directory if it doesn't exist
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    # Save as ICO file
    img.save(os.path.join(static_dir, 'favicon.ico'), format='ICO')

if __name__ == '__main__':
    create_favicon() 