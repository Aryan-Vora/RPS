import pygame
import random
import sys
pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sun Tzu's Rock, Paper, Scissors")

rock_image = pygame.image.load("rock.png")
paper_image = pygame.image.load("paper.png")
scissors_image = pygame.image.load("scissors.png")
pygame.mixer.init()
paper_sound = pygame.mixer.Sound("paper_collision.wav")
rock_sound = pygame.mixer.Sound("rock_collision.wav")
scissors_sound = pygame.mixer.Sound("scissors_collision.wav")

all_images = []
image_rects = []
for _ in range(40):
    image = random.choice([rock_image, paper_image, scissors_image])
    all_images.append(image)
    image_rect = image.get_rect()
    image_rect.x = random.randint(0, WIDTH - image_rect.width)
    image_rect.y = random.randint(0, HEIGHT - image_rect.height)
    image_rects.append(image_rect)

# Random velocities for each image
image_velocities_x = [random.uniform(
    2, 3) * random.choice([1, -1]) for _ in range(len(all_images))]
image_velocities_y = [random.uniform(
    2, 3) * random.choice([1, -1]) for _ in range(len(all_images))]

def all_images_of_same_type(images):
    return all(image == images[0] for image in images)


def determine_winner(obj1, obj2):
    if obj1["image"] == obj2["image"]:
        return None 
    elif obj1["image"] == scissors_image:
        if obj2["image"] == rock_image:
            return obj2
        else:
            return obj1
    elif obj1["image"] == rock_image:
        if obj2["image"] == paper_image:
            return obj2
        else:
            return obj1
    elif obj1["image"] == paper_image:
        if obj2["image"] == scissors_image:
            return obj2
        else:
            return obj1


clock = pygame.time.Clock()
running = True

while running:
    game_over = False
    winner = None

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        screen.fill(WHITE)

        for i in range(len(all_images)):
            image_rects[i].move_ip(image_velocities_x[i],
                                   image_velocities_y[i])

            # Bounce off the edges of the screen
            if image_rects[i].left < 0 or image_rects[i].right > WIDTH:
                image_velocities_x[i] *= -1
            if image_rects[i].top < 0 or image_rects[i].bottom > HEIGHT:
                image_velocities_y[i] *= -1

            # Handle collisions with other images
            for j in range(len(all_images)):
                if i != j and image_rects[i].colliderect(image_rects[j]):
                    winner = determine_winner({"image": all_images[i]}, {
                                              "image": all_images[j]})
                    if winner:
                        if winner["image"] == rock_image:
                            rock_sound.play()
                        elif winner["image"] == paper_image:
                            paper_sound.play()
                        elif winner["image"] == scissors_image:
                            scissors_sound.play()

                        all_images[i] = winner["image"]
                        all_images[j] = winner["image"]

        for i in range(len(all_images)):
            screen.blit(all_images[i], image_rects[i])

        pygame.display.flip()
        clock.tick(FPS)

        if all_images_of_same_type(all_images):
            game_over = True
            winner = all_images[0]

    font = pygame.font.Font(None, 36)
    if winner:
        screen.fill(WHITE)
        if winner == rock_image:
            result_text = "The winner is Rock!"
        elif winner == paper_image:
            result_text = "The winner is Paper!"
        elif winner == scissors_image:
            result_text = "The winner is Scissors!"
    else:
        result_text = "It's a tie!"

    text_surface = font.render(result_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)

   #"Play Again" and "Quit" text
    font = pygame.font.Font(None, 36)
    play_again_text = font.render("Play Again", True, (0, 0, 0))
    play_again_rect = play_again_text.get_rect(
        center=(WIDTH // 2 - 100, HEIGHT // 2 + 50))
    quit_text = font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 + 50))
    screen.blit(play_again_text, play_again_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    # Reset the game
                    all_images = []
                    image_rects = []
                    for _ in range(30):
                        image = random.choice(
                            [rock_image, paper_image, scissors_image])
                        all_images.append(image)
                        image_rect = image.get_rect()
                        image_rect.x = random.randint(
                            0, WIDTH - image_rect.width)
                        image_rect.y = random.randint(
                            0, HEIGHT - image_rect.height)
                        image_rects.append(image_rect)
                    game_over = False
                    winner = None
                    waiting_for_click = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
