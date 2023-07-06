from Pygen import UI, Events, TileMap, Sprites, Animator
import pygame, time, json, datetime
from enum import Enum

pygame.init()

# creating the screen
screenSize = (600, 950)
screen = pygame.display.set_mode(screenSize)  # flags=pygame.RESIZABLE
pygame.display.set_caption("Mood Logger")

# the states of the application
class States (Enum):
    overview = 0
    entry = 1
    stats = 2

state = States.overview

# the save data
def SaveData():
    with open('mood.json', 'w') as f:
        json.dump(saveData, f, ensure_ascii=False, indent=4)

saveData = json.load(open("mood.json"))

# the current date
today = datetime.date.today()
date = today.strftime("%B-%d-%Y")

# making sure the current date is in the data base
if date not in saveData:
    saveData[date] = {
        "entries": [],
        "overview": {
            "sleep quality": 0,
            "sleep duration": [0, 0],
            "socialness": 0,
            "mood": 0,
            "fatigue": 0,
            "activity": 0,
            "overview": ""
        }
    }

# loading the days board
board = saveData[date]

# creating the buttons
color = UI.ColorPalette((61, 46, 34), (139, 81, 33), (191, 115, 41), (13, 18, 38))

    # stats
statsButton = [
    UI.Button((10, 10), (70, 20), color, "Back", textSize=15)
]

    # day overview
dayButtons = [
    UI.Button((10, 10), (70, 20), color, "Entry", textSize=15),
    UI.Button((300-75, 750), (150, 40), color, "Save", textSize=30),
    UI.Button((520, 10), (70, 20), color, "Stats", textSize=15)
]
dayText = [
    UI.TextRenderer(35, "pixel2.ttf", "Day Overview", (300, 35), color.textColor, True),
    UI.TextRenderer(35, "pixel2.ttf", "Sleep", (300, 75+17), color.textColor, True),
    UI.TextRenderer(35, "pixel2.ttf", "Mood Factors", (300, 315+30), color.textColor, True),
    UI.TextRenderer(35, "pixel2.ttf", "Description", (300, 615+30), color.textColor, True)
]
daySliders = [
    UI.Slider((150, 135), (300, 50), color, slide=board["overview"]["sleep quality"], backgroundText="quality"),
    UI.Slider((150, 195), (300, 50), color, slide=board["overview"]["sleep duration"][0], backgroundText="early - start - late"),
    UI.Slider((150, 255), (300, 50), color, slide=board["overview"]["sleep duration"][1], backgroundText="early -  end  - late"),
    UI.Slider((150, 375), (300, 50), color, slide=board["overview"]["mood"], backgroundText="overall mood"),
    UI.Slider((150, 435), (300, 50), color, slide=board["overview"]["socialness"], backgroundText="socialness"),
    UI.Slider((150, 495), (300, 50), color, slide=board["overview"]["fatigue"], backgroundText="fatigue"),
    UI.Slider((150, 555), (300, 50), color, slide=board["overview"]["activity"], backgroundText="activity")
]
dayTyping = [  # 675
    UI.TypingBox((100, 675), (400, 50), color)
]
dayTyping[0].text = board["overview"]["overview"]
dayTyping[0].forceUpdate = True

    # entries
entryButtons = [
    UI.Button((10, 15), (150, 40), color, "Save", textSize=30)
]
entryText = [
    UI.TextRenderer(35, "pixel2.ttf", "Entry", (300, 35), color.textColor, True)
]
entrySliders = [
    UI.Slider((150, 95), (300, 50), color, slide=0, backgroundText="overall mood"),
    UI.Slider((150, 155), (300, 50), color, slide=0, backgroundText="stress"),
    UI.Slider((150, 215), (300, 50), color, slide=0, backgroundText="anxiety"),
    UI.Slider((150, 275), (300, 50), color, slide=0, backgroundText="depression"),
    UI.Slider((150, 335), (300, 50), color, slide=0, backgroundText="happiness"),
    UI.Slider((150, 395), (300, 50), color, slide=0, backgroundText="suicidalness"),
    UI.Slider((150, 455), (300, 50), color, slide=0, backgroundText="fatigue"),
    UI.Slider((150, 515), (300, 50), color, slide=0, backgroundText="sleepiness"),
    UI.Slider((150, 575), (300, 50), color, slide=0, backgroundText="energy"),
    UI.Slider((150, 635), (300, 50), color, slide=0, backgroundText="lovedness"),
    UI.Slider((150, 695), (300, 50), color, slide=0, backgroundText="pain"),
    UI.Slider((150, 755), (300, 50), color, slide=0, backgroundText="socialness"),
    UI.Slider((150, 815), (300, 50), color, slide=0, backgroundText="hopefulness"),
    UI.Slider((150, 875), (300, 50), color, slide=0, backgroundText="activity")
]

