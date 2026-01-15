
- In pygame the x, y coordinates (0, 0) start at the top left.

- Surface objects are objects that represent a rectangular 2D image.The window border, title bar, and buttons are not part of the display Surface object

- Pygame can draw 16,777,216 different colors (that is, 256 x 256 x 256 colors)

- To draw using transparent colors, you must create a Surface object with the convert_alpha() method. This surface is then blitted (copied) to the DISPLAYSRUF

```python
anotherSurface = DISPLAYSURF.convert_alpha()
```

- Represent Color : `pygame.Color(BLACK)`
- Represent Rectangular Area 
    - `pygame.Rect(top-left-x, top-left-y, width, height)`