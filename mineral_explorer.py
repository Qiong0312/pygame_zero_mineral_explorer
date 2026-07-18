import pgzrun
import random
import pygame
from pgzhelper import *
import sys, os
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

# screen size
WIDTH = 1100
HEIGHT = 600

#colours
Grass = (77, 161, 74)
Ocean = (27, 176, 209)

# Background
the_depths_bg = Actor('the_depths_bg')
the_depths_bg._surf = pygame.transform.scale(the_depths_bg._surf, (1100, 600))
the_depths_bg.topleft = (0, 0)

# Main Character
main_character = Actor('move_1')
main_character.topleft = (100, 180)
main_character.images = ['move_1', 'move_2', 'move_3', 'move_4', 'move_5', 'move_6', 'move_7']
main_character.fps = 10

# Collected minerals
collected_talc = False
collected_fluorite = False
collected_apatite = False
collected_silver = False
collected_opal = False
collected_topaz = False
collected_amethyst = False
collected_tungsten_carbide = False

# Minerals
show_talc = True
talc = Actor('talc')
talc.topleft = (1250, 400)
# talc._surf = pygame.transform.scale(talc._surf, (180, 180)

show_fluorite = True
fluorite = Actor('fluorite')
fluorite.topleft = (2250, 380)
# fluorite._surf = pygame.transform.scale(fluorite._surf, (180, 180))

show_apatite = True
apatite = Actor('apatite')
apatite.topleft = (3250, 360)
# apatite._surf = pygame.transform.scale(apatite._surf, (180, 180))

show_silver = True
silver = Actor('silver')
silver.topleft = (4250, 380)
# silver._surf = pygame.transform.scale(silver._surf, (180, 180))

show_opal = True
opal = Actor('opal')
opal.topleft = (5250, 400)
# opal._surf = pygame.transform.scale(opal._surf, (180, 180))

show_topaz = True
topaz = Actor('topaz')
topaz.topleft = (6250, 380)
# topaz._surf = pygame.transform.scale(topaz._surf, (180, 180))
 
show_amethyst = True
amethyst = Actor('amethyst')
amethyst.topleft = (7250, 360)
# amethyst._surf = pygame.transform.scale(amethyst._surf, (180, 180))

show_tungsten_carbide = True
tungsten_carbide = Actor('tungsten_carbide')
tungsten_carbide.topleft = (8250, 380)
# tungsten_carbide._surf = pygame.transform.scale(tungsten_carbide._surf, (180, 180))


# Grid placeholders (slightly bigger than the powders)
TB_SLOT_W = 90
TB_SLOT_H = 90
TB_GAP = 0
TB_GRID_WIDTH = 8 * TB_SLOT_W + 7 * TB_GAP
TB_START_X = (WIDTH - TB_GRID_WIDTH) // 2
TB_START_Y = 10
tb_slots = []
for i in range(8):
    x = TB_START_X + i * (TB_SLOT_W + TB_GAP)
    tb_slots.append(Rect((x, TB_START_Y), (TB_SLOT_W, TB_SLOT_H)))
    # Semi-transparent fill for each grid cell
    tb_slot_surface = pygame.Surface((TB_SLOT_W, TB_SLOT_H), pygame.SRCALPHA)
    tb_slot_surface.fill((0, 0, 0, 120))   # black, alpha 120 (0 = invisible, 255 = solid)

