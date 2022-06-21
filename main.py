import os, glob, shutil
from uiautomator import device as d
from uiautomator import Adb
import inquirer
from inquirer.themes import GreenPassion


def takeScreenshot():
    d.wait.update()
    d(resourceId="com.whatsapp:id/date_divider_header").wait.gone(timeout=1000)
    d.screenshot(f'IMG-{takeScreenshot.counter}.png')
    takeScreenshot.counter += 1


takeScreenshot.counter = 0


def scroll(forward):
    advance = d(scrollable=True).exists
    while advance:
        takeScreenshot()
        if(forward):
            advance = d(scrollable=True).scroll.vert.forward()
        else:
            advance = d(scrollable=True).scroll.vert.backward()
    takeScreenshot()


def scrollForward():
    scroll(True)


def scrollBackward():
    scroll(False)


def processIndividual():
    if not inquirer.confirm("¿Está abierto el chat?", default=True):
        return

    d(resourceId='com.whatsapp:id/conversation_contact').click.wait()
    takeScreenshot()
    d.press.back()
    scrollBackward()
    for file in glob.glob('./*.png'):
        shutil.move(os.path.join(".", file), os.path.join(".", "screenshots", file))


if __name__ == "__main__":
    adb = Adb()

    try:
        print(f'Dispositivo con S/N: {adb.device_serial()}')

        questions = [
            inquirer.Confirm(
                "individual",
                message="¿Es una extracción individual?",
                default=True,
            ),
        ]

        answers = inquirer.prompt(questions, theme=GreenPassion())

        if answers['individual']:
            processIndividual()
        else:
            print("Extracción múltiple no implementada")

    except EnvironmentError:
        print("Dispositivo no detectado o desconectado")
