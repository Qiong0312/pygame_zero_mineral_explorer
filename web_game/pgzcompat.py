"""Minimal Pygame Zero-like helpers for pygbag (plain pygame + asyncio)."""
from __future__ import annotations

import array
import os
import sys
import time
from pathlib import Path

import pygame

_ROOT = Path(__file__).resolve().parent
_IMAGES = _ROOT / "images"
_MUSIC = _ROOT / "music"

screen = None  # set by init_display()
_clock = None
_fonts = {}
_browser_audio_hooked = False


def init_display(width: int, height: int):
    global screen, _clock
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    try:
        pygame.mixer.init(44100, -16, 2, 512)
        try:
            pygame.mixer.set_num_channels(16)
        except Exception:
            pass
    except Exception as e:
        print("mixer init warning:", e)
        try:
            pygame.mixer.init()
        except Exception as e2:
            print("mixer init failed:", e2)
    screen = pygame.display.set_mode((width, height))
    _clock = pygame.time.Clock()
    _install_browser_audio_hooks()
    return screen


def _install_browser_audio_hooks():
    """Safari/iOS: resume SDL AudioContext on the first user gesture."""
    global _browser_audio_hooked
    if _browser_audio_hooked or sys.platform != "emscripten":
        return
    try:
        from platform import window

        window.eval(
            """
            (function () {
              if (window.__pgzAudioHooksInstalled) return;
              window.__pgzAudioHooksInstalled = true;

              function resumeAll() {
                function resumeCtx(ctx) {
                  if (!ctx) return;
                  try {
                    if (ctx.state === 'suspended' && ctx.resume) ctx.resume();
                  } catch (e) {}
                }
                try {
                  if (typeof Module !== 'undefined') {
                    if (Module.SDL2 && Module.SDL2.audioContext) resumeCtx(Module.SDL2.audioContext);
                    if (Module.SDL && Module.SDL.audioContext) resumeCtx(Module.SDL.audioContext);
                  }
                } catch (e) {}
                try { if (typeof SDL2 !== 'undefined') resumeCtx(SDL2.audioContext); } catch (e) {}
                try { if (typeof SDL !== 'undefined') resumeCtx(SDL.audioContext); } catch (e) {}
                try {
                  var nodes = document.querySelectorAll('audio,video');
                  for (var i = 0; i < nodes.length; i++) {
                    var p = nodes[i].play();
                    if (p && p.catch) p.catch(function () {});
                  }
                } catch (e) {}
              }

              window.__pgzResumeAudio = resumeAll;
              ['touchstart', 'touchend', 'mousedown', 'keydown'].forEach(function (evt) {
                window.addEventListener(evt, resumeAll, true);
              });
            })();
            """
        )
        _browser_audio_hooked = True
        print("browser audio hooks installed", flush=True)
    except Exception as e:
        print("browser audio hooks failed:", e)


def unlock_browser_audio():
    """Call from a click/touch handler so Safari allows sound."""
    if sys.platform != "emscripten":
        return
    _install_browser_audio_hooks()
    try:
        from platform import window

        window.eval("if (window.__pgzResumeAudio) window.__pgzResumeAudio();")
    except Exception as e:
        print("unlock_browser_audio eval failed:", e)

    # Warm the mixer inside the user-gesture stack (helps Safari).
    try:
        if pygame.mixer.get_init():
            beep = pygame.mixer.Sound(buffer=array.array("h", [0] * 512))
            beep.set_volume(0.0)
            beep.play()
    except Exception as e:
        print("silent unlock play failed:", e)


def _font(size: int):
    size = int(size)
    if size not in _fonts:
        _fonts[size] = pygame.font.SysFont(None, size)
    return _fonts[size]


def _parse_color(color):
    if isinstance(color, (tuple, list)):
        return tuple(color)
    if isinstance(color, str):
        return pygame.Color(color)
    return color


def _wrap_text(text: str, font, width: int):
    """Word-wrap text to fit within width (PGZero ptext-compatible enough)."""
    lines = []
    for paragraph in str(text).replace("\t", "    ").split("\n"):
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split(" ")
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if font.size(trial)[0] <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


