import pygame
import math # Import the math module
from pytmx import load_pygame

pygame.init()

# Set up the display
width, height = 16 * 30, 16 * 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ocean")

# Play background music
pygame.mixer.music.load("Assets/Sound/starlight_city.mp3")
# pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
pygame.mixer.music.play(-1)  # Play the music indefinitely

collideSound = pygame.mixer.Sound("Assets/Sound/coin.wav")

# Load tiled tmx map
map = load_pygame("Tiled/map.tmx")

# background layers
layers = map.visible_layers
backgrounds = [layer for layer in layers if layer.name.startswith("bg")]

# get objects
objects = list(map.objects) # Convert to list to iterate multiple times

# Lấy các đối tượng cụ thể và lưu vị trí X ban đầu của chúng
fishs = []
turtles = []
chickens = []

# Tăng cường đối tượng PyTMX với thuộc tính 'original_x' và 'original_y'
# để lưu trữ vị trí ban đầu của chúng.
for obj in objects:
    obj.original_x = obj.x
    obj.original_y = obj.y # Lưu cả y nếu muốn dao động theo Y

    if obj.name == "fish":
        fishs.append(obj)
    elif obj.name == "turtle":
        turtles.append(obj)
    elif obj.name == "chicken":
        chickens.append(obj)

# print(len(saladlist))

print(f"Fishs: {len(fishs)}, Turtles: {len(turtles)}, Chickens: {len(chickens)}")
# Tạo font chữ
font = pygame.font.Font(None, 16)  # Tạo font chữ với kích thước 36

clock = pygame.time.Clock()
running = True


# player
playerImageSheet = pygame.image.load("Assets/Animals/Sheep.png").convert_alpha()  # Sử dụng convert_alpha để hỗ trợ trong suốt
playerImages = []
playerIndex = 0
playerSpeed = 2  # Tốc độ di chuyển của người chơi
for i in range(4):
    image = playerImageSheet.subsurface((i * 16, 0, 16, 16))  # Cắt ảnh từ sprite sheet
    image = pygame.transform.scale(image, (20, 20))  # Đảm bảo kích thước là 16x16
    playerImages.append(image)
    
# print(f"Player images: {len(playerImages)}")  # In ra số lượng hình ảnh người chơi

playerX = 16 * 15  # Vị trí X của người chơi
playerY = 16 * 15  # Vị trí Y của người chơi

