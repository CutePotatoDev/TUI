import tui
import comp
import time
import datetime


def executor(elements, ui):
    elements[0].x = ui.width - 14
    i = 5
    j = 0
    animstr = ["   ", ".  ", ".. ", "..."]

    while True:
        if i == 5:
            elements[0].text = "[ %s ]" % datetime.datetime.now().strftime("%H:%M:%S")
            i = 0

        elements[1].text = elements[1].text[:8] + animstr[j]

        j += 1
        if j == 4:
            j = 0
         
        i += 1
        time.sleep(0.2)
    

def main():
    ui = tui.TUI(color=comp.ColorPair(comp.Color.BLACK, comp.Color.BLUE),
                 box=True)

    clocklabel = tui.Label("[ 00:00:00 ]", y=0, x=0)
    loadlabel = tui.Label("Loading ", y=1, x=3)
    
    ui.add(clocklabel)
    ui.add(loadlabel)

    elements = (clocklabel, loadlabel)

    ui.loop(executor, elements, ui)
    ui.run()
    

if __name__ == "__main__":
    main()
