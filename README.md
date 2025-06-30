# Black Hole Simulator

This project is a sophisticated simulation of a black hole system, developed using Python and Pygame. It allows users to explore gravitational dynamics by simulating stars orbiting and being captured by a black hole, complete with trajectory visualizations and interactive controls. The simulator incorporates realistic physics, including optional relativistic effects, star interactions, and collision mechanics.

## Features

- **Orbiting and Captured Stars**: Simulate stars in stable orbits or dynamically captured by the black hole.
- **Trajectory Visualizations**: Display star paths with adjustable trail lengths for clear orbital tracking.
- **Interactive UI**: Control simulation parameters like gravitational strength, speed, and star count via an in-game interface.
- **Physics Options**: Toggle relativistic effects (e.g., orbital precession), star collisions, and gravitational interactions.
- **3D Isometric View**: Switch to an isometric perspective for enhanced visualization.

## Installation

To run the simulator, ensure you have Python and Pygame installed. Follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/WIESZJAK/black-hole-simulator.git
   ```
2. Navigate to the project directory:
   ```
   cd black-hole-simulator
   ```
3. Install the required dependency:
   ```
   pip install pygame
   ```
4. Launch the simulator:
   ```
   python GOTOWE.py
   ```

## Usage

1. Start the simulator from the main menu, where you can specify the number of orbiting and captured stars.
2. After the simulation loads, press **"I"** to display the user interface.
3. Press **"E"** to access sliders for editing simulation parameters (e.g., gravitational constant, trail length).
4. Press **"F"** to view detailed statistics about the simulation and selected stars.

## Performance Considerations

- **High Star Counts**: The simulator supports up to 500 orbiting and 500 captured stars (total of 1000 stars). However, performance may degrade with large numbers due to computational demands.
- **Optimization Tips**: To handle 1000 stars, reduce the trail length and simulation speed via the sliders (accessible with "E"). For a smoother experience with full feature exploration, use 50 orbiting and 50 captured stars.
- **Warning**: Excessive star counts without adjustments may slow down the simulation significantly.

## Controls

- **I**: Toggle UI visibility.
- **E**: Open sliders for parameter editing.
- **F**: Display detailed simulation statistics.
- **Additional Keys**: Check the in-game UI for more controls (e.g., "P" to pause, "R" to reset).

## Demo

See the simulator in action below:

![Simulator Demo](demo.gif)

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License. You are free to:

- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material.

Under these terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial**: You may not use the material for commercial purposes.

See the [LICENSE](LICENSE) file for full details.

## Contact & Contributions

For questions, suggestions, or contributions, feel free to open an issue or submit a pull request on the GitHub repository. This project is part of my portfolio as a mid-level AI/ML developer, and I welcome collaboration to enhance its features!
