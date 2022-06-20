from uiautomator import device as d
from uiautomator import Adb
import inquirer
from inquirer.themes import GreenPassion

adb = Adb()


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

    print('\x1b[6;30;44m' + 'Proceso iniciado...' + '\x1b[0m')
    d(resourceId='com.whatsapp:id/conversation_contact').click.wait()
    takeScreenshot()
    d.press.back()
    scrollBackward()
    print('\x1b[6;30;42m' + 'Proceso terminado' + '\x1b[0m')


if __name__ == "__main__":

    questions = [
        inquirer.Confirm(
            "conectado",
            message=f'¿Es correcto el S/N: {adb.device_serial()}?',
            default=True,
        ),
        inquirer.Confirm(
            "individual",
            message="¿Es una extracción individual?",
            default=True,
        ),
    ]

    answers = inquirer.prompt(questions, theme=GreenPassion())
    if not answers['conectado']:
        quit()

    if answers['individual']:
        processIndividual()
    else:
        print("Extracción múltiple no implementada")
