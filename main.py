from vars import *

def main():
    turn, init = 1, True
    b = pygame.time.get_ticks()
    check = False
    _running = True
    current_npc = None
    init1, tes, deb = pygame.time.get_ticks(), -1, False
    pygame.mixer_music.load(resource_path("assets/istd_DOOM.mp3"))
    pygame.mixer_music.set_volume(.25)
    pygame.mixer_music.play()
    wait = pygame.time.get_ticks()
    while _running:
        screen.fill(bg_color)
        for event in pygame.event.get():
            #quit event
            if event.type == pygame.QUIT: _running = False
            # mouse events
            if event.type == pygame.MOUSEBUTTONUP:
                mo_pos = pygame.mouse.get_pos()
                if gameScreens[0]==True:
                    if isHover(mo_pos, [WIDTH/2-75, HEIGHT/2, 150, 50]): change_game_screen(1) #start button
                elif gameScreens[2]==True:
                    if turn==1:
                        if battle_box.attack_select.collidepoint(mo_pos[0], mo_pos[1]):
                            turn=2
                            init=True
                            print('attack')
                        if battle_box.gaurd_select.collidepoint(mo_pos[0], mo_pos[1]):
                            print('gaurd')
                        if battle_box.stance_select.collidepoint(mo_pos[0], mo_pos[1]):
                            print('stance')
            # key press events
            if event.type == pygame.KEYDOWN:
                if gameScreens[1]==True:
                    if event.key == pygame.K_e:
                        npc_in_range = pygame.sprite.spritecollideany(main_plr.plr_sprite, npc_group)
                        if npc_in_range and dia.display_dialogue_box==False:
                            dia.display_dialogue_box=True 
                            current_npc=npc_in_range.parent_class
                            dia.selected_face=random.randint(0, len(current_npc.faces)-1)
                    if event.key == pygame.K_SPACE:
                        if dia.display_dialogue_box==True: 
                            pygame.mixer.Sound(resource_path('assets/snd_item.wav')).play()
                            if not dia.page>=len(dia.text)-1:
                                dia.page+=1
                                dia.selected_face=random.randint(0, len(current_npc.faces)-1)
                            else: 
                                dia.display_dialogue_box=False
                                dia.page=0
                elif gameScreens[2]==True:
                    if event.key == pygame.K_BACKSPACE:
                        pygame.mixer_music.load(resource_path("assets/testsong.mp3"))
                        pygame.mixer_music.play()
                        change_game_screen(1)
                    if turn==2:
                        main_plr.lane_movement(event)

                        if event.key == pygame.K_SPACE: check=True
        #
        mouse = pygame.mouse.get_pressed()
        mo_pos = pygame.mouse.get_pos()
        pressed = pygame.key.get_pressed()

        if gameScreens[0]==True:
            pygame.draw.rect(screen, RGB_Colors.red, [WIDTH/2-75, HEIGHT/2, 150, 50])
            createText('Start', (HEIGHT/2, WIDTH/2-50), size=32)
        elif gameScreens[1]==True:
            main_plr.movement(pressed)
            screen.blit(pygame.image.load(resource_path("assets/background.png")), (0, 0))

            if tree1.img.rect.colliderect(main_plr.plr_sprite.rect):
                if main_plr.direction.x > 0: main_plr.plr_sprite.rect.x += main_plr.velocity
                elif main_plr.direction.x < 0: main_plr.plr_sprite.rect.x -= main_plr.velocity
                if main_plr.direction.y > 0: main_plr.plr_sprite.rect.y += main_plr.velocity
                elif main_plr.direction.y < 0: main_plr.plr_sprite.rect.y -= main_plr.velocity
                deb=True
                main_plr.velocity=0
            
            camera_group.customDraw(screen, main_plr.plr_sprite, stages.town )

            if pygame.time.get_ticks() > 700+init1 and deb==True:
                init1 = pygame.time.get_ticks() 
                tes+=1
                if tes == 1:
                    change_game_screen(2)
                    tes=-1
                    deb=False
                    main_plr.velocity=3
            elif deb == True: createText("HERE COMES DARE DEVIL", (100, 100), size=32, color=(255, 0, 0))
            
            if pygame.sprite.spritecollideany(main_plr.plr_sprite, npc_group):
                if dia.display_dialogue_box == False: createText('E - TALK', (HEIGHT/2, WIDTH/2-50), size=32)
            else:
                dia.display_dialogue_box=False
                dia.page=0

            if dia.display_dialogue_box==True: dia.draw(screen, current_npc)
            # print(tree1.img.sheet.get_rect().centery, main_plr.plr_sprite.rect.centery)
        elif gameScreens[2]==True:
            screen.blit(pygame.image.load(resource_path("assets/background.png")), (0, 0))
            createText('this is a fight screen', (HEIGHT/2-132, 50), size=32)
            pygame.draw.rect(screen, (0, 0, 0), battle_box, 5)
            if turn==1:
                battle_box.draw()
            else:
                battle_box.draw_lanes()
                main_plr.lane_draw(battle_box)
                main_plr.counter_zone.y = main_plr.battle_rect.y
                main_plr.counter_zone.x = main_plr.battle_rect.x+main_plr.battle_rect.width-10

                pygame.draw.rect(screen, (0, 0, 0), main_plr.counter_zone, 2)

                for lane in notes:
                    for note in lane:
                        if not note.freeze: note.x-=8
                        pygame.draw.rect(screen, note.color, note)
                        if note.x < - 25: pass

                if check:
                    check=False
                    for lane in notes:
                        collision = main_plr.counter_zone.collidelist(lane)
                        if collision != -1: print(collision, lane[collision].note_value)
                        if collision != -1 and lane[collision].note_value == 2:
                            lane[collision].freeze = True
                            # lane.pop(collision)

                if pygame.time.get_ticks() > wait+8000:
                    wait = pygame.time.get_ticks()
                    if not init: turn=1
                    init=False
                

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

if __name__ == '__main__':
    main()
    