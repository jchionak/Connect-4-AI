"""
Implements the main game loop, title screen, and other UI elements.
"""
from manager import *
from learning_player import MoveTree, LearningPlayer, run_learning_algorithm
import pygame
import pygame_gui
import sys
from user import get_user_mouse_position, HumanPlayer


def title_screen():
    """
    Runs the title screen of the game.

    From the title screen, you can choose to either play a game vs the computer, play against a friend locally, or quit.
    """
    pygame.init()

    window_surface = pygame.display.set_mode((950, 800))
    pygame.display.set_caption('Connect 4')

    background = pygame.Surface((950, 800))
    background.fill((135, 206, 250))

    manager = pygame_gui.UIManager((950, 800), 'assets/button.json')
    manager.get_theme().load_theme('assets/title.json')

    multiplayer_button_layout_rect = pygame.Rect(0, 0, 250, 100)
    multiplayer_button_layout_rect.bottom = -250

    multiplayer_button = pygame_gui.elements.UIButton(relative_rect=multiplayer_button_layout_rect,
                                                      text='2 Player Game', manager=manager,
                                                      anchors={'centerx': 'centerx', 'bottom': 'bottom'},
                                                      object_id=pygame_gui.core.ObjectID(object_id='#multi_button',
                                                                                         class_id='@menu_buttons'))

    ai_button_layout_rect = pygame.Rect(0, 0, 250, 100)
    ai_button_layout_rect.bottom = -400

    ai_button = pygame_gui.elements.UIButton(relative_rect=ai_button_layout_rect,
                                             text='1 Player Game', manager=manager,
                                             anchors={'centerx': 'centerx', 'bottom': 'bottom'},
                                             object_id=pygame_gui.core.ObjectID(object_id='#ai_button',
                                                                                class_id='@menu_buttons'))

    quit_button_layout_rect = pygame.Rect(0, 0, 250, 100)
    quit_button_layout_rect.bottom = -100

    quit_button = pygame_gui.elements.UIButton(relative_rect=quit_button_layout_rect,
                                               text='Quit', manager=manager,
                                               anchors={'centerx': 'centerx', 'bottom': 'bottom'},
                                               object_id=pygame_gui.core.ObjectID(object_id='#quit_button',
                                                                                  class_id='@menu_buttons'))

    title_layout_rect = pygame.Rect(0, 0, 950, 200)
    title_layout_rect.top = 0

    title = pygame_gui.elements.UILabel(relative_rect=title_layout_rect, text='Connect 4', manager=manager,
                                        anchors={'centerx': 'centerx', 'top': 'top'}, visible=True,
                                        object_id=pygame_gui.core.ObjectID(object_id='#title_text',
                                                                           class_id='@menu_text'))

    name_layout_rect = pygame.Rect(0, 0, 950, 200)
    name_layout_rect.top = 100

    name = pygame_gui.elements.UILabel(relative_rect=name_layout_rect, text='Created by: Jayden Chiola-Nakai',
                                       manager=manager, anchors={'centerx': 'centerx', 'top': 'top'}, visible=True,
                                       object_id=pygame_gui.core.ObjectID(object_id='#name_text',
                                                                          class_id='@menu_text'))

    clock = pygame.time.Clock()
    multi = False
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == multiplayer_button:
                    multi = True
                elif event.ui_element == quit_button:
                    is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        if multi:
            multiplayer_game()
            multi = False

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()

    pygame.display.quit()


def multiplayer_game(background: pygame.Surface):
    """
    Runs a game between two human players.
    """
    playing = True
    while playing:
        pygame.display.quit()

        red_player = HumanPlayer('red')
        yellow_player = HumanPlayer('yellow')

        pygame.init()

        screen = pygame.display.set_mode((950, 800))

        screen.fill((0, 0, 205))
        pygame.display.set_caption('Connect 4')
        for i in range(7):
            for j in range(6):
                pygame.draw.circle(screen, (255, 255, 255), (100 + i * 125, 75 + j * 125), 50)

        pygame.display.flip()

        available_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        game = GameManager(red_player, yellow_player)

        while not game.board.full_board():
            if len(game.move_sequence) % 2 == 0:
                moving_player = 'red'
                while True:
                    move = red_player.make_move(available_columns, game)
                    if move in available_columns:
                        break
                game.add_piece('red', move)
                pygame.draw.circle(screen, (220, 20, 60),
                                   (100 + (ord(move) - 65) * 125, 75 + (5 - game.moves_per_column[move]) * 125), 50)
            else:
                moving_player = 'yellow'
                while True:
                    move = yellow_player.make_move(available_columns, game)
                    if move in available_columns:
                        break
                game.add_piece('yellow', move)
                pygame.draw.circle(screen, (255, 255, 51),
                                   (100 + (ord(move) - 65) * 125, 75 + (5 - game.moves_per_column[move]) * 125), 50)
            pygame.display.flip()
            pygame.time.delay(240 * 2)
            game.moves_per_column[move] += 1
            if game.moves_per_column[move] >= 6:
                available_columns.remove(move)
            if game.board.check_win((move, game.moves_per_column[move])):
                game.winner = moving_player

                # small menu for choosing whether to play again or return to title screen
                manager = pygame_gui.UIManager((950, 800), 'assets/button.json')

                clock = pygame.time.Clock()

                rm_button_layout_rect = pygame.Rect(0, 0, 250, 100)
                rm_button_layout_rect.top = 0

                rm_button = pygame_gui.elements.UIButton(relative_rect=rm_button_layout_rect,
                                                         text='Rematch', manager=manager,
                                                         anchors={'centerx': 'centerx', 'top': 'top'},
                                                         object_id=pygame_gui.core.ObjectID(object_id='#rm_button',
                                                                                            class_id='@menu_buttons'))

                ts_button_layout_rect = pygame.Rect(0, 0, 250, 100)
                ts_button_layout_rect.top = 150

                ts_button = pygame_gui.elements.UIButton(relative_rect=ts_button_layout_rect,
                                                         text='Title Screen', manager=manager,
                                                         anchors={'centerx': 'centerx', 'top': 'top'},
                                                         object_id=pygame_gui.core.ObjectID(object_id='#ts_button',
                                                                                            class_id='@menu_buttons'))

                is_running = True
                while is_running:
                    time_delta = clock.tick(60) / 1000.0
                    for event in pygame.event.get():
                        print(event.dict)
                        if event.type == pygame.QUIT:
                            print('quit')
                            is_running = False

                        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                            print('hi')
                            # if event.ui_element == ts_button:
                            # is_running = False
                            # to_break = True
                            pygame.display.quit()
                            return

                            # elif event.ui_element == rm_button:
                            #     print('Rematch')
                            #     is_running = False
                            #     to_break = True

                        manager.process_events(event)

                    manager.update(time_delta)

                    manager.draw_ui(screen)

                    pygame.display.flip()
                break


title_screen()
