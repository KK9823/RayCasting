This is a rendering project which uses ray casting to render a 3d scene.
Uses Pygame for rendering.

Controls:
- WASD - movement
- left and right arrow keys - move camera
- left shift - sprint

Run Instructions:
- Download dependencies using "pip install -r requirements.txt"
- Run command "python main.py"

Demo

https://github.com/user-attachments/assets/9c9240f4-0688-46b5-b3ac-589f0445ee83


What is Ray Casting?

Ray Casting is a graphics technique that shoots rays (you can see the visualization on the minimap shown by green lines) from a point (the camera position) to render a 3d interface. The interface is rendered using many slices of vertical rectangles. The main idea is, the longer a ray takes to travel until it hits a wall, the shorter the ray's rectangle is on the screen. This is because objects farther away will be seen smaller. The Ceiling and Floor are just visual tricks made by fading rectangles as they go into the distance (center of the screen). If you want to see a more low-level visualization of the rays/rectangles, go into config.py and reduce the number of rays and you will be able to see each individual slice of rectangle more clearly. (Right now, the ray count is 600).


Features
- Player Collision with walls
- Wall Distance Fading
- Wall Edge Highlights
- Minimap
- Floor and Ceiling
- 
