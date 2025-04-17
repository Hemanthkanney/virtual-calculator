# Hand Gesture-Controlled Math Solver with AI Visualization

🚀 **A hybrid system that solves math equations via hand gestures and generates AI-powered visual explanations**

---

## 📌 Overview
This project combines:
- **👋 Hand gesture recognition** (MediaPipe) for equation input
- **🧮 Symbolic math solving** (SymPy) for computations
- **🎨 Stable Diffusion + GAN refinement** for visual explanations

**Use Case:** Interactive STEM education, assistive tech, and futuristic UI experiments.

---

## ✨ Key Features
| Component | Technology | Function |
|-----------|------------|----------|
| **Gesture Input** | MediaPipe | Detects digits/operators via hand poses |
| **Math Engine** | SymPy | Solves equations (algebra/calculus) |
| **AI Visualization** | Stable Diffusion + GAN | Generates & refines solution diagrams |
| **UI** | OpenCV + Tkinter | Real-time camera feed + display |

---

## ⚙️ Installation
```bash
pip install -r requirements.txt  # Installs:
# mediapipe, sympy, opencv-python, torch, diffusers
```

🚀 Usage
Run the main script:

python
```python gesture_math_solver.py```
Gesture Commands:

Left hand: Numbers (0-9) and basic operations (+, -, ×, ÷)

Right hand: Advanced symbols (x, y, ∫, d/dx, Σ)

✋ Open palm: Show solution

🛠️ System Architecture

graph LR
A[Camera Input] --> B(MediaPipe Gesture Detection)
B --> C{Is Equation Complete?}
C -->|Yes| D[SymPy Solving]
D --> E[Stable Diffusion Visualization]
E --> F[GAN Refinement]
F --> G[Display Solution]

