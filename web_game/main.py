import asyncio
import sys
import pygame
from pgzcompat import Actor, music, Rect, init_display, screen_api, tick

screen = screen_api
WIDTH = 1100
HEIGHT = 600


async def main():
    global screen
    init_display(WIDTH, HEIGHT)
    screen = screen_api

    with open("game.py", "r", encoding="utf-8") as f:
        exec(f.read(), globals())

    # Preload SFX and try intro music immediately (works when browser allows autoplay).
    try:
        _load_audio_assets()
        _start_scene_music()
    except Exception as e:
        print("audio preload skip:", e)

    print("Mineral Explorer loop starting", flush=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                print("click at", pos, flush=True)
                try:
                    # Re-attempt unlock/play on click (needed when autoplay was blocked).
                    _ensure_audio()
                    on_mouse_down(pos)
                except SystemExit:
                    # On web, treat as a soft restart
                    try:
                        restart_game()
                    except Exception:
                        pass
                except Exception as e:
                    print("click error:", e)
                    import traceback
                    traceback.print_exc()
        try:
            update()
            draw()
        except Exception as e:
            print("frame error:", e)
            import traceback
            traceback.print_exc()
        pygame.display.flip()
        tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
