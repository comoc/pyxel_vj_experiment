import pyxel
import math
import random

class VJApp:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel VJ")
        
        self.effects = [
            self.draw_circles,
            self.draw_lines,
            self.draw_noise,
            self.draw_wave,
            self.draw_tunnel,
            self.draw_kaleidoscope,
            self.draw_beat_circles,
            self.draw_beat_bars,
            self.draw_beat_spiral,
            self.draw_beat_flash
        ]
        self.current_effect = 0
        self.t = 0
        self.color_offset = 0
        self.particles = [(random.random() * 160, random.random() * 120, random.random() * 6.28) 
                         for _ in range(50)]
        
        # BPM system
        self.bpm = 120  # Default BPM
        self.beat_time = 0  # Time of last beat
        self.beat_duration = 60 / self.bpm  # Duration of one beat in seconds
        self.auto_beat = True  # Auto beat generation
        self.beat_intensity = 0  # For beat-reactive effects
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        # Change effect with number keys (1-0)
        for i in range(10):
            if pyxel.btnp(pyxel.KEY_1 + i):
                self.current_effect = i
                
        # BPM control
        if pyxel.btn(pyxel.KEY_Z):
            self.bpm = max(60, self.bpm - 1)
            self.beat_duration = 60 / self.bpm
        if pyxel.btn(pyxel.KEY_X):
            self.bpm = min(240, self.bpm + 1)
            self.beat_duration = 60 / self.bpm
            
        # Update time and beat
        self.t += 1/30  # Assuming 30 FPS
        
        # Auto beat generation based on BPM
        if self.auto_beat and self.t - self.beat_time >= self.beat_duration:
            self.beat_time = self.t
            self.beat_intensity = 1.0
        
        # Manual beat override
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.beat_time = self.t
            self.beat_intensity = 1.0
            self.auto_beat = not self.auto_beat  # Toggle auto beat
            
        # Update beat intensity
        self.beat_intensity = max(0, self.beat_intensity - 0.1)
        
        # Cycle colors (sync with beat)
        if self.t - self.beat_time < self.beat_duration * 0.1:
            self.color_offset = (self.color_offset + 1) % 16
            
        # Update particles
        for i in range(len(self.particles)):
            x, y, angle = self.particles[i]
            speed = 1 + self.beat_intensity * 2
            x = (x + math.cos(angle) * speed) % 160
            y = (y + math.sin(angle) * speed) % 120
            if random.random() < 0.02:
                angle = random.random() * 6.28
            self.particles[i] = (x, y, angle)
    
    def draw(self):
        pyxel.cls(0)
        self.effects[self.current_effect]()
        
        # Draw BPM and beat indicators
        bpm_text = f"BPM:{int(self.bpm)}"
        mode_text = "AUTO" if self.auto_beat else "MANUAL"
        phase = (self.t - self.beat_time) / self.beat_duration
        bpm_color = 11 if phase < 0.1 else 7
        pyxel.text(4, 4, f"{bpm_text} {mode_text}", bpm_color)
    
    def draw_circles(self):
        beat_phase = (self.t - self.beat_time) / self.beat_duration
        for i in range(8):
            radius = 20 + math.sin(beat_phase * math.pi * 2 + i) * (10 + self.beat_intensity * 10)
            x = 80 + math.cos(beat_phase * math.pi * 2 + i) * 30
            y = 60 + math.sin(beat_phase * math.pi * 2 + i * 2) * 20
            col = (i + self.color_offset) % 16
            pyxel.circb(x, y, radius, col)
    
    def draw_lines(self):
        beat_phase = (self.t - self.beat_time) / self.beat_duration
        for i in range(16):
            x1 = math.sin(beat_phase * math.pi * 2 + i * 0.5) * 80 + 80
            y1 = math.cos(beat_phase * math.pi * 2 + i * 0.5) * 60 + 60
            x2 = math.sin(beat_phase * math.pi * 2 + i * 0.5 + math.pi) * 80 + 80
            y2 = math.cos(beat_phase * math.pi * 2 + i * 0.5 + math.pi) * 60 + 60
            col = (i + self.color_offset) % 16
            pyxel.line(x1, y1, x2, y2, col)
    
    def draw_noise(self):
        for x, y, _ in self.particles:
            col = (int(x + y + self.t * 8) + self.color_offset) % 16
            pyxel.pset(x, y, col)
    
    def draw_wave(self):
        beat_phase = (self.t - self.beat_time) / self.beat_duration
        for i in range(16):
            points = []
            for x in range(0, 160, 4):
                y = 60 + math.sin(x * 0.05 + beat_phase * math.pi * 2 + i * 0.5) * (20 + self.beat_intensity * 10)
                points.append((x, y))
            
            for j in range(len(points) - 1):
                x1, y1 = points[j]
                x2, y2 = points[j + 1]
                col = (i + self.color_offset) % 16
                pyxel.line(x1, y1, x2, y2, col)

    def draw_tunnel(self):
        beat_phase = (self.t - self.beat_time) / self.beat_duration
        center_x, center_y = 80, 60
        for r in range(80, 0, -4):
            angle = beat_phase * math.pi * 2 + r * 0.1
            offset_x = math.cos(angle) * (2 + self.beat_intensity * 4)
            offset_y = math.sin(angle) * (2 + self.beat_intensity * 4)
            col = (r // 4 + self.color_offset) % 16
            pyxel.circb(
                center_x + offset_x,
                center_y + offset_y,
                r,
                col
            )
    
    def draw_kaleidoscope(self):
        beat_phase = (self.t - self.beat_time) / self.beat_duration
        center_x, center_y = 80, 60
        segments = 8
        for i in range(segments):
            angle = i * (2 * math.pi / segments)
            length = 20 + math.sin(beat_phase * math.pi * 2) * (10 + self.beat_intensity * 20)
            x = center_x + math.cos(angle) * length
            y = center_y + math.sin(angle) * length
            
            next_i = (i + 1) % segments
            next_angle = next_i * (2 * math.pi / segments)
            next_x = center_x + math.cos(next_angle) * length
            next_y = center_y + math.sin(next_angle) * length
            
            col = (i + self.color_offset) % 16
            pyxel.line(x, y, next_x, next_y, col)
            pyxel.line(center_x, center_y, x, y, col)
    
    def draw_beat_circles(self):
        size = 40 + self.beat_intensity * 20
        for i in range(8):
            angle = i * math.pi / 4
            x = 80 + math.cos(angle) * size
            y = 60 + math.sin(angle) * size
            radius = 5 + self.beat_intensity * 15
            col = (i + self.color_offset) % 16
            pyxel.circ(x, y, radius, col)
    
    def draw_beat_bars(self):
        bar_count = 16
        bar_width = 160 // bar_count
        for i in range(bar_count):
            height = 20 + self.beat_intensity * 40
            if i % 2 == 0:
                height *= 0.5
            x = i * bar_width
            y = 60 - height/2
            col = (i + self.color_offset) % 16
            pyxel.rect(x, y, bar_width-1, height, col)
    
    def draw_beat_spiral(self):
        center_x, center_y = 80, 60
        points = []
        spins = 3
        for i in range(60):
            angle = i * 0.2 * (1 + self.beat_intensity)
            r = i * (0.5 + self.beat_intensity)
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * r
            points.append((x, y))
            
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            col = (i // 4 + self.color_offset) % 16
            pyxel.line(x1, y1, x2, y2, col)
    
    def draw_beat_flash(self):
        # Flash background
        flash_intensity = int(self.beat_intensity * 16)
        if flash_intensity > 0:
            pyxel.rect(0, 0, 160, 120, flash_intensity % 16)
        
        # Radiating lines
        center_x, center_y = 80, 60
        for i in range(12):
            angle = i * math.pi / 6
            length = 40 + self.beat_intensity * 40
            x = center_x + math.cos(angle) * length
            y = center_y + math.sin(angle) * length
            col = (i + self.color_offset) % 16
            pyxel.line(center_x, center_y, x, y, col)

VJApp()
