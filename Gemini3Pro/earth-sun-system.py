import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ---------------------------------------------------------
# 1. Physics Engine (High Precision)
# ---------------------------------------------------------
def calculate_effective_potential(x, y, mu):
    # Primary (Sun) at (-mu, 0), Secondary (Earth) at (1-mu, 0)
    x1 = -mu
    x2 = 1 - mu
    
    r1 = np.sqrt((x - x1)**2 + y**2)
    r2 = np.sqrt((x - x2)**2 + y**2)
    
    # Avoid singularities
    r1 = np.maximum(r1, 1e-6)
    r2 = np.maximum(r2, 1e-6)
    
    # Effective Potential (Gravity + Centrifugal)
    potential = -((1 - mu) / r1) - (mu / r2) - 0.5 * (x**2 + y**2)
    return potential

# Parameters
mu_earth = 3.003e-6 
# Visual scaling: We use a slightly exaggerated mu for the contour visual 
# if needed, but for 2K detail we can stick closer to physics or 
# use log-scales in coloring. Here we use standard physics but distinct levels.

# ---------------------------------------------------------
# 2. High-Res Grid (2K Target)
# ---------------------------------------------------------
# 2560x1440 aspect ratio is 16:9. 
# We define the physical bounds to fit this ratio.
x_range = 3.2  # -1.6 to 1.6
y_range = 1.8  # -0.9 to 0.9

x = np.linspace(-1.5, 1.7, 2560)
y = np.linspace(-0.9, 0.9, 1440)
X, Y = np.meshgrid(x, y)

Z = calculate_effective_potential(X, Y, mu_earth)

# ---------------------------------------------------------
# 3. Rendering (2K Style)
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 9), dpi=160) # 16*160 = 2560px width
ax.set_facecolor('#050508') # Deep space dark

# Clipping for visual clarity (The Sun's well is infinitely deep)
# We want to focus on the "Lagrange Surface" between -3.5 and -1.5
Z_clipped = np.clip(Z, -3.05, -1.499)

# Contours
# We use 'magma' for high contrast energy levels
levels = np.linspace(np.min(Z_clipped), np.max(Z_clipped), 120)
contour_plot = ax.contourf(X, Y, Z_clipped, levels=levels, cmap='magma', extend='both')

# Fine topographical lines
ax.contour(X, Y, Z_clipped, levels=levels[::2], colors='white', alpha=0.08, linewidths=0.5)

# ---------------------------------------------------------
# 4. Markers & Geometry
# ---------------------------------------------------------

# Bodies
ax.plot(-mu_earth, 0, 'o', color='#FFD700', markersize=18, label='Sun', markeredgecolor='#ffaa00', markeredgewidth=2)
ax.plot(1-mu_earth, 0, 'o', color='#00FFFF', markersize=8, label='Earth', markeredgecolor='white', markeredgewidth=1)

# Lagrange Points Calculation
l1_x = 1 - (mu_earth/3)**(1/3)
l2_x = 1 + (mu_earth/3)**(1/3)
l3_x = -1 - (5*mu_earth)/12
l4_x = 0.5 - mu_earth
l4_y = np.sqrt(3)/2

points = [
    (l1_x, 0, 'L1'),
    (l2_x, 0, 'L2'),
    (l3_x, 0, 'L3'),
    (l4_x, l4_y, 'L4'),
    (l4_x, -l4_y, 'L5')
]

for px, py, txt in points:
    ax.plot(px, py, 'x', color='white', markersize=12, markeredgewidth=2.5, alpha=0.9)
    ax.text(px, py+0.06, txt, color='white', fontsize=14, ha='center', fontweight='bold')

# ---------------------------------------------------------
# 5. Final Polish
# ---------------------------------------------------------
ax.set_title("Earth-Sun System: Gravitational Topography (Effective Potential)", 
             color='white', fontsize=20, pad=20, weight='light')
ax.axis('off') # Clean look for the map

# Add scale reference
ax.plot([0, 1], [-0.85, -0.85], color='white', linewidth=1)
ax.text(0.5, -0.88, '1 AU (150 million km)', color='white', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('Map1_EarthSun_Global_2K.png', dpi=160, facecolor='#050508')
plt.show()