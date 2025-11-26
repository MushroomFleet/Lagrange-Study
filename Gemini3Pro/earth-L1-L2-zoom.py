import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------
# 1. Physics Engine (Zoomed)
# ---------------------------------------------------------
def get_potential(x, y, mu):
    # Distances
    r1 = np.sqrt((x + mu)**2 + y**2) # Sun
    r2 = np.sqrt((x - (1 - mu))**2 + y**2) # Earth
    r2 = np.maximum(r2, 1e-6) # Protect Earth core
    return -((1 - mu) / r1) - (mu / r2) - 0.5 * (x**2 + y**2)

mu = 3.003e-6
Earth_X = 1 - mu

# ---------------------------------------------------------
# 2. High-Res Grid (Focused on Earth)
# ---------------------------------------------------------
# Zoom window: +/- 2.5 million km around Earth
zoom_radius = 0.016 
res = 2000

x = np.linspace(Earth_X - zoom_radius, Earth_X + zoom_radius, int(res*1.77)) # Aspect ratio width
y = np.linspace(-zoom_radius, zoom_radius, res)
X, Y = np.meshgrid(x, y)

Z = get_potential(X, Y, mu)

# ---------------------------------------------------------
# 3. Critical Energy Levels
# ---------------------------------------------------------
# We need the exact potential at L1 and L2 to draw the "Gate" contours
dist_L = (mu/3)**(1/3)
L1_loc = 1 - mu - dist_L
L2_loc = 1 - mu + dist_L

C_L1 = get_potential(L1_loc, 0, mu)
C_L2 = get_potential(L2_loc, 0, mu)

# ---------------------------------------------------------
# 4. Rendering (2K Style)
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 9), dpi=160)
ax.set_facecolor('#000005')

# Gradient Configuration
Z_max = C_L1 + 0.000005 
Z_min = C_L1 - 0.000025
levels = np.linspace(Z_min, Z_max, 150)

# Main Topography
cf = ax.contourf(X, Y, np.clip(Z, Z_min, Z_max), levels=levels, cmap='inferno')

# The "Walls" (Critical Contours)
# Cyan for L1 (Sun-side gate), Magenta for L2 (Outer gate)
ax.contour(X, Y, Z, levels=[C_L1], colors='cyan', linewidths=2, linestyles='solid', alpha=0.8)
ax.contour(X, Y, Z, levels=[C_L2], colors='magenta', linewidths=2, linestyles='solid', alpha=0.8)

# ---------------------------------------------------------
# 5. Operational Details (Orbits & Bodies)
# ---------------------------------------------------------

# Earth
ax.plot(Earth_X, 0, 'o', color='#22aaff', markersize=25, label='Earth', markeredgecolor='white', markeredgewidth=2)

# L1 & L2 Markers
ax.plot(L1_loc, 0, '+', color='cyan', markersize=15, markeredgewidth=3)
ax.plot(L2_loc, 0, '+', color='magenta', markersize=15, markeredgewidth=3)

# ORBITS
# JWST Halo (L2) - Stylized Lissajous vertical projection
theta = np.linspace(0, 2*np.pi, 200)
halo_r = 0.005 # Approx 800k km scale visually
ax.plot(L2_loc + 0.002*np.cos(theta), 0.005*np.sin(theta), color='white', linestyle='--', linewidth=1.5, alpha=0.8)
ax.text(L2_loc, 0.006, "JWST Halo Orbit", color='white', fontsize=10, ha='center', alpha=0.7)

# SOHO Halo (L1)
ax.plot(L1_loc + 0.0015*np.cos(theta), 0.003*np.sin(theta), color='white', linestyle='--', linewidth=1.5, alpha=0.8)
ax.text(L1_loc, -0.005, "SOHO Halo Orbit", color='white', fontsize=10, ha='center', alpha=0.7)

# ---------------------------------------------------------
# 6. Annotation & Scale
# ---------------------------------------------------------
ax.set_title("Earth's Hill Sphere: L1 & L2 Gateways", color='white', fontsize=20, pad=15)

# Formatting axes to Metric
def au_to_mkm(val, pos):
    return f'{(val - Earth_X)*149.6:.1f} M km'

ax.xaxis.set_major_formatter(FuncFormatter(au_to_mkm))
ax.set_xlabel("Distance from Earth (Million km)", color='gray')
ax.tick_params(colors='gray', labelcolor='gray')
ax.set_yticks([]) # Hide Y axis numbers for cleaner look, keep grid
ax.grid(True, color='white', alpha=0.05)

plt.tight_layout()
plt.savefig('Map2_Earth_Zoom_2K.png', dpi=160, facecolor='#000005')
plt.show()