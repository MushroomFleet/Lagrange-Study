import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------
planets = [
    {'name': 'Mercury', 'r': 0.39,  'mu': 1.66e-7, 'angle': 0},
    {'name': 'Venus',   'r': 0.72,  'mu': 2.45e-6, 'angle': 1.25}, 
    {'name': 'Earth',   'r': 1.00,  'mu': 3.00e-6, 'angle': 2.51},
    {'name': 'Mars',    'r': 1.52,  'mu': 3.23e-7, 'angle': 3.76},
    {'name': 'Jupiter', 'r': 5.20,  'mu': 9.54e-4, 'angle': 5.02}
]

# ---------------------------------------------------------
# 2. Calculation Engine (Log-Polar Normalized)
# ---------------------------------------------------------
res = 1800 
screen = np.linspace(-1.1, 1.1, res)
SX, SY = np.meshgrid(screen, screen)
R_scr = np.sqrt(SX**2 + SY**2)
Theta_scr = np.arctan2(SY, SX)

# Log Mapping
min_au, max_au = 0.25, 6.5
log_min, log_max = np.log(min_au), np.log(max_au)
# Mask center hole
R_scr = np.maximum(R_scr, 0.08)

# Map Screen Radius -> Physical Radius (AU)
R_phys = np.exp(log_min + (R_scr) * (log_max - log_min))

# Build Composite Potential
# Start with a very low background
Z_comp = np.zeros_like(SX) - 200 

for p in planets:
    # Derotate to local frame
    theta_local = Theta_scr - p['angle']
    
    # Normalize angle to -pi to pi
    theta_local = (theta_local + np.pi) % (2 * np.pi) - np.pi
    
    r_local = R_phys / p['r'] 
    
    x_c = r_local * np.cos(theta_local)
    y_c = r_local * np.sin(theta_local)
    
    # Physics (R3BP)
    r1 = np.sqrt((x_c + p['mu'])**2 + y_c**2)
    r2 = np.sqrt((x_c - (1-p['mu']))**2 + y_c**2)
    r1, r2 = np.maximum(r1, 1e-4), np.maximum(r2, 1e-4)
    pot = -((1 - p['mu']) / r1) - (p['mu'] / r2) - 0.5 * (x_c**2 + y_c**2)
    
    # Normalize Depth
    l1_E = -1.5 - (p['mu']/3)**(1/3)
    norm_pot = (pot - l1_E) / (p['mu']**(1/3))
    
    # --- VISUAL FIX: create an "Island Mask" ---
    # 1. Radial band (same as before)
    sigma_r = 0.15
    radial_weight = np.exp(-((np.log(R_phys) - np.log(p['r']))**2) / (2*sigma_r**2))
    
    # 2. Angular masking (The new part)
    # This hides the ring when it is far from the planet
    sigma_theta = 0.5 # Width of the visible arc in radians
    angular_weight = np.exp(-(theta_local**2) / (2*sigma_theta**2))
    
    total_weight = radial_weight * angular_weight
    
    # Apply mask
    # We blend the planet's potential into the background
    Z_comp = np.maximum(Z_comp, norm_pot * total_weight - (1-total_weight)*10)

# ---------------------------------------------------------
# 3. Rendering
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 12), dpi=180)
ax.set_facecolor('#050505')

# Contour Map
# We adjust levels to focus on the "Saddle" details near 0
levels = np.linspace(-4, 0.5, 90)
ax.contourf(SX, SY, Z_comp, levels=levels, cmap='gist_stern', extend='min')
ax.contour(SX, SY, Z_comp, levels=levels, colors='white', alpha=0.05, linewidths=0.5)

# ---------------------------------------------------------
# 4. Overlays
# ---------------------------------------------------------
for p in planets:
    r_s = (np.log(p['r']) - log_min) / (log_max - log_min)
    px = r_s * np.cos(p['angle'])
    py = r_s * np.sin(p['angle'])
    
    # Faint full orbit ring for context
    circle = mpatches.Circle((0,0), r_s, color='white', fill=False, alpha=0.05, linestyle=':')
    ax.add_artist(circle)
    
    # Planet Dot
    c = '#ffaa00' if p['name'] == 'Venus' else 'white'
    if p['name'] == 'Mars': c = '#ff5533'
    if p['name'] == 'Earth': c = '#00aaff'
    if p['name'] == 'Jupiter': c = '#dbaa77'
    
    ax.plot(px, py, 'o', color=c, markersize=10, markeredgecolor='black', zorder=5)
    ax.text(px*1.15, py*1.15, p['name'], color=c, fontsize=9, fontweight='bold', ha='center')
    
    # Jupiter Trojans
    if p['name'] == 'Jupiter':
        # Adjust angular mask for Trojans so they don't get cut off
        for offset, name in [(np.pi/3, 'L4'), (-np.pi/3, 'L5')]:
            lx = r_s * np.cos(p['angle'] + offset)
            ly = r_s * np.sin(p['angle'] + offset)
            
            cx = lx + np.random.normal(0, 0.02, 300)
            cy = ly + np.random.normal(0, 0.02, 300)
            ax.scatter(cx, cy, s=0.5, c='#aaaaaa', alpha=0.5)
            ax.text(lx*1.08, ly*1.08, name, color='gray', fontsize=7, ha='center')

# Sun
ax.plot(0, 0, 'o', color='#FFD700', markersize=25, zorder=10, markeredgecolor='#ffaa00', markeredgewidth=2)

ax.axis('off')
ax.set_aspect('equal')
ax.set_title("Solar System Gravity Archipelago\n(Log-Polar Projection - Normalized Local Wells)", color='white', fontsize=18, pad=20)

plt.tight_layout()
plt.savefig('Map3_Archipelago_Corrected_2K.png', dpi=180, facecolor='#050505')
plt.show()