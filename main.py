import pygame
import sys
from tkinter import Tk, filedialog, simpledialog

def select_file():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    root.attributes('-topmost', True)  # Bring dialog to front
    
    file_path = filedialog.askopenfilename(
        title="Select Spritesheet",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*")
        ]
    )
    root.destroy()
    return file_path

def get_tile_size():
    root = Tk()
    root.withdraw()  # Hide the main window
    
    result = simpledialog.askinteger("Input", "Enter a number:")
    
    root.destroy()
    return result, result

def main():
    
    print("Please select a spritesheet file and tilesize...")
    tilewidth, tileheight = get_tile_size()
    
    print("Hello, World!")
    sheet_path = select_file()
    scale = 2
    
    pygame.init()
    
    
    try:
        spritesheet = pygame.image.load(sheet_path)
    except pygame.error as e:
        print(f"Unable to load spritesheet image: {e}")
        sys.exit(1)
    
    sheet_width, sheet_height = spritesheet.get_size()
    
    cols = sheet_width // tilewidth
    rows = sheet_height //tileheight
    
    display_width = sheet_width * scale
    display_height = sheet_height * scale
    
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("frame viewer for spritesheets")
    
    scaled_spritesheet = pygame.transform.scale(
        spritesheet, 
        (display_width, display_height)
    )

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouseX, mouseY = pygame.mouse.get_pos()
        tileX = mouseX //(tilewidth * scale)
        tileY = mouseY //(tileheight * scale)
        
        frame_num = tileY * cols + tileX
        
        screen.blit(scaled_spritesheet, (0,0))
        
        for x in range (cols + 1):
            pygame.draw.line(
                screen, 
                (255, 255, 0),
                (x * tilewidth * scale, 0), 
                (x * tilewidth * scale, display_height),
                1
            )
        for y in range (rows + 1):
            pygame.draw.line(
                screen, 
                (255, 255, 0),
                (y * tileheight * scale, 0), 
                (y * tileheight* scale, display_width),
                1
            )
            
        font = pygame.font.Font(None, 24)
            
        if 0 <= tileX < cols and 0 <= tileY < rows:
            highlight_rect = pygame.Rect(
                tileX* tilewidth * scale,
                tileY * tileheight * scale,
                tilewidth * scale,
                tileheight * scale
            )
            pygame.draw.rect(screen, (255, 0, 0), highlight_rect, 2)
            
            # Display frame info
            info_text = f"Frame: {frame_num} | Pos: ({tileX}, {tileY}) | Row: {tileY}, Col: {tileX}"
            text_surface = font.render(info_text, True, (255, 255, 255))
            text_bg = pygame.Rect(5, 5, text_surface.get_width() + 10, text_surface.get_height() + 10)
            pygame.draw.rect(screen, (0, 0, 0), text_bg)
            pygame.draw.rect(screen, (255, 255, 0), text_bg, 1)
            screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()
    
        
if __name__ == "__main__":
    print("This script is being run directly.")
    main()