# Top bar powder images
TB_POWDER_WIDTH = 80
TB_POWDER_HEIGHT = 55
talc_powder_tb = Actor('talc_powder')
talc_powder_tb._surf = pygame.transform.scale(talc_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
talc_powder_tb.topleft = (tb_slots[0].left + 5, tb_slots[0].top + 15)

fluorite_powder_tb = Actor('fluorite_powder')
fluorite_powder_tb._surf = pygame.transform.scale(fluorite_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
fluorite_powder_tb.topleft = (tb_slots[1].left + 5, tb_slots[1].top + 15)

apatite_powder_tb = Actor('apatite_powder')
apatite_powder_tb._surf = pygame.transform.scale(apatite_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
apatite_powder_tb.topleft = (tb_slots[2].left + 5, tb_slots[2].top + 15)

silver_powder_tb = Actor('silver_powder')
silver_powder_tb._surf = pygame.transform.scale(silver_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
silver_powder_tb.topleft = (tb_slots[3].left + 5, tb_slots[3].top + 15)

opal_powder_tb = Actor('opal_powder')
opal_powder_tb._surf = pygame.transform.scale(opal_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
opal_powder_tb.topleft = (tb_slots[4].left + 5, tb_slots[4].top + 15)

topaz_powder_tb = Actor('topaz_powder')
topaz_powder_tb._surf = pygame.transform.scale(topaz_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
topaz_powder_tb.topleft = (tb_slots[5].left + 5, tb_slots[5].top + 15)

amethyst_powder_tb = Actor('amethyst_powder')
amethyst_powder_tb._surf = pygame.transform.scale(amethyst_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
amethyst_powder_tb.topleft = (tb_slots[6].left + 5, tb_slots[6].top + 15)

tungsten_carbide_powder_tb = Actor('tungsten_carbide_powder')
tungsten_carbide_powder_tb._surf = pygame.transform.scale(tungsten_carbide_powder_tb._surf, (TB_POWDER_WIDTH, TB_POWDER_HEIGHT))
tungsten_carbide_powder_tb.topleft = (tb_slots[7].left + 5, tb_slots[7].top + 15)

# Coins
coins = 175

# Mineral popup
show_mineral_popup = False
clicked_mineral = ''

MINERAL_POPUP_WIDTH = 550
MINERAL_POPUP_HEIGHT = 400
DARK_TRANSPARENT = (0, 0, 0, 64)

popup_x = (WIDTH - MINERAL_POPUP_WIDTH) // 2    # Equals 200
popup_y = (HEIGHT - MINERAL_POPUP_HEIGHT) // 2  # Equals 75
mineral_popup_rect = Rect((popup_x, popup_y), (MINERAL_POPUP_WIDTH, MINERAL_POPUP_HEIGHT))

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
GAP = 30  # Space between OK and Cancel buttons

button_y = popup_y + MINERAL_POPUP_HEIGHT - 60  
go_to_store_x = (WIDTH // 2) - BUTTON_WIDTH - (GAP // 2)      # Equals 500 - 100 - 15 = 385
cancel_x = (WIDTH // 2) + (GAP // 2)                  # Equals 500 + 15 = 515

mineral_popup_go_to_store_button = Rect((go_to_store_x, button_y), (BUTTON_WIDTH, BUTTON_HEIGHT))
mineral_popup_cancel_button = Rect((cancel_x, button_y), (BUTTON_WIDTH, BUTTON_HEIGHT))

mineral_popup_surface = pygame.Surface((MINERAL_POPUP_WIDTH, MINERAL_POPUP_HEIGHT), pygame.SRCALPHA)
mineral_popup_surface.fill((0, 0, 0, 230))

# Tool store popup
show_store_popup = False
selected_tool = ''   # e.g. 'finger_nail', or '' if none selected

STORE_WIDTH = 700
STORE_HEIGHT = 480
store_x = (WIDTH - STORE_WIDTH) // 2
store_y = (HEIGHT - STORE_HEIGHT) // 2

store_rect = Rect((store_x, store_y), (STORE_WIDTH, STORE_HEIGHT))
store_surface = pygame.Surface((STORE_WIDTH, STORE_HEIGHT), pygame.SRCALPHA)
store_surface.fill((0, 0, 0, 230))

store_close_button = Rect((store_x + STORE_WIDTH - 300, store_y + STORE_HEIGHT - 60), (110, 40))
buy_and_scratch_button = Rect((store_x + STORE_WIDTH - 500, store_y + STORE_HEIGHT - 60), (110, 40))
TOOL_SIZE = 60
# Tool images (put PNGs in images/ with these names)
finger_nail = Actor('finger_nail')
bronze_bell = Actor('bronze_bell')
nannys_teeth = Actor('nannys_teeth')
toilet_fragment = Actor('toilet_fragment')
steel_axe = Actor('steel_axe')
diamond_drill = Actor('diamond_drill')

bronze_bell._surf = pygame.transform.scale(bronze_bell._surf, (50, 60))
nannys_teeth._surf = pygame.transform.scale(nannys_teeth._surf, (60, 50))

# Resize and place them in a 3x2 grid
tool_actors = [finger_nail, bronze_bell, nannys_teeth, toilet_fragment, steel_axe, diamond_drill]

for i, tool in enumerate(tool_actors):
    # tool._surf = pygame.transform.scale(tool._surf, (60, 60))
    tool.topleft = (store_x + 40 + i * 110, store_y + 70)

tool_costs = {
    'finger_nail': 5,
    'bronze_bell': 10,
    'nannys_teeth': 15,
    'toilet_fragment': 20,
    'steel_axe': 30,
    'diamond_drill': 35,
}

tool_stories = {
    'finger_nail': (
        "Last week, Nanny cut me clean off with her nail cutter. However, the momentum of the cut hurled me up and jammed me in nanny's {silver} necklace. To her disappointment, when she got me off for her weird teeth and nail collection, I scraped a whole line in her necklace. Nanny calmed down from her rage as she laid me down in the collection. The {teeth} did scrape me a bit, but it was pretty cozy in there. Everything went well until I ended up in this cave... Wait! I still remember that {silver} scores 2.5 on the Mohs scale and {teeth} score a bit higher than 4.5. This must come in handy later."
    ),
    'bronze_bell': (
        "I once stood in a legendary bell tower and an {opal} hammer hit me every hour. Every hit severely scratched me and weakened me to the point I plummeted 51 storeys down to the luxury {marble} floor, scraping a long, terrible line into it. The enraged tower owner kicked me out into the field and left me there, maybe forever. A year later, I got stranded here the same way as you did... Oh! I still have some information for you. {Marble} has a Mohs scale of about 2.5 to 3, and {opal} scores a little lower than 6.5. This must be useful!"
    ),
    'nannys_teeth': (
        "About a year ago, I lived happily inside nanny's mouth, until an irresponsible person launched their soccer ball right into me! I did not completely fall off, but I was left dangling by a part of my root! How rude! Then Nanny's crazy dentists knocked me off with the hardest mineral on Earth—{diamond}. I tumbled down to the floor, covered in scratches. And oh! Please wash me. I'm covered in {steel} dust from when nanny bit her fork. Also, nanny now has one less tooth. Hehe!"
    ),
    'toilet_fragment': (
        "Once upon a time, the president was sitting on me normally but little did we know, something did not go as planned. Just then, a World War I grenade exploded and blasted me into pieces. The president did survive, but I was not so lucky. I flew for what seemed like ages, blasting through rocks like {orthoclase} but being scratched multiple times by {tungsten}. Then finally, I landed here.. Oh! I can remember that {tungsten} has a Mohs scale of 8, and {orthoclase} scores a 6. This may be important."
    ),
    'steel_axe': (
        "My story all started in the legendary cavern of the north, where an evil wizard used me to punish all who stepped into his territory. After so many years had passed, the wizard hurled me out into the wild. I was damaged countless times by rocks like {topaz}, but I managed to stand up to a few {animal claw fragments} left there by vultures. Then, the witch found me to chop a few wood logs for the fireplace. oh! Forgot to tell you, quick tip. The Mohs scale for the {topaz} that bullied me is 8 and the {animal claw fragments} score around 2.5."
    ),
    'diamond_drill': (
        "Okay! I will tell you my story. It all began in the weapon factory where I drilled into {every single mineral}. Then, in World War I, a grenade detonated and blasted me outside. When I landed, I crushed a weird rabbit that was desperate to catch me. That time, I also cracked some {tungsten} ore, which did not even hurt. Then after 100 years, I ended up in this cave... Oh! I know why the rabbit wanted me. It is because I am dense and weigh more carats (carrots)."
    ),
}

# Map actor -> name key (so clicks know which tool was clicked)
tool_names = {
    finger_nail: 'finger_nail',
    bronze_bell: 'bronze_bell',
    nannys_teeth: 'nannys_teeth',
    toilet_fragment: 'toilet_fragment',
    steel_axe: 'steel_axe',
    diamond_drill: 'diamond_drill',
}
# Mohs scale
mineral_hardness = {'Talc': 1, 'Fluorite': 4, 'Apatite': 5, 'Silver': 2.5, 'Opal': 6, 'Topaz': 8, 'Amethyst': 7, 'Tungsten Carbide': 9,}
tool_hardness = {'finger_nail': 2.5, 'bronze_bell': 3, 'nannys_teeth': 5, 'toilet_fragment': 7, 'steel_axe': 4, 'diamond_drill': 10}
show_silver = True

# End game popup
show_end_game_popup = False
end_game_popup_WIDTH = 850
end_game_popup_HEIGHT = 500
end_game_popup_x = (WIDTH - end_game_popup_WIDTH) // 2
end_game_popup_y = (HEIGHT - end_game_popup_HEIGHT) // 2
end_game_popup_rect = Rect((end_game_popup_x, end_game_popup_y), (end_game_popup_WIDTH, end_game_popup_HEIGHT))
end_game_popup_surface = pygame.Surface((end_game_popup_WIDTH, end_game_popup_HEIGHT), pygame.SRCALPHA)
end_game_popup_surface.fill((0, 0, 0, 230))
end_game_button = Rect((end_game_popup_x + 370, end_game_popup_y + end_game_popup_HEIGHT - 60), (110, 40))

# Scratch result popup
show_result_popup = False
result_image = None
result_message = ''
RESULT_WIDTH = 400
RESULT_HEIGHT = 280
result_x = (WIDTH - RESULT_WIDTH) // 2
result_y = (HEIGHT - RESULT_HEIGHT) // 2
result_rect = Rect((result_x, result_y), (RESULT_WIDTH, RESULT_HEIGHT))
result_surface = pygame.Surface((RESULT_WIDTH, RESULT_HEIGHT), pygame.SRCALPHA)
result_surface.fill((0, 0, 0, 230))
result_ok_button = Rect((result_x + (RESULT_WIDTH - 110) // 2, result_y + RESULT_HEIGHT - 60), (110, 40))

# Intro popup
show_intro_popup = True
intro_popup_WIDTH = 1100
intro_popup_HEIGHT = 600

the_intro_bg = Actor('the_intro_bg')
the_intro_bg._surf = pygame.transform.scale(the_intro_bg._surf, (1100, 600))
the_intro_bg.topleft = (0, 0)

the_into_surface = pygame.Surface((intro_popup_WIDTH, intro_popup_HEIGHT), pygame.SRCALPHA)
the_into_surface.fill((0, 0, 0, 100))

intro_popup_ok_button = Rect((WIDTH // 2 - 60, HEIGHT - 100), (120, 60))

# Sounds
music.set_volume(0.4)
music.play("intro")

click_sound = pygame.mixer.Sound("music/click.mp3")
click_sound.set_volume(0.5)

powder_collect_sound = pygame.mixer.Sound("music/powder_collect.mp3")
powder_collect_sound.set_volume(0.6)

tool_break_sound = pygame.mixer.Sound("music/tool_break.mp3")
tool_break_sound.set_volume(0.6)

def draw_intro_popup():
    # draw background
    the_intro_bg.draw()
    screen.blit(the_into_surface, (0, 0))

    # draw text
    draw_story(
        story="{Mineral Explorer}",
        x=300,
        y=55,
        max_width=600,
        fontsize=96,
    )

    draw_story(
        story="How to play:",
        x=495,
        y=150,
        max_width=300,
        fontsize=42,
    )

    draw_story(
        story="Click a {mineral} -> Purchase a {tool} -> Scratch & Collect {Powders}!",
        x=240,
        y=200,
        max_width=700,
        fontsize=32,
    )

    draw_story(
        story="How to win:",
        x=500,
        y=250,
        max_width=300,
        fontsize=42,
    )

    draw_story(
        story="The {more} powders you collect, the {higher} your score!",
        x=300,
        y=300,
        max_width=600,
        fontsize=32,
    )

    draw_story(
        story="The Science behind:",
        x=430,
        y=350,
        max_width=400,
        fontsize=42,
    )

    draw_story(
        story=(
            "{Minerals}: Minerals are naturally formed substances, often found in bodies of rock called ores."
            "{Mohs Scale}: A scale of mineral hardness from 1 to 10, "
            "with 1 being the softest and 10 being the hardest. "
            "Only a tool harder or the same hardness as the mineral can scratch it."
        ),
        x=50,
        y=400,
        max_width=1000,
        fontsize=32,
    )

    # draw buttons
    screen.draw.filled_rect(intro_popup_ok_button, "orange")
    screen.draw.text("Enter Game", center=intro_popup_ok_button.center, fontsize=24, color="white")

def scratching():
    global coins, show_store_popup, show_result_popup
    global result_image, result_message, coin_left_message, selected_tool, scratch_result
    global show_talc
    global show_fluorite
    global show_apatite
    global show_silver
    global show_opal
    global show_topaz
    global show_amethyst
    global show_tungsten_carbide
    global show_end_game_popup
    global collected_talc
    global collected_fluorite
    global collected_apatite
    global collected_silver
    global collected_opal
    global collected_topaz
    global collected_amethyst
    global collected_tungsten_carbide


    if selected_tool == '':
        return # Have to select a tool first

    cost = tool_costs[selected_tool]

    # Pay money
    coins -= cost
    coin_left_message = f"Coins left: {coins}"
    mineral = clicked_mineral
    if mineral == '':
        return # Have to click a mineral first

    m_hard = mineral_hardness[mineral]
    t_hard = tool_hardness[selected_tool]

    if t_hard >= m_hard:
        # Tool is stronger than mineral
        powder_collect_sound.play()
        powder_name = mineral.lower().replace(' ', '_') + '_powder'   # Powder

        result_image = Actor(powder_name)
        result_image._surf = pygame.transform.scale(result_image._surf, (100, 70))
        result_image.center = (WIDTH // 2, result_y + 90)
        result_message = f"The {selected_tool.replace('_', ' ')} scratched the {mineral} into powder!"
        scratch_result = "POWDER COLLECTED!"
        if mineral == 'Talc':
            collected_talc = True
        if mineral == 'Fluorite':
            collected_fluorite = True
        if mineral == 'Apatite':
            collected_apatite = True
        if mineral == 'Silver':
            collected_silver = True
        if mineral == 'Topaz':
            collected_topaz = True
        if mineral == 'Opal':
            collected_opal = True
        if mineral == 'Tungsten Carbide':
            collected_tungsten_carbide = True
        if mineral == 'Amethyst':
            collected_amethyst = True

        if mineral == 'Talc':
            show_talc = False
        if mineral == 'Fluorite':
            show_fluorite = False
        if mineral == 'Apatite':
            show_apatite = False
        if mineral == 'Silver':
            show_silver = False
        if mineral == 'Topaz':
            show_topaz = False
        if mineral == 'Opal':
            show_opal = False
        if mineral == 'Tungsten Carbide':
            show_tungsten_carbide = False
        if mineral == 'Amethyst':
            show_amethyst = False


    else:# Mineral wins → tool breaks
        tool_break_sound.play()
        broken_name = selected_tool + '_broken'
        result_image = Actor(broken_name)
        # result_image._surf = pygame.transform.scale(result_
        # image._surf, (120, 120))
        result_image.center = (WIDTH // 2, result_y + 90)
        result_message = f"The {mineral} was harder! Your {selected_tool.replace('_', ' ')} broke!"
        scratch_result = "TOOL BROKEN!"

    show_result_popup = True
    show_store_popup = False
 
def result_popup():
    screen.blit(result_surface, (result_x, result_y))
    screen.draw.rect(result_rect, (200, 200, 200))

    screen.draw.text(
        scratch_result,
        center = (WIDTH // 2, result_y + 25),
        fontsize = 28,
        color = "orange",
    )
    
    if result_image is not None:
        result_image.draw()

    screen.draw.text(
    result_message,
    center=(WIDTH // 2, result_y + 155),
    fontsize=24,
    color="white",
    width=350,
)

    screen.draw.text(
        coin_left_message,
        center=(WIDTH // 2, result_y + 195),
        fontsize=28,
        color=Ocean if coins > 0 else "red",
    )

    screen.draw.filled_rect(result_ok_button, "orange")
    screen.draw.text("OK", center=result_ok_button.center, fontsize=20, color="white")


def mineral_popup(mineral):
    # Popup box frame
    screen.blit(mineral_popup_surface, (popup_x, popup_y))
    screen.draw.rect(mineral_popup_rect, (200, 200, 200))

    # Popup message text
    popup_title = ''
    popup_message = ''
    if mineral == 'Talc':
        popup_title = 'TALC'
        popup_mohs_scale = 'Mohs Scale 1'
        popup_message = 'Talc is the {softest} mineral on the planet. It is found in a wide range of {everyday things}, and you probably have used it without knowing. Talc is used in objects like baby powder and cosmetics. A form of talc known as {soapstone} could also be found in {ornamental objects} and {practical things}, like sinks, bowls and... tyres? I hate to think about driving on the softest mineral on earth.'

    if mineral == 'Fluorite':
        popup_title = 'FLUORITE'
        popup_mohs_scale = 'Mohs Scale 4'
        popup_message = "Fluorite is a beautiful, {fluorescent} mineral that has a name that came from the ancient Roman language, {Latin}! It is also the primary source of {fluorine}, making it essential for all sorts of things. Fluorite is used in {toothpaste}, {non-stick cookware coatings}, {refrigerator coolants}, {plastics}, and {the lenses of cameras}. It could also be found in {glass}! There's no way this thing could get more useful. Otherwise, our houses are going to be flooded by the stuff!"
    
    if mineral == 'Apatite':
        popup_title = 'APATITE'
        popup_mohs_scale = 'Mohs Scale 5'
        popup_message ="Apatite is a {translucent} mineral that is perfect for {agriculture} and {industrial uses}, due to its high {phosphorus} content. Apatite could also be used to make {jewellery}, and like many other minerals, is used in {toothpaste}. It is important {medically} too, as it can help with joint repair. Wow! Apatite is an amazing mineral! I'm just sad that it will not increase my appetite."

    if mineral == 'Silver':
        popup_title = 'SILVER'
        popup_mohs_scale = 'Mohs Scale 2.5'
        popup_message = "Silver is a very {soft}, {precious} metal and very {expensive}, often found in the ores of other minerals. It is ideal for {jewellery} due to its resistance to tarnish and its lustre. Silver is also highly praised for its high {electrical conductivity}, which is better than any other metal. That is why many of the best electrical devices use silver. Ah, so that's why they cost that much. It can't be cheap with expensive metals and so many details. Right?"

    if mineral == 'Opal':
        popup_title = 'OPAL'
        popup_mohs_scale = 'Mohs Scale 6'
        popup_message = "Opals are precious gemstones found especially in {Australia}. They are commonly found in {jewellery}, and are used in a wide range of {microscopic filtration systems} and {cosmetics}. Opals are also the {birthstone of October}, and the gem for a {fourteenth wedding anniversary}. They are composed of {silica with water}, and form over very {long periods of time} underground. Opals may be expensive minerals, but aren't quite as rare as {koalas} and {kangaroos}. They are both found in Australia, but opals are {not only} found in Australia."

    if mineral == 'Topaz':
        popup_title = 'TOPAZ'
        popup_mohs_scale = 'Mohs Scale 8'
        popup_message = "Topaz is a highly {durable} mineral, making it perfect for {jewellery} like many other minerals. It is also highly valued in {industrial things}, often used in kilns, furnaces, glass making and the production of fluorine. Topaz can be found in {ceramics} and {glass-casting moulds} too. They can even grow to be giants, like the 600-pound {rock} in the American Museum of Natural History in New York! Wow! Topaz is amazing! But could you imagine a thing that is put in kilns and is heavier than a piano in your house?"

    if mineral == 'Amethyst':
        popup_title = 'AMETHYST'
        popup_mohs_scale = 'Mohs Scale 7'
        popup_message = "Amethysts are {quartz crystals} that form in rock bubbles called {geodes}. They have that beautiful purple colour due to natural {radiation from iron}, and are perfect to use in {decoration or jewellery}. They could also be used to help with {concentration and focus}. There even was an ancient Greek belief that amethysts prevented intoxication! Isn't it amazing? Who knew ugly rocks could be piñatas?"

    if mineral == 'Tungsten Carbide':
        popup_title = 'TUNGSTEN CARBIDE'
        popup_mohs_scale = 'Mohs Scale 9'
        popup_message = "Tungsten carbide is an {extremely hard and dense} mineral composed of {tungsten} and a bit of {carbon}. It is twice as dense as steel and has a {sky-high melting point} of 3422°C or 6191°F, which is the highest of any metal. Due to its high durability, tungsten carbide is used in {drills}, {saws}, {drone propellers}, {heavy-duty saw blades} and {valves that undergo severe friction}. However, sometimes {cobalt} is added to provide more impact resistance. Who knew the metal with the highest melting point needs hardness support?"
   
    screen.draw.text(popup_title, center=(WIDTH // 2, popup_y + 30), fontsize=32, color="orange")
    screen.draw.text(popup_mohs_scale, center=(WIDTH // 2, popup_y + 65), fontsize=28, color=Grass)
    # screen.draw.text(popup_message, center=(WIDTH // 2, popup_y + 140), fontsize=24, color="white", width=450)

    draw_story(
        popup_message,
        popup_x + 40,
        popup_y + 90,
        475,
        fontsize=24,
    )

    # --- GO TO STORE BUTTON (Green) ---
    screen.draw.filled_rect(mineral_popup_go_to_store_button, Grass)  # Green background
    screen.draw.text("GO TO STORE", center=mineral_popup_go_to_store_button.center, fontsize=20, color="white", bold=True)

    # --- CANCEL BUTTON (Orange) ---
    screen.draw.filled_rect(mineral_popup_cancel_button, "orange")
    screen.draw.text("CANCEL", center=mineral_popup_cancel_button.center, fontsize=20, color="white", bold=True)


def store_popup():
    # Dark box
    screen.blit(store_surface, (store_x, store_y))
    screen.draw.rect(store_rect, (200, 200, 200))

    # Title
    screen.draw.text("TOOL STORE", center=(WIDTH // 2, store_y + 25), fontsize=32, color="orange")

    # Draw each tool + its cost underneath
    for tool in tool_actors:
        tool.draw()
        name = tool_names[tool]
        cost = tool_costs[name]

        # Orange box around the selected tool
        if selected_tool == name:
            highlight = Rect(
                (tool.left - 3, tool.top - 3),
                (TOOL_SIZE + 6, TOOL_SIZE + 6),
            )
            screen.draw.rect(highlight, "orange")

        screen.draw.text(
            name.replace('_', ' '),
            center=(tool.left + 30, tool.top + 75),
            fontsize=20,
            color="white",
        )

        screen.draw.text(
            f"{cost} coins",
            center=(tool.left + 30, tool.top + 95),
            fontsize=18,
            color="orange",
        )
        

    # Story under the grid
    if selected_tool == '':
        draw_story(
            "{Click a tool} to hear its story.",
            store_x + 220,
            store_y + 230,
            640,
            fontsize=28,
        )

        draw_story(
            "Read the story carefully, as there are some {clues} inside.",
            store_x + 100,
            store_y + 280,
            640,
            fontsize=28,
        )
    else:
        draw_story(
            tool_stories[selected_tool],
            store_x + 30,
            store_y + 200,
            640,
            fontsize=24,
        )

    # Close button
    screen.draw.filled_rect(store_close_button, "orange")
    screen.draw.text("CLOSE", center=store_close_button.center, fontsize=20, color="white")

    # Buy & scratch button
    if selected_tool != '' and coins >= tool_costs[selected_tool]:
        screen.draw.filled_rect(buy_and_scratch_button, Grass)
    else:
        screen.draw.filled_rect(buy_and_scratch_button, "grey")

    screen.draw.text("BUY & SCRATCH", center=buy_and_scratch_button.center, fontsize=20, color="white")


def draw():
    if show_intro_popup:
        draw_intro_popup()
        return

    the_depths_bg.draw()
    main_character.draw()
    grid_center_x = TB_START_X + (8 * TB_SLOT_W) // 2
    grid_bottom_y = TB_START_Y + TB_SLOT_H
    screen.draw.text(
        "Powders Collected",
        center=(grid_center_x, grid_bottom_y + 15),
        fontsize=26,
        color="white",
    )

    screen.draw.text(
        f'Coins: {coins}', 
        (20, 45),
        color=(Ocean), 
        fontsize = 40
    )

    for slot in tb_slots:
        screen.blit(tb_slot_surface, (slot.left, slot.top)) 
        screen.draw.rect(slot, "orange")

    if collected_talc:
        talc_powder_tb.draw()
    if collected_fluorite:
        fluorite_powder_tb.draw()
    if collected_apatite:
        apatite_powder_tb.draw()
    if collected_silver:
        silver_powder_tb.draw()
    if collected_opal:
        opal_powder_tb.draw()
    if collected_topaz:
        topaz_powder_tb.draw()
    if collected_amethyst:
        amethyst_powder_tb.draw()
    if collected_tungsten_carbide:
        tungsten_carbide_powder_tb.draw()

    if show_end_game_popup:
        end_game_popup()

    if show_talc:
        talc.draw()

    if show_fluorite:
        fluorite.draw()

    if show_apatite:
        apatite.draw()

    if show_silver:
        silver.draw()

    if show_opal:
        opal.draw()

    if show_topaz:
        topaz.draw()
    
    if show_amethyst:  
        amethyst.draw()

    if show_tungsten_carbide:
        tungsten_carbide.draw()

    if show_mineral_popup:
        mineral_popup(mineral=clicked_mineral)

    if show_store_popup:
        store_popup()

    if show_result_popup:
        result_popup()

def update():
    main_character.animate()
    if not show_mineral_popup and not show_store_popup and not show_intro_popup and not show_result_popup and not show_end_game_popup:
        move_mineral()



def get_most_distant_mineral_right():
    minerals = [talc, fluorite, apatite, silver, opal, topaz, amethyst, tungsten_carbide]
    farthest_mineral = max(minerals, key=lambda x: x.right)
    return farthest_mineral.right


def move_mineral():
    speed = 3.5
    if show_talc:
        talc.left -= speed
    if talc.right < 0:
        talc.left = get_most_distant_mineral_right() + 1000

    if show_fluorite:
        fluorite.left -= speed
    if fluorite.right < 0:
        fluorite.left = get_most_distant_mineral_right() + 1000
    
    if show_apatite:
        apatite.left -= speed
    if apatite.right < 0:
        apatite.left = get_most_distant_mineral_right() + 1000

    if show_silver:
        silver.left -= speed
    if silver.right < 0:
        silver.left = get_most_distant_mineral_right() + 1000

    if show_opal:
        opal.left -= speed
    if opal.right < 0:
        opal.left = get_most_distant_mineral_right() + 1000
    
    if show_topaz:
        topaz.left -= speed
    if topaz.right < 0:
        topaz.left = get_most_distant_mineral_right() + 1000
    
    if show_amethyst:
        amethyst.left -= speed
    if amethyst.right < 0:
        amethyst.left = get_most_distant_mineral_right() + 1000
    
    if show_tungsten_carbide:
        tungsten_carbide.left -= speed
    if tungsten_carbide.right < 0:
        tungsten_carbide.left = get_most_distant_mineral_right() + 1000

def on_mouse_down(pos):
    global show_mineral_popup, clicked_mineral
    global show_store_popup, selected_tool
    global show_result_popup, result_image, result_message
    global coins
    global show_end_game_popup
    global show_intro_popup

    # Intro popup
    if show_intro_popup:
        if intro_popup_ok_button.collidepoint(pos):
            click_sound.play()
            show_intro_popup = False
            music.play("into_the_deep")
            return
        return

    # Ending
    if show_end_game_popup:
        if end_game_button.collidepoint(pos):
            click_sound.play()
            exit()
        return
    

    # Result popup
    if show_result_popup:
        if result_ok_button.collidepoint(pos):
            click_sound.play()
            show_result_popup = False
            result_image = None
            result_message = ''
            selected_tool = ''

            powders_collected = (
                collected_talc
                + collected_fluorite
                + collected_apatite
                + collected_silver
                + collected_opal
                + collected_topaz
                + collected_amethyst
                + collected_tungsten_carbide
            )

            if coins == 0 or powders_collected == 8:
                show_end_game_popup = True
                music.play("end_game")
        return

        for tool in tool_actors:
            if tool.collidepoint(pos):
                click_sound.play()
                selected_tool = tool_names[tool]
                return
        return

  
    # Store popup
    if show_store_popup:
        if store_close_button.collidepoint(pos):
            click_sound.play()
            show_store_popup = False
            selected_tool = ''
            return
        if buy_and_scratch_button.collidepoint(pos):
            click_sound.play()
            if selected_tool != '' and coins >= tool_costs[selected_tool]:
                scratching()
            return
        for tool in tool_actors:
            if tool.collidepoint(pos):
                click_sound.play()
                selected_tool = tool_names[tool]
                return
        return   # block clicks from going to minerals

    if show_result_popup:
        if result_ok_button.collidepoint(pos):
            click_sound.play()
            show_result_popup = False
            result_image = None
            result_message = ''
            selected_tool = ''
            return

    if show_mineral_popup:
        if mineral_popup_cancel_button.collidepoint(pos):
            click_sound.play()
            show_mineral_popup = False
            return

        if mineral_popup_go_to_store_button.collidepoint(pos):
            click_sound.play()
            show_mineral_popup = False
            show_store_popup = True
            selected_tool = ''
            return
        return

    if show_talc and talc.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Talc'
    
    if show_fluorite and fluorite.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Fluorite'   

    if show_apatite and apatite.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Apatite'

    if show_silver and silver.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Silver'

    if show_opal and opal.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Opal'
    
    if show_topaz and topaz.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Topaz'
    
    if show_amethyst and amethyst.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Amethyst'
    
    if show_tungsten_carbide and tungsten_carbide.collidepoint(pos):
        click_sound.play()
        show_mineral_popup = True
        clicked_mineral = 'Tungsten Carbide'

import re   # put this with your other imports at the top

def draw_story(story, x, y, max_width, fontsize=24, highlight_color="orange"):
    parts = re.split(r'(\{[^{}]+\})', story)

    font = pygame.font.Font(None, fontsize)
    space_w = font.size(' ')[0]

    cursor_x = x
    cursor_y = y
    line_height = fontsize + 1

    for part in parts:
        if part == '':
            continue

        if part.startswith('{') and part.endswith('}'):
            color = highlight_color
            text = part[1:-1]
        else:
            color = "white"
            text = part

        for word in text.split(' '):
            if word == '':
                continue

            word_w = font.size(word)[0]

            if cursor_x > x and cursor_x + word_w > x + max_width:
                cursor_x = x
                cursor_y += line_height

            screen.draw.text(word, (cursor_x, cursor_y), fontsize=fontsize, color=color)
            cursor_x += word_w + space_w


def end_game_popup():
    powders_collected = (
        collected_talc
        + collected_fluorite
        + collected_apatite
        + collected_silver
        + collected_opal
        + collected_topaz
        + collected_amethyst
        + collected_tungsten_carbide
    )

    score = (collected_talc * 1 + collected_fluorite * 3 + collected_apatite * 4 + collected_silver * 2 + collected_opal * 5 + collected_topaz * 7 + collected_amethyst * 6 + collected_tungsten_carbide * 8) * powders_collected
    screen.blit(end_game_popup_surface,(end_game_popup_x, end_game_popup_y))
    screen.draw.rect(end_game_popup_rect, (200, 200, 200))

    screen.draw.text(
        "GAME FINISHED ON 0 COINS LEFT" if coins == 0 else "GAME FINISHED ON ALL POWDERS COLLECTED",
        center = (WIDTH // 2, end_game_popup_y + 30),
        fontsize = 36,
        color = "orange",
    )

    # add star icon
    STAR_SIZE = 40

    star_icons = []
    for i in range(5):
        star = Actor("star")
        star._surf = pygame.transform.scale(
            star._surf,
            (STAR_SIZE, STAR_SIZE),
        )
        star_icons.append(star)

    if score == 288:
        star_count = 5
    elif score > 190:
        star_count = 3
    elif score > 70:
        star_count = 2
    else:
        star_count = 1

    STAR_GAP = 8
    stars_y = end_game_popup_y + 55

    stars_width = (
        star_count * STAR_SIZE
        + (star_count - 1) * STAR_GAP
    )
    stars_start_x = WIDTH // 2 - stars_width // 2

    for i in range(star_count):
        star_icons[i].topleft = (
            stars_start_x + i * (STAR_SIZE + STAR_GAP),
            stars_y,
        )
        star_icons[i].draw()

    # score text
    draw_story(
        (f"Your score is {score}!"),
        x = WIDTH // 2 - 100,
        y = end_game_popup_y + 105,
        max_width = 350,
        fontsize = 36,
        highlight_color = "orange",
    )

    screen.draw.filled_rect(end_game_button,"orange")
    screen.draw.text("END THE GAME", center=end_game_button.center, fontsize=20, color="white")
 
    global show_talc
    global show_fluorite
    global show_apatite
    global show_silver
    global show_opal
    global show_topaz
    global show_amethyst
    global show_tungsten_carbide

    show_talc = False
    show_fluorite = False
    show_apatite = False
    show_silver = False
    show_opal = False
    show_topaz = False
    show_amethyst = False
    show_tungsten_carbide = False


    collected_names = []
    if collected_talc:
        collected_names.append("Talc")
    if collected_fluorite:
        collected_names.append("Fluorite")
    if collected_apatite:
        collected_names.append("Apatite")
    if collected_silver:
        collected_names.append("Silver")
    if collected_opal:
        collected_names.append("Opal")
    if collected_topaz:
        collected_names.append("Topaz")
    if collected_amethyst:
        collected_names.append("Amethyst")
    if collected_tungsten_carbide:
        collected_names.append("Tungsten Carbide")

    if collected_names:
        mineral_names = ", ".join(collected_names)
    else:
        mineral_names = "None"


    if powders_collected == 8:
        collected_message = f"Amazing! You collected powders from all {powders_collected} minerals!: {mineral_names}."
    else:
        collected_message = f"You collected powders from {powders_collected} minerals: {mineral_names}."
    screen.draw.text(
        collected_message,
        center=(WIDTH // 2, end_game_popup_y + 155),
        fontsize=28,
        color="white",
        width=end_game_popup_WIDTH - 100,
    )

    # Mohs scale ruler
    ruler_left = end_game_popup_x + 75       # left end of the line
    ruler_right = end_game_popup_x + end_game_popup_WIDTH - 75   # right end
    ruler_y = end_game_popup_y + 300         # vertical position

    # rule label
    screen.draw.text(
        "Mohs Scale",
        center=(ruler_left, ruler_y + 45),
        fontsize=24,
        color="orange",
    )

    # main line
    screen.draw.line((ruler_left, ruler_y), (ruler_right, ruler_y), "white")

    # ticks and labels 0 to 10
    for i in range(11):
        tick_x = ruler_left + i * (ruler_right - ruler_left) // 10
        screen.draw.line((tick_x, ruler_y - 8), (tick_x, ruler_y + 8), "white")
        screen.draw.text(
            str(i),
            center=(tick_x, ruler_y + 22),
            fontsize=24,
            color="orange",
        )

    # place minerals on the ruler
    ruler_minerals = {}
    for m_name in mineral_hardness:
        RULER_ICON_W = 60
        RULER_ICON_H = 60
        if m_name == 'Opal':
            RULER_ICON_W = 40
        icon = Actor(m_name.lower().replace(' ', '_'))
        icon._surf = pygame.transform.scale(icon._surf, (RULER_ICON_W, RULER_ICON_H))
        ruler_minerals[m_name] = icon
    
    collected_flags = {
        'Talc': collected_talc,
        'Fluorite': collected_fluorite,
        'Apatite': collected_apatite,
        'Silver': collected_silver,
        'Opal': collected_opal,
        'Topaz': collected_topaz,
        'Amethyst': collected_amethyst,
        'Tungsten Carbide': collected_tungsten_carbide,
    }

    for i, (m_name, hardness) in enumerate(mineral_hardness.items()):
        # only show minerals that have been collected
        if not collected_flags[m_name]:
            continue

        icon_x = ruler_left + hardness * (ruler_right - ruler_left) / 10
        row_offset = 75 if i % 2 == 0 else 100   # alternate heights

        icon = ruler_minerals[m_name]
        icon.topleft = (icon_x - RULER_ICON_W // 2, ruler_y - row_offset)

        if m_name == 'Opal':
            icon.topleft = (icon_x - RULER_ICON_W // 2 + 10, ruler_y - row_offset)

        screen.draw.line((icon_x, ruler_y - row_offset + RULER_ICON_H + 5), (icon_x, ruler_y), "white")
        icon.draw()

    # place tools under the ruler
    ruler_tools = {}
    for t_name in tool_hardness:
        TOOL_ICON_W = 60
        TOOL_ICON_H = 60
        if t_name == 'bronze_bell':
            TOOL_ICON_W = 50
            TOOL_ICON_H = 60
        if t_name == 'nannys_teeth':
            TOOL_ICON_H = 40
        if t_name == 'finger_nail':
            TOOL_ICON_W = 50
            TOOL_ICON_H = 50
        icon = Actor(t_name)
        icon._surf = pygame.transform.scale(icon._surf, (TOOL_ICON_W, TOOL_ICON_H))
        ruler_tools[t_name] = icon

    for i, (t_name, hardness) in enumerate(tool_hardness.items()):
        icon_x = ruler_left + hardness * (ruler_right - ruler_left) / 10
        if t_name == 'finger_nail':
            row_offset = 25
        else:
            row_offset = 50

        icon = ruler_tools[t_name]
        icon.topleft = (icon_x - TOOL_ICON_W // 2, ruler_y + row_offset)

        # line from the ruler down to the top of the icon
        if t_name == 'finger_nail':
            screen.draw.line((icon_x, ruler_y), (icon_x, ruler_y + row_offset - 5), "white")
        else:
            screen.draw.line((icon_x, ruler_y + 30), (icon_x, ruler_y + row_offset - 5), "white")
        icon.draw()


pgzrun.go()