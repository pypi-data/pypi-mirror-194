from cyberonix.main.tools import template
def waiting():
    try:
        input("\n\u001b[31m[+]press ENTER to go back\u001b[0m")
    except KeyboardInterrupt:
        template.exit_program()