# loading the background image
backgroundImage1 = pygame.Surface(screenSize)
backgroundImage1.blit(pygame.transform.scale(pygame.image.load("moodBackgroundImage.png"), [3456//4, 5184//4]), [-175, -40])
backgroundImage1.set_alpha(175)

backgroundImage2 = pygame.Surface((1200, 750))
backgroundImage2.blit(pygame.transform.scale(pygame.image.load("moodBackgroundImage2.png"), [5184//4, 3456//4]), [0, 0])
backgroundImage2.set_alpha(175)

backgroundImages = [backgroundImage1, backgroundImage2]
backgroundImage = backgroundImages[0]

# creating an event manager
events = Events.Manager()

# some time related things
dt = 1/120
fps = 0
desiredTime = 0  # 0 is unlimited, 1 / fps limits it to the fps desired
lastCheckedFps = time.time()

# running the game
while True:
    # the start of the frame
    frameStart = time.time()

    # getting the size of the screen (incase it got scaled or something)
    screenSize = screen.get_size()

    # updating the events
    events.GetEvents()
    
    # updaing the fps counter
    if time.time() - lastCheckedFps > 0.1:
        lastCheckedFps = time.time()
        fps = round(1 / dt)

    # clearing the screen
    screen.fill((225, 225, 225))
    screen.blit(backgroundImage, [0, 0])

    # checking which state is active
    if state == States.overview:
        # rendering the stuff for it
        for textBox in dayText:
            textBox.Render(screen)
        for slider in daySliders:
            slider.Render(screen, events)
        for typing in dayTyping:
            typing.Render(screen, events)
        for button in dayButtons:
            button.Render(screen, events)
        
        # checking if buttons were pressed
        if dayButtons[0].state == UI.Button.States.realeased:
            # changing the menu when the entry button is pressed
            state = States.entry
        elif dayButtons[1].state == UI.Button.States.realeased:
            # saving the info for the day overview
            board["overview"]["sleep quality"] = daySliders[0].slide
            board["overview"]["sleep duration"] = [daySliders[1].slide, daySliders[2].slide]
            board["overview"]["socialness"] = daySliders[4].slide
            board["overview"]["mood"] = daySliders[3].slide
            board["overview"]["fatigue"] = daySliders[5].slide
            board["overview"]["activity"] = daySliders[6].slide
            board["overview"]["overview"] = dayTyping[0].text

            SaveData()
        elif dayButtons[2].state == UI.Button.States.realeased:
            state = States.stats
            screenSize = (1200, 750)
            screen = pygame.display.set_mode(screenSize)  # flags=pygame.RESIZABLE
            backgroundImage = backgroundImages[1]
    elif state == States.entry:
        for textBox in entryText:
            textBox.Render(screen)
        for slider in entrySliders:
            slider.Render(screen, events)
        for button in entryButtons:
            button.Render(screen, events)
        
        # checking if the save button was pressed
        if entryButtons[0].state == UI.Button.States.realeased:
            # saving the entry
            entry = {}
            currentTime = datetime.datetime.now()
            entry["time"] = currentTime.hour + currentTime.minute/60
            entry["mood"] = entrySliders[0].slide
            entry["stress"] = entrySliders[1].slide
            entry["anxiety"] = entrySliders[2].slide
            entry["depression"] = entrySliders[3].slide
            entry["happiness"] = entrySliders[4].slide
            entry["suicidalness"] = entrySliders[5].slide
            entry["fatigue"] = entrySliders[6].slide
            entry["sleepiness"] = entrySliders[7].slide
            entry["energy"] = entrySliders[8].slide
            entry["lovedness"] = entrySliders[9].slide
            entry["pain"] = entrySliders[10].slide
            entry["socialness"] = entrySliders[11].slide
            entry["hopefulness"] = entrySliders[12].slide
            entry["activity"] = entrySliders[13].slide

            board["entries"].append(entry)
            SaveData()

            # changing the menu
            state = States.overview

            # updating the sliders
            for slider in entrySliders:
                slider.forceUpdate = True
                slider.slide = 0
    elif state == States.stats:
        # rendering the menu
        for button in statsButton:
            button.Render(screen, events)

        # rendering the stats
        pygame.draw.rect(screen, color.color, [10, 45, 1200-90+35, 750-90], border_radius=4)
        pygame.draw.rect(screen, color.darkColor, [10, 45, 1200-90+35, 750-90], width=4, border_radius=4)
        pygame.draw.line(screen, color.darkColor, (245, 45+2), (245, 45+750-90-4), width=4)
        pygame.draw.line(screen, color.darkColor, (245, 750//2), (1200-90+40, 750//2), width=4)
        
        # generating the points for the graph (maybe cash this stuff but idk)
        points = []
        colors = {
            "mood"        : (47 , 79 , 79 ),
            "stress"      : (127, 0  , 0  ),
            "anxiety"     : (0  , 100, 0  ),
            "depression"  : (0  , 0  , 128),
            "happiness"   : (255, 140, 0  ),
            "suicidalness": (222, 184, 135),
            #"fatigue"     : (0  , 255, 0  ),
            "sleepiness"  : (0  , 191, 255),
            "energy"      : (0  , 0  , 255),
            "lovedness"   : (255, 0  , 255),
            #"pain"        : (255, 255, 84 ),
            "socialness"  : (221, 160, 221),
            #"hopefulness" : (255, 20 , 147),
            "activity"    : (127, 255, 212)
        }

        # rendering the moods each color goes with
        y = 0
        for mood in colors:
            UI.DrawText(screen, 30, "pixel2.ttf", f"* {mood}", (15, 50 + y), colors[mood])
            y += 35
        
        # looping through all the last few days (max 10)
        maxPoints = 40
        for i, day in enumerate([key for key in saveData][-maxPoints:]):
            # generating the sum of the entries for the day
            average = {key: 0 for key in colors}
            for entry in saveData[day]["entries"]:
                for mood in colors:
                    average[mood] += entry[mood]
            
            # generating the average for the day
            length = len(saveData[day]["entries"])
            for mood in average:
                average[mood] = 1 - average[mood]/length
            
            # adding the point
            for mood in average:
                points.append([colors[mood], i, average[mood]])

        # rendering the graph
        i = 0
        numPoints = len(points)
        for col, x, y in points:
            pos = (x * 890 / maxPoints + 255, y * 640 + 55)
            pygame.draw.circle(screen, col, pos, 4)
            for i2 in range(i+1, numPoints):
                nc, nx, ny = points[i2]
                if nc != col: continue
                newPos = (nx * 890 / maxPoints + 255, ny * 640 + 55)
                pygame.draw.line(screen, col, pos, newPos, width=1)
                break
            i += 1

        # changing if the button to go back was pressed
        if statsButton[0].state == UI.Button.States.realeased:
            state = States.overview
            screenSize = (600, 950)
            screen = pygame.display.set_mode(screenSize)  # flags=pygame.RESIZABLE
            backgroundImage = backgroundImages[0]

    # rendering the fps counter
    #UI.DrawText(screen, 20, "pixel2.ttf", f"FPS {fps}", (screenSize[0] - 90, 10), (255, 0, 0))

    # updating the display
    pygame.display.update()

    # dealing with time change
    dif = max(desiredTime - (time.time() - frameStart), 0)
    time.sleep(dif)
    frameEnd = time.time()
    dt = min(frameEnd - frameStart, 1/15)