# Parameters for oscillation
oscillation_amplitude = 5   # Số pixel đối tượng sẽ di chuyển sang mỗi bên (ví dụ: 5 pixel)
oscillation_speed = 0.005  # Tốc độ dao động (giá trị nhỏ hơn = chậm hơn, lớn hơn = nhanh hơn)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get current time for oscillation (in milliseconds)
    current_time_ms = pygame.time.get_ticks()

    # Draw the map layers
    for layer in backgrounds:
        for x, y, image in layer.tiles():
            screen.blit(image, (x * map.tilewidth, y * map.tileheight)) # Sử dụng map.tilewidth/height

    # Draw objects with oscillation
    # Một hàm tiện ích để xử lý việc vẽ và dao động cho bất kỳ danh sách đối tượng nào
    def draw_oscillating_objects(object_list, time_ms, amplitude, speed, axis='x'):
        for obj in object_list:
            # Tính toán độ lệch vị trí dựa trên hàm sine và thời gian
            # Nhân với tốc độ để kiểm soát tần số dao động
            # Nhân với biên độ để kiểm soát độ lớn của dao động
            offset = amplitude * math.sin(time_ms * speed)

            # Áp dụng offset vào vị trí phù hợp
            if axis == 'x':
                new_x = obj.original_x + offset
                new_y = obj.original_y
            elif axis == 'y':
                new_x = obj.original_x
                new_y = obj.original_y + offset
            else: # Nếu muốn cả x và y dao động (tạo chuyển động tròn hoặc elip)
                new_x = obj.original_x + amplitude * math.sin(time_ms * speed)
                new_y = obj.original_y + amplitude * math.cos(time_ms * speed) # Sử dụng cos để có sự lệch pha

            if obj.image:
                screen.blit(obj.image, (new_x, new_y))
            else:
                # Debugging: Vẽ hình chữ nhật cho các đối tượng không có hình ảnh
                pygame.draw.rect(screen, (255, 0, 255), (new_x, new_y, obj.width, obj.height), 1)

    # Áp dụng dao động cho từng loại đối tượng
    # Ví dụ: fishs dao động theo X, turtles dao động theo Y, chickens cũng theo X
    draw_oscillating_objects(fishs, current_time_ms, oscillation_amplitude, oscillation_speed, axis='x')
    draw_oscillating_objects(turtles, current_time_ms, oscillation_amplitude, oscillation_speed * 0.8, axis='y') # Rùa chậm hơn một chút
    draw_oscillating_objects(chickens, current_time_ms, oscillation_amplitude * 0.5, oscillation_speed * 1.2, axis='x') # Gà dao động nhỏ hơn và nhanh hơn


    # Player movement    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerX -= playerSpeed
    if keys[pygame.K_RIGHT]:
        playerX += playerSpeed
    if keys[pygame.K_UP]:
        playerY -= playerSpeed
    if keys[pygame.K_DOWN]:
        playerY += playerSpeed
        
 
        
    # Ensure player stays within bounds
    playerX = max(0, min(playerX, width - 20))  #
    playerY = max(0, min(playerY, height - 20)) # Giới hạn trong
    # Ensure player stays within the map bounds
    playerX = max(0, min(playerX, map.width * map.tilewidth - 20))  # Giới hạn trong chiều rộng của bản đồ
    playerY = max(0, min(playerY, map.height * map.tileheight - 20)) # Giới hạn trong chiều cao của bản đồ
    
    # check player collision Player vs Salad List
    
    # saladRectList = []
    # for salad in saladList:
    #     saladRect = salad.get_rect()
    #     saladRectList.append(saladRect)
    
    # # Player vs saladRectList
    # playerRect = player.image.get_rect()
    # for x in saladRectList:
        
    #     if playerRect.colliderect(x):
    #         print("Collided!!!")

    # Check for collisions with fishs
    remaining_fishs = []
    for fish in fishs:
        playerRect = pygame.Rect(playerX, playerY, 20, 20)
        fishRect = pygame.Rect(fish.x, fish.y, 16, 16)  # Kích thước cá
        if playerRect.colliderect(fishRect):
            collideSound.play()
            # Remove fish from the list
        else:
            remaining_fishs.append(fish)
    fishs = remaining_fishs  # Cập nhật danh sách cá còn lại
    
    # Check for collisions with turtles
    remaining_turtles = []
    for turtle in turtles:
        playerRect = pygame.Rect(playerX, playerY, 20, 20)
        turtleRect = pygame.Rect(turtle.x, turtle.y, 16, 16)  # Kích thước rùa
        if playerRect.colliderect(turtleRect):
            collideSound.play()
            # Remove turtle from the list
        else:
            remaining_turtles.append(turtle)
    turtles = remaining_turtles  # Cập nhật danh sách rùa còn lại   
    
    # Check for collisions with chickens
    remaining_chickens = []
    for chicken in chickens:
        playerRect = pygame.Rect(playerX, playerY, 20, 20)
        chickenRect = pygame.Rect(chicken.x, chicken.y, 16, 16)  # Kích thước gà
        if playerRect.colliderect(chickenRect):
            collideSound.play()
            # Remove chicken from the list
        else:
            remaining_chickens.append(chicken)
    chickens = remaining_chickens  # Cập nhật danh sách gà còn lại
    
    # Tạo list knight
    knightList = []
    for obj in objects:
        if obj.name == "knight":
            knightList.append(obj)

    # check player vs enemy
    # playerRect = pygame.Rect(playerX, playerY, 16, 16)
    # playerEnemy1 = pygame.Rect(enemyList[0].x, enemyList[0].y, 16, 16)
    
    

    # Draw player 
    if playerIndex < len(playerImages):
        screen.blit(playerImages[int(playerIndex)], (playerX, playerY)) 
        playerIndex += 0.05
    else:
        playerIndex = 0
    
    # Render văn bản
    text_fish = font.render(f"{len(fishs)}", True, 'white') # (text, antialias, color)
    text_turtles = font.render(f"{len(turtles)}", True, 'white')
    text_chickens = font.render(f"{len(chickens)}", True, 'white')

    # Blit văn bản lên màn hình (x, y)
    screen.blit(text_fish, (16*2, 16*28 + 3)) # Góc trên cùng bên trái
    screen.blit(text_turtles, (16*6, 16*28 + 3)) # Dưới cá một chút
    screen.blit(text_chickens, (16*10, 16*28 + 3)) # Dưới rùa một chút
    
    # dRraw knightS
    for knight in knightList:
        screen.blit(knight.image, (knight.x, knight.y))
    

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60) # Thường nên để FPS cao hơn (ví dụ 60) cho chuyển động mượt mà hơn

pygame.quit()