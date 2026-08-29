#!/usr/bin/env python3

import curses, sys, select, time, random, math, os



class ESTREGG:

    def __init__(self, stdscr):

        self.scr = stdscr

        curses.curs_set(0)

        self.scr.nodelay(True)



        # Colors

        curses.start_color()

        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_CYAN, -1)     # Wormhole / A Button

        curses.init_pair(2, curses.COLOR_RED, -1)      # Fire / B Button

        curses.init_pair(3, curses.COLOR_GREEN, -1)    # Thrusters / Y Button

        curses.init_pair(4, curses.COLOR_MAGENTA, -1)  # White Hole / X Button

        curses.init_pair(5, curses.COLOR_WHITE, -1)    # Rocket / D-Pad

        curses.init_pair(6, curses.COLOR_YELLOW, -1)   # Stars

        curses.init_pair(7, curses.COLOR_CYAN, -1)     # Planets



        # ESTREGG - World State & Dynamic Galaxies

        self.galaxy_num = 1

        self.world_x, self.world_y = 30.0, 15.0

        self.cam_x, self.cam_y = 0.0, 0.0



        self.direction = 'UP'

        self.autopilot = False

        self.zoom = 1.0

        self.settings_open = False

        self.info_open = False

        self.manual_open = False

        self.star_info_open = False

        self.focused_star_details = None



        # Settings Options

        self.show_stars = True

        self.speed_multiplier = 1.0



        self.last_input_source = "Keyboard"

        self.last_pressed_key = "None"

        self.gamepad_mac = "N/A"

        self.gamepad = self._find_gamepad()



        # Planet Landing State

        self.is_landed = False

        self.current_landed_planet = None

        self.launch_charge = 0

        self.cooldown_landing = 0



        # Input Highlights

        self.dpad_state = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

        self.action_state = {'A': False, 'B': False, 'X': False, 'Y': False}



        # Stars & Physics Arrays

        self.stars = []

        self._generate_galaxy_content()



    def _generate_galaxy_content(self):

        planet_types = ['ring', 'gas', 'rock']

        prefix = f"ESTREGG-G{self.galaxy_num}-"

        self.planets = []

        for i in range(10):

            angle = random.uniform(0, 2 * math.pi)

            dist = random.uniform(40, 280)

            self.planets.append({

                'x': math.cos(angle) * dist,

                'y': math.sin(angle) * dist,

                'name': f"{prefix}Planet-{i+1}",

                'flagged': False,

                'type': random.choice(planet_types)

            })



        self.wormholes = [

            {'x': 180, 'y': 180, 'name': f"ESTREGG Hyper-Portal Alpha-{self.galaxy_num}"},

            {'x': -180, 'y': -180, 'name': f"ESTREGG Hyper-Portal Beta-{self.galaxy_num}"}

        ]



        self.black_hole = {'x': 0, 'y': -140, 'name': 'Sagittarius A*'}

        self.white_hole = {'x': -180, 'y': 100, 'name': 'Polaris Emitter'}

        self.stars = []



    def _find_gamepad(self):

        try:

            from evdev import InputDevice, list_devices

            for path in list_devices():

                dev = InputDevice(path)

                if any(k in dev.name.lower() for k in ["controller", "gamepad", "gengame", "x7", "t-7", "joystick"]):

                    self.gamepad_mac = dev.uniq if dev.uniq else "N/A (USB or Virtual)"

                    return dev

        except ImportError:

            pass

        self.gamepad_mac = "N/A"

        return None



    def _safe_addstr(self, y, x, text, attr=curses.A_NORMAL):

        h, w = self.scr.getmaxyx()

        if 0 <= y < h:

            if x < 0:

                text = text[-x:]

                x = 0

            if x + len(text) >= w:

                text = text[:max(0, w - x - 1)]

            if text and x < w - 1:

                try:

                    self.scr.addstr(y, x, text, attr)

                except curses.error:

                    pass



    def _init_stars(self, h, w):

        if not self.stars:

            star_classes = ['Class O (Blue)', 'Class B (Blue-White)', 'Class A (White)', 'Class F (Yellow-White)', 'Class G (Solar)', 'Class M (Red Dwarf)']

            for _ in range(4000):

                self.stars.append({

                    'x': random.randint(-1500, 1500),

                    'y': random.randint(-1500, 1500),

                    'char': random.choice(['.', '.', '*', '+', '°', '·', '✦', '✧', '★', '⚡']),

                    'class': random.choice(star_classes),

                    'radius': round(random.uniform(0.5, 12.5), 2),

                    'mass': round(random.uniform(0.1, 25.0), 2)

                })



    def trigger_wormhole_animation(self):

        h, w = self.scr.getmaxyx()

        center_x, center_y = w // 2, h // 2



        for step in range(35):

            self.scr.erase()

            for _ in range(120):

                sx = random.randint(0, w - 2)

                sy = random.randint(0, h - 1)

                length = random.randint(2, max(3, step // 3))

                trail = "=" if abs(sx - center_x) > abs(sy - center_y) else "|"

                for l in range(length):

                    self._safe_addstr(sy, min(w - 2, sx + l), trail, curses.color_pair(1) | curses.A_BOLD)



            self._safe_addstr(center_y - 1, center_x - 2, ">>>>====>>", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(center_y,     center_x - 4, "===>> ENTERING ESTREGG WORMHOLE >>==", curses.color_pair(1) | curses.A_BOLD)

            self._safe_addstr(center_y + 1, center_x - 2, ">>>>====>>", curses.color_pair(5) | curses.A_BOLD)

            self.scr.refresh()

            time.sleep(0.04)



        self.galaxy_num += 1

        self._generate_galaxy_content()

        self.world_x, self.world_y = 0.0, 0.0

        self.cam_x, self.cam_y = 0.0, 0.0



        for step in range(25):

            self.scr.erase()

            radius = step * 2

            for angle in range(0, 360, 15):

                rad = math.radians(angle)

                ex = int(center_x + math.cos(rad) * radius)

                ey = int(center_y + math.sin(rad) * (radius / 2))

                self._safe_addstr(ey, ex, "@", curses.color_pair(4) | curses.A_BOLD)



            self._safe_addstr(center_y, center_x - 14, f"ESTREGG: ARRIVED IN GALAXY #{self.galaxy_num}", curses.color_pair(3) | curses.A_BOLD)

            self.scr.refresh()

            time.sleep(0.03)



    def _get_target_planet(self):

        unflagged = [p for p in self.planets if not p['flagged']]

        if not unflagged:

            return None

        return min(unflagged, key=lambda p: math.hypot(p['x'] - self.world_x, p['y'] - self.world_y))



    def _apply_space_physics(self):

        bh_dist = math.hypot(self.black_hole['x'] - self.world_x, self.black_hole['y'] - self.world_y)

        if bh_dist < 30:

            angle = math.atan2(self.black_hole['y'] - self.world_y, self.black_hole['x'] - self.world_x)

            if bh_dist > 6.0:

                self.world_x += math.cos(angle) * 0.9

                self.world_y += math.sin(angle) * 0.9

            else:

                self.world_x -= math.cos(angle) * 2.5

                self.world_y -= math.sin(angle) * 2.5



        wh_dist = math.hypot(self.white_hole['x'] - self.world_x, self.white_hole['y'] - self.world_y)

        if wh_dist < 35:

            angle = math.atan2(self.world_y - self.white_hole['y'], self.world_x - self.white_hole['x'])

            self.world_x += math.cos(angle) * 1.8

            self.world_y += math.sin(angle) * 1.8



    def _draw_planet(self, p, h, w):

        px = int((p['x'] - self.cam_x) * self.zoom + (w // 2) * (1 - self.zoom))

        py = int((p['y'] - self.cam_y) * self.zoom + (h // 2) * (1 - self.zoom))



        if p['type'] == 'ring':

            art = ["   .---.   ", "  /     \\  ", "==|  O  |==", "  \\     /  ", "   '---'   "]

        elif p['type'] == 'gas':

            art = ["  .----.  ", " / ~~~  \\ ", "|  ===   |", " \\ ~~~  / ", "  '----'  "]

        else:

            art = ["  .---.  ", " / o   \\ ", "|   O   |", " \\   o / ", "  '---'  "]



        for idx, line in enumerate(art):

            ly = py + idx - 2

            lx = px - len(line) // 2

            self._safe_addstr(ly, lx, line, curses.color_pair(7) | curses.A_BOLD)



        if p['flagged']:

            self._safe_addstr(py - 3, px + 2, "[P]", curses.color_pair(3) | curses.A_BOLD)



    def focus_nearest_star_info(self):

        if not self.stars: return

        nearest = min(self.stars, key=lambda s: math.hypot(s['x'] - self.world_x, s['y'] - self.world_y))

        self.focused_star_details = nearest

        self.star_info_open = not self.star_info_open



    def draw(self):

        self.scr.erase()

        h, w = self.scr.getmaxyx()

        self._init_stars(h, w)



        margin_x = w // 4

        margin_y = h // 4

        screen_x = self.world_x - self.cam_x

        screen_y = self.world_y - self.cam_y



        if screen_x < margin_x: self.cam_x -= (margin_x - screen_x)

        elif screen_x > w - margin_x: self.cam_x += (screen_x - (w - margin_x))

        if screen_y < margin_y: self.cam_y -= (margin_y - screen_y)

        elif screen_y > h - margin_y: self.cam_y += (screen_y - (h - margin_y))



        if self.show_stars:

            for star in self.stars:

                sx = int((star['x'] - self.cam_x) * self.zoom + (w // 2) * (1 - self.zoom))

                sy = int((star['y'] - self.cam_y) * self.zoom + (h // 2) * (1 - self.zoom))

                if 0 <= sy < h - 1 and 0 <= sx < w - 1:

                    self._safe_addstr(sy, sx, star['char'], curses.color_pair(6) | curses.A_DIM)



        for wh in self.wormholes:

            wx = int((wh['x'] - self.cam_x) * self.zoom + (w // 2) * (1 - self.zoom))

            wy = int((wh['y'] - self.cam_y) * self.zoom + (h // 2) * (1 - self.zoom))

            self._safe_addstr(wy, wx - 6, "( O WORMHOLE O )", curses.color_pair(1) | curses.A_BOLD)



        bhx = int((self.black_hole['x'] - self.cam_x) * self.zoom + (w // 2) * (1 - self.zoom))

        bhy = int((self.black_hole['y'] - self.cam_y) * self.zoom + (h // 2) * (1 - self.zoom))

        self._safe_addstr(bhy, bhx - 6, "(( BLACK HOLE ))", curses.A_REVERSE | curses.A_BOLD)



        whx = int((self.white_hole['x'] - self.cam_x) * self.zoom + (w // 2) * (1 - self.zoom))

        why = int((self.white_hole['y'] - self.cam_y) * self.zoom + (h // 2) * (1 - self.zoom))

        self._safe_addstr(why, whx - 6, "(( WHITE HOLE ))", curses.color_pair(4) | curses.A_BOLD)



        for p in self.planets:

            self._draw_planet(p, h, w)



        self._safe_addstr(1, 2, f"--- ESTREGG GALAXY SECTOR #{self.galaxy_num} ---", curses.color_pair(5))

        zoom_txt = f"{int(self.zoom * 100)}%"

        flagged_cnt = sum(1 for p in self.planets if p['flagged'])

        self._safe_addstr(2, 2, f"[AUTO: {'ON' if self.autopilot else 'OFF'}] [ZOOM: {zoom_txt}] [FLAGS: {flagged_cnt}/10]", curses.color_pair(1) if self.autopilot else curses.color_pair(5))

        self._safe_addstr(3, 2, f"[TELEMETRY] POS: ({self.world_x:.1f}, {self.world_y:.1f}) | DIR: {self.direction} | LAST IN: {self.last_input_source}", curses.color_pair(6))



        sy = int((self.world_y - self.cam_y) * self.zoom + (h // 2) * (1 - self.zoom))

        sx = int((self.world_x - self.cam_x) * self.zoom + (w // 2) * (1 - self.zoom))

        flame = random.choice(["W", "V", "M", "Y", "v", "^"]) if not self.is_landed else ""



        if self.direction == 'UP':

            self._safe_addstr(sy-1, sx-1, " /\\ ", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy,   sx-1, "|==|", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy+1, sx-1, "/\"\"\\", curses.color_pair(5) | curses.A_BOLD)

            if flame: self._safe_addstr(sy+2, sx-1, f" {flame}{flame} ", curses.color_pair(2) | curses.A_BOLD)



        elif self.direction == 'DOWN':

            self._safe_addstr(sy-1, sx-1, "\\\"\"/", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy,   sx-1, "|==|", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy+1, sx-1, " \\/ ", curses.color_pair(5) | curses.A_BOLD)

            if flame: self._safe_addstr(sy-2, sx-1, f" {flame}{flame} ", curses.color_pair(2) | curses.A_BOLD)



        elif self.direction == 'LEFT':

            self._safe_addstr(sy-1, sx-1, " /\\ ", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy,   sx-2, "<|==|", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy+1, sx-1, " \\/ ", curses.color_pair(5) | curses.A_BOLD)

            if flame: self._safe_addstr(sy, sx+3, f"{flame}", curses.color_pair(2) | curses.A_BOLD)



        elif self.direction == 'RIGHT':

            self._safe_addstr(sy-1, sx-1, " /\\ ", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy,   sx-1, "|==|>", curses.color_pair(5) | curses.A_BOLD)

            self._safe_addstr(sy+1, sx-1, " \\/ ", curses.color_pair(5) | curses.A_BOLD)

            if flame: self._safe_addstr(sy, sx-2, f"{flame}", curses.color_pair(2) | curses.A_BOLD)



        if self.cooldown_landing > 0:

            self.cooldown_landing -= 1



        if not self.is_landed and self.cooldown_landing == 0:

            for p in self.planets:

                if abs(p['x'] - self.world_x) <= 3 and abs(p['y'] - self.world_y) <= 2:

                    p['flagged'] = True

                    self.autopilot = False

                    self.zoom = 1.0

                    self.is_landed = True

                    self.current_landed_planet = p



        if self.is_landed and self.current_landed_planet:

            self.world_x = self.current_landed_planet['x']

            self.world_y = self.current_landed_planet['y']



        by = h - 5

        d_color = lambda k: curses.color_pair(5) | curses.A_BOLD if self.dpad_state[k] else curses.A_DIM

        self._safe_addstr(by,   3, " [^] ", d_color('UP'))

        self._safe_addstr(by+1, 1, "[<]", d_color('LEFT'))

        self._safe_addstr(by+1, 7, "[>]", d_color('RIGHT'))

        self._safe_addstr(by+2, 3, " [v] ", d_color('DOWN'))



        rx = max(15, w - 16)

        x_attr = (curses.color_pair(4) | curses.A_BOLD) if self.action_state['X'] else curses.A_DIM

        b_attr = (curses.color_pair(2) | curses.A_BOLD) if self.action_state['B'] else curses.A_DIM



        self._safe_addstr(by, rx+3, "(Y)", curses.color_pair(3) | (curses.A_BOLD if self.action_state['Y'] else curses.A_DIM))

        self._safe_addstr(by+1, rx, "(X)", x_attr)

        self._safe_addstr(by+1, rx+6, "(B)", b_attr)

        self._safe_addstr(by+2, rx+3, "(A)", curses.color_pair(1) | (curses.A_BOLD if self.action_state['A'] else curses.A_DIM))



        if self.info_open:

            mw, mh = 56, 14

            mx, my = (w - mw) // 2, (h - mh) // 2

            for y in range(mh): self._safe_addstr(my + y, mx, " " * mw, curses.A_REVERSE)

            self._safe_addstr(my + 1, mx + 2, f"=== ESTREGG PLANETS (GALAXY #{self.galaxy_num}) ===", curses.A_REVERSE | curses.A_BOLD)



            flagged_cnt = sum(1 for p in self.planets if p['flagged'])

            self._safe_addstr(my + 3, mx + 2, f"Progress: {flagged_cnt} / 10 Planets Flagged", curses.A_REVERSE | curses.A_BOLD)



            for idx, p in enumerate(self.planets):

                if idx < 8:

                    status = "[FLAGGED]" if p['flagged'] else "[UNFLAGGED]"

                    self._safe_addstr(my + 4 + idx, mx + 2, f"{p['name']} : {status}", curses.A_REVERSE)



            if flagged_cnt == 10:

                self._safe_addstr(my + 12, mx + 2, "ALL FLAGS COLLECTED! PRESS 'A' FOR WORMHOLE!", curses.A_REVERSE | curses.COLOR_CYAN | curses.A_BOLD)



        if self.settings_open:

            mw, mh = 50, 10

            mx, my = (w - mw) // 2, (h - mh) // 2

            for y in range(mh): self._safe_addstr(my + y, mx, " " * mw, curses.A_REVERSE)

            self._safe_addstr(my + 1, mx + 2, "=== ESTREGG SETTINGS (PRESS '3' TO CLOSE) ===", curses.A_REVERSE | curses.A_BOLD)

            self._safe_addstr(my + 3, mx + 2, f"[1] Toggle Starfield Rendering : {'ON' if self.show_stars else 'OFF'}", curses.A_REVERSE)

            self._safe_addstr(my + 4, mx + 2, f"[2] Thrust Speed Multiplier   : {self.speed_multiplier:.1f}x", curses.A_REVERSE)

            self._safe_addstr(my + 6, mx + 2, f"Connected Controller         : {self.gamepad.name if self.gamepad else 'None'}", curses.A_REVERSE)

            self._safe_addstr(my + 7, mx + 2, f"Controller MAC               : {self.gamepad_mac}", curses.A_REVERSE)



        if self.star_info_open and self.focused_star_details:

            mw, mh = 48, 7

            mx, my = (w - mw) // 2, (h - mh) // 2

            s = self.focused_star_details

            for y in range(mh): self._safe_addstr(my + y, mx, " " * mw, curses.A_REVERSE)

            self._safe_addstr(my + 1, mx + 2, "=== ESTREGG STAR DETAILS (R3) ===", curses.A_REVERSE | curses.A_BOLD)

            self._safe_addstr(my + 3, mx + 2, f"Spectral Class: {s['class']}", curses.A_REVERSE)

            self._safe_addstr(my + 4, mx + 2, f"Solar Radius  : {s['radius']} R_sun", curses.A_REVERSE)

            self._safe_addstr(my + 5, mx + 2, f"Solar Mass    : {s['mass']} M_sun", curses.A_REVERSE)



        self.scr.refresh()



    def update_autopilot(self):

        if self.is_landed or not self.autopilot:

            self.zoom = 1.0

            return



        target = self._get_target_planet()

        if not target:

            self.autopilot = False

            self.zoom = 1.0

            return



        tx, ty = target['x'], target['y']

        dist = math.hypot(tx - self.world_x, ty - self.world_y)



        if dist > 40: self.zoom = max(0.4, self.zoom - 0.02)

        elif dist < 20: self.zoom = min(1.0, self.zoom + 0.04)



        speed = 1.2 * self.speed_multiplier

        if abs(self.world_x - tx) > 0.5:

            if self.world_x < tx: self.world_x += speed; self.direction = 'RIGHT'

            else: self.world_x -= speed; self.direction = 'LEFT'



        if abs(self.world_y - ty) > 0.5:

            if self.world_y < ty: self.world_y += speed; self.direction = 'DOWN'

            else: self.world_y -= speed; self.direction = 'UP'



    def process_movement(self, dir_name, step=1.0):

        step *= self.speed_multiplier

        self.direction = dir_name

        self.dpad_state[dir_name] = True



        if self.is_landed:

            self.launch_charge += 1

            if self.launch_charge >= 2:

                self.is_landed = False

                self.current_landed_planet = None

                self.launch_charge = 0

                self.cooldown_landing = 15

                self.world_y -= 6.0

            return



        if dir_name == 'UP': self.world_y -= step

        elif dir_name == 'DOWN': self.world_y += step

        elif dir_name == 'LEFT': self.world_x -= step

        elif dir_name == 'RIGHT': self.world_x += step



    def handle_input(self):

        for k in self.dpad_state: self.dpad_state[k] = False

        for k in self.action_state: self.action_state[k] = False



        key = self.scr.getch()



        if key != -1:

            self.last_input_source = "Keyboard"

            self.last_pressed_key = f"Keycode {key} ({chr(key) if 32 <= key <= 126 else 'Special'})"



        # Ctrl + B (ASCII Keycode 2) or Tab (9) exits cleanly

        if key in [2, 9]:

            return False



        if key == curses.KEY_UP: self.process_movement('UP')

        elif key == curses.KEY_DOWN: self.process_movement('DOWN')

        elif key == curses.KEY_LEFT: self.process_movement('LEFT')

        elif key == curses.KEY_RIGHT: self.process_movement('RIGHT')



        if key in [ord('a'), ord('A')]: 

            self.action_state['A'] = True

            if sum(1 for p in self.planets if p['flagged']) == 10:

                self.trigger_wormhole_animation()

            else:

                self.autopilot = not self.autopilot



        elif key in [ord('i'), ord('I')]: 

            self.info_open = not self.info_open



        elif key in [ord('b'), ord('B')]: 

            self.process_movement('RIGHT', step=0.4)

            self.action_state['B'] = True



        elif key in [ord('x'), ord('X')]: 

            self.process_movement('LEFT', step=0.4)

            self.action_state['X'] = True



        elif key in [ord('y'), ord('Y')]: 

            self.process_movement('UP', step=0.4)

            self.action_state['Y'] = True



        elif key in [ord('r'), ord('R')]: 

            self.focus_nearest_star_info()



        elif key == ord('3'): 

            self.settings_open = not self.settings_open



        elif self.settings_open:

            if key == ord('1'):

                self.show_stars = not self.show_stars

            elif key == ord('2'):

                self.speed_multiplier = 2.0 if self.speed_multiplier == 1.0 else (3.0 if self.speed_multiplier == 2.0 else 1.0)



        if self.gamepad:

            from evdev import ecodes

            r, w_fds, x = select.select([self.gamepad.fd], [], [], 0.001)

            if r:

                for event in self.gamepad.read():

                    if event.type == ecodes.EV_KEY and event.value == 1:

                        self.last_input_source = f"Gamepad ({self.gamepad.name})"

                        self.last_pressed_key = f"Btn Code {event.code}"



                        if event.code in [304, 305]:

                            self.action_state['A'] = True

                            if sum(1 for p in self.planets if p['flagged']) == 10:

                                self.trigger_wormhole_animation()

                            else:

                                self.autopilot = not self.autopilot



                        elif event.code in [314, 315]:

                            self.settings_open = not self.settings_open



                        elif event.code == 317:

                            self.info_open = not self.info_open



                        elif event.code == 306:

                            self.process_movement('RIGHT', step=0.4)

                            self.action_state['B'] = True

                        elif event.code == 307:

                            self.process_movement('LEFT', step=0.4)

                            self.action_state['X'] = True

                        elif event.code == 308:

                            self.process_movement('UP', step=0.4)

                            self.action_state['Y'] = True

                        elif event.code == 318:

                            self.focus_nearest_star_info()



                    elif event.type == ecodes.EV_ABS:

                        if event.code in [0, 2]:

                            if event.value < 10000: self.process_movement('LEFT')

                            elif event.value > 55000: self.process_movement('RIGHT')

                        if event.code in [1, 5]:

                            if event.value < 10000: self.process_movement('UP')

                            elif event.value > 55000: self.process_movement('DOWN')

        return True



    def run(self):

        while True:

            self._apply_space_physics()

            self.update_autopilot()

            self.draw()

            if not self.handle_input():

                break

            time.sleep(0.03)



def main(stdscr):

    app = ESTREGG(stdscr)

    app.run()



if __name__ == "__main__":

    curses.wrapper(main)

    os.system('clear')
