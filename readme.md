# It's another python text user interface.
It's my personal challenge write text user interface library for python. Which be suitable for my needs and requirements. Interest part that all development and testing done on Android phone terminal.

##### Oh what's a plan.
* Root UI element (common variables and functions) [UIElement]:
    - [x] Y, X coordinates.
	- [x] Height and width.
	- [x] Color.
* Color holder [ColorPair]:
    - [x] Background and foreground color.
	- [x] Automatic unique color ID generation on object create time.
* Screen container [TUI]:
    - [x] Default screen initialization. 
* ScrollPad:
    - [ ] Content scrolling.
	- [ ] Scroll bar.
* String (Main UI building block):
	- [ ] One line and multi line string support.
	- [ ] Calculate height and width of element from content.
	- [ ] Foreground and background color.
* Cursor:
    - [ ] Coordinates, relative to parent element.
	- [ ] Type (linear, point, ...).
	    - Linear - By default cursor is on firs element of line.
		- Point - Use coordinates to determine cursor location.