class _ScreenDraw:
    def text(self, text, pos=None, **kwargs):
        fontsize = kwargs.get("fontsize", 24)
        color = _parse_color(kwargs.get("color", "white"))
        center = kwargs.get("center")
        width = kwargs.get("width")
        font = _font(fontsize)

        # PGZero: when positioned with center=, lines are center-aligned.
        # When positioned with topleft/pos, lines are left-aligned.
        if center is not None:
            align = 0.5
        else:
            align = 0.0
        align_kw = kwargs.get("align")
        if align_kw == "left":
            align = 0.0
        elif align_kw == "center":
            align = 0.5
        elif align_kw == "right":
            align = 1.0
        elif isinstance(align_kw, (int, float)):
            align = float(align_kw)

        if width is not None:
            lines = _wrap_text(text, font, int(width))
        else:
            lines = str(text).split("\n")

        line_surfs = [font.render(line, True, color) for line in lines]
        if not line_surfs:
            return

        line_gap = font.get_linesize()
        block_w = max(s.get_width() for s in line_surfs)
        if width is not None:
            block_w = max(block_w, int(width))
        block_h = line_gap * (len(line_surfs) - 1) + line_surfs[0].get_height()

        block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
        for i, line_surf in enumerate(line_surfs):
            x = int(round(align * (block_w - line_surf.get_width())))
            y = int(round(i * line_gap))
            block.blit(line_surf, (x, y))

        if center is not None:
            rect = block.get_rect(center=center)
        elif pos is not None:
            rect = block.get_rect(topleft=pos)
        else:
            rect = block.get_rect()
        screen.blit(block, rect)

    def filled_rect(self, rect, color):
        pygame.draw.rect(screen, _parse_color(color), rect)

    def rect(self, rect, color, width=1):
        pygame.draw.rect(screen, _parse_color(color), rect, width)

    def line(self, start, end, color):
        pygame.draw.line(screen, _parse_color(color), start, end)

    def filled_circle(self, pos, radius, color):
        pygame.draw.circle(screen, _parse_color(color), pos, radius)

    def circle(self, pos, radius, color, width=1):
        pygame.draw.circle(screen, _parse_color(color), pos, radius, width)


class Screen:
    def __init__(self):
        self.draw = _ScreenDraw()

    def fill(self, color):
        screen.fill(_parse_color(color))

    def blit(self, surf, dest):
        screen.blit(surf, dest)


# Module-level screen API used by the game (mimics pgzero's `screen`)
screen_api = Screen()


class Actor:
    def __init__(self, image_name, pos=None):
        self._image_name = image_name
        self._surf = self._load(image_name)
        self._pos = [0, 0]
        self.images = None
        self.fps = 5
        self._anim_index = 0
        self._anim_accum = 0.0
        if pos is not None:
            self.pos = pos

    def _load(self, name):
        path = _IMAGES / f"{name}.png"
        if not path.exists():
            # try without assuming extension already present
            path = _IMAGES / name
        surf = pygame.image.load(str(path))
        if pygame.display.get_init() and pygame.display.get_surface() is not None:
            surf = surf.convert_alpha()
        return surf

    @property
    def width(self):
        return self._surf.get_width()

    @property
    def height(self):
        return self._surf.get_height()

    @property
    def left(self):
        return self._pos[0]

    @left.setter
    def left(self, value):
        self._pos[0] = value

    @property
    def right(self):
        return self._pos[0] + self.width

    @right.setter
    def right(self, value):
        self._pos[0] = value - self.width

    @property
    def top(self):
        return self._pos[1]

    @top.setter
    def top(self, value):
        self._pos[1] = value

    @property
    def bottom(self):
        return self._pos[1] + self.height

    @bottom.setter
    def bottom(self, value):
        self._pos[1] = value - self.height

    @property
    def topleft(self):
        return tuple(self._pos)

    @topleft.setter
    def topleft(self, value):
        self._pos[0], self._pos[1] = value

    @property
    def pos(self):
        return (self._pos[0] + self.width / 2, self._pos[1] + self.height / 2)

    @pos.setter
    def pos(self, value):
        self._pos[0] = value[0] - self.width / 2
        self._pos[1] = value[1] - self.height / 2

    @property
    def center(self):
        return self.pos

    @center.setter
    def center(self, value):
        self.pos = value

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos = (value, self.pos[1])

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos = (self.pos[0], value)

    def draw(self):
        if screen is None:
            return
        screen.blit(self._surf, (int(self._pos[0]), int(self._pos[1])))

    def collidepoint(self, pos):
        x, y = pos[0], pos[1]
        rect = pygame.Rect(int(self._pos[0]), int(self._pos[1]), self.width, self.height)
        return rect.collidepoint(int(x), int(y))

    def animate(self):
        if not self.images:
            return
        self._anim_accum += 1.0 / 60.0
        frame_time = 1.0 / max(self.fps, 1)
        while self._anim_accum >= frame_time:
            self._anim_accum -= frame_time
            self._anim_index = (self._anim_index + 1) % len(self.images)
            self._surf = self._load(self.images[self._anim_index])


