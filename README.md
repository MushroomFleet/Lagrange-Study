# Lagrange Study: AI-Generated Physics Visualization

A comparative study exploring AI capabilities in scientific visualization through gravitational physics simulations. This project demonstrates how **Gemini 3 Pro Preview** can generate sophisticated Python code for visualizing Lagrange points across the Solar System, contrasted with **Nano Banana Pro's** image generation approach.

## 🎯 Project Overview

This research project tasked advanced AI models with creating topographical contour maps of the Solar System's Lagrange points—critical equilibrium positions in celestial mechanics where gravitational forces balance. The study compares:

- **Code Generation Approach**: Gemini 3 Pro Preview generating physics-simulation Python scripts
- **Image Generation Approach**: Nano Banana Pro creating visual representations from prompts

## 📊 Three Visualization Maps

### 1. **Earth-Sun Global System**
A 2K resolution topographic map showing the gravitational potential field of the Earth-Sun system, highlighting all five Lagrange points (L1-L5) using the Restricted Three-Body Problem physics model.

### 2. **Earth's Hill Sphere (L1/L2 Zoom)**
A tactical zoomed view focusing on Earth's L1 and L2 gateway points, featuring:
- JWST Halo Orbit visualization at L2
- SOHO Halo Orbit at L1
- High-contrast "inferno" colormap showing potential gradients

### 3. **Solar System Archipelago**
A log-polar projection displaying Mercury, Venus, Earth, Mars, and Jupiter as isolated "gravity islands," including Jupiter's Trojan asteroids at L4 and L5 points.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/MushroomFleet/Lagrange-Study.git
cd Lagrange-Study

# Install dependencies
pip install -r Gemini3Pro/requirements.txt
```

### Running the Visualizations

```bash
# Generate the Earth-Sun global map
python Gemini3Pro/earth-sun-system.py

# Generate the Earth L1/L2 zoom view
python Gemini3Pro/earth-L1-L2-zoom.py

# Generate the Solar System archipelago
python Gemini3Pro/solar-archipelago.py
```

Generated images will be saved as high-resolution PNG files in the current directory.

## 📁 Repository Structure

```
lagrange-map/
├── Gemini3Pro/           # AI-generated Python visualization scripts
│   ├── earth-sun-system.py
│   ├── earth-L1-L2-zoom.py
│   ├── solar-archipelago.py
│   ├── requirements.txt
│   └── images/           # Generated output examples
├── bananaPro/            # Nano Banana Pro image generation
│   ├── banana-pro-prompts.md   # Image generation prompts
│   └── banana-*.jpeg            # Generated images
└── README.md
```

## 🎨 AI Models Compared

### Gemini 3 Pro Preview
- **Task**: Generate complete Python physics simulation code
- **Output**: Executable scripts using NumPy and Matplotlib
- **Strengths**: Mathematical precision, customizable parameters, reproducible results
- **Approach**: Code-first scientific visualization

### Nano Banana Pro
- **Task**: Generate images from detailed physics-based prompts
- **Output**: High-fidelity visual representations
- **Strengths**: Artistic interpretation, rapid prototyping, aesthetic quality
- **Approach**: Prompt-driven image synthesis

## 🔬 Physics Background

The visualizations use the **Restricted Three-Body Problem (R3BP)** model to calculate effective potential fields. Lagrange points are positions where the gravitational pull of two large masses precisely equals the centripetal force required for a small object to move with them.

**The Five Lagrange Points:**
- **L1**: Between the two bodies (Sun-Earth gateway)
- **L2**: Beyond the smaller body (ideal for space telescopes like JWST)
- **L3**: Opposite side of the larger body
- **L4/L5**: Forming equilateral triangles with the two bodies (stable, home to Trojan asteroids)

## 📚 Citation

### Academic Citation

If you use this codebase in your research or project, please cite:

```bibtex
@software{lagrange_study,
  title = {Lagrange Study: AI-Generated Physics Visualization},
  author = {Drift Johnson},
  year = {2025},
  url = {https://github.com/MushroomFleet/Lagrange-Study},
  version = {1.0.0}
}
```

### Donate:


[![Ko-Fi](https://cdn.ko-fi.com/cdn/kofi3.png?v=3)](https://ko-fi.com/driftjohnson)

## 📝 License

This project is provided for educational and research purposes.

## 🙏 Acknowledgments

- Gemini 3 Pro Preview for physics simulation code generation
- Nano Banana Pro for visual interpretation and artistic rendering
- The celestial mechanics research community for R3BP models
