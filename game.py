import pygame
import random
import cv2
import mediapipe as mp
import sys
# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gesture-Controlled Fruit Ninja")

font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Fruit class
class Fruit:
    def __init__(self):
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 0, 0), [0, 0, 40, 40])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, 700)
        self.rect.y = height
        self.speed_y = random.randint(-20, -10)
        self.gravity = 1
        self.sliced = False

    def update(self):
        self.rect.y += self.speed_y
        self.speed_y += self.gravity

# Create a fruit list
fruits = [Fruit() for _ in range(5)]
score = 0

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Webcam frame for hand tracking
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    hand_pos = None
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm = handLms.landmark[8] 
            cx, cy = int(lm.x * width), int(lm.y * height)
            hand_pos = (cx, cy)
            pygame.draw.circle(screen, (0, 255, 0), hand_pos, 15)

    for fruit in fruits:
        fruit.update()
        if not fruit.sliced:
            screen.blit(fruit.image, fruit.rect)

        if hand_pos and fruit.rect.collidepoint(hand_pos):
            fruit.sliced = True
            score += 1

        if fruit.rect.y > height + 40 or fruit.sliced:
            fruits.remove(fruit)
            fruits.append(Fruit())

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# Clean up
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