class Music:
    """Background music.

    On web (emscripten), use HTML5 Audio against HTTP-served /music/*.ogg.
    Large tracks fail as pygame.mixer.Sound (decode into RAM) and mixer.music
    streaming is unreliable in pygame-wasm — but short SFX Sounds work fine.
    """

    def __init__(self):
        self._volume = 0.5
        self._cache = {}
        self._channel = None
        self._current_name = None
        self._html = sys.platform == "emscripten"

    def set_volume(self, value):
        self._volume = float(value)
        if self._html:
            try:
                from platform import window
                window.eval(
                    f"if (window.__pgzBgm) window.__pgzBgm.volume = {self._volume:.3f};"
                )
            except Exception:
                pass
            return
        try:
            if self._channel is not None:
                self._channel.set_volume(self._volume)
        except Exception:
            pass

    def stop(self):
        self._current_name = None
        if self._html:
            try:
                from platform import window
                window.eval(
                    "if (window.__pgzBgm) { window.__pgzBgm.pause(); window.__pgzBgm.currentTime = 0; }"
                )
            except Exception:
                pass
            return
        try:
            if self._channel is not None:
                self._channel.stop()
        except Exception:
            pass

    def _get_sound(self, name: str):
        if name in self._cache:
            return self._cache[name]
        path = _resolve_audio(name)
        if path is None:
            print("music not found:", name, "in", _MUSIC)
            return None
        print("loading music Sound:", path, flush=True)
        snd = pygame.mixer.Sound(str(path))
        self._cache[name] = snd
        return snd

    def _play_html(self, name: str):
        # Served as static files from build/web/music/ (not from the apk MEMFS).
        import json

        url = f"music/{name}.ogg"
        try:
            unlock_browser_audio()
        except Exception:
            pass
        try:
            from platform import window

            window.eval(
                f"""
                (function () {{
                  var url = {json.dumps(url)};
                  var vol = {self._volume:.3f};
                  if (!window.__pgzBgm) {{
                    window.__pgzBgm = new Audio();
                    window.__pgzBgm.loop = true;
                    window.__pgzBgm.preload = 'auto';
                  }}
                  var a = window.__pgzBgm;
                  a.volume = Math.max(0, Math.min(1, vol));
                  if (a.dataset.track !== url) {{
                    a.dataset.track = url;
                    a.src = url;
                    a.load();
                  }}
                  var p = a.play();
                  if (p && p.catch) {{
                    p.catch(function (err) {{ console.log('bgm play blocked/failed', url, err); }});
                  }}
                }})();
                """
            )
            self._current_name = name
            print("playing html bgm:", url, flush=True)
        except Exception as e:
            print("html bgm failed:", e)
            raise

    def _play_sound(self, name: str):
        if name == self._current_name and self._channel is not None:
            try:
                if self._channel.get_busy():
                    return
            except Exception:
                pass

        snd = self._get_sound(name)
        if snd is None:
            return

        if self._channel is None:
            try:
                pygame.mixer.set_num_channels(max(16, pygame.mixer.get_num_channels()))
            except Exception:
                pass
            self._channel = pygame.mixer.Channel(0)

        self._channel.stop()
        snd.set_volume(self._volume)
        self._channel.set_volume(self._volume)
        self._channel.play(snd, loops=-1)
        self._current_name = name
        print("playing music via Sound loop:", name, flush=True)

    def play(self, name):
        try:
            unlock_browser_audio()
        except Exception:
            pass

        if self._html:
            try:
                self._play_html(name)
                return
            except Exception as e:
                print("html music fallback to Sound:", e)

        try:
            self._play_sound(name)
        except Exception as e:
            print("music Sound play failed, trying mixer.music:", name, e)
            path = _resolve_audio(name)
            if path is None:
                return
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(self._volume)
                pygame.mixer.music.play(-1)
                self._current_name = name
            except Exception as e2:
                print("music.play failed:", name, e2)


def _resolve_audio(name: str):
    for ext in (".ogg", ".mp3", ".wav"):
        path = _MUSIC / f"{name}{ext}"
        if path.exists():
            return path
        # also try cwd-relative music/
        path2 = Path("music") / f"{name}{ext}"
        if path2.exists():
            return path2
    return None


def sound_path(name: str) -> str:
    path = _resolve_audio(name)
    if path is None:
        raise FileNotFoundError(name)
    return str(path)


music = Music()
Rect = pygame.Rect


def tick(fps=60):
    if _clock is not None:
        _clock.tick(fps)
