import json
import os
from colorama import Fore, Style, init

# Inicialización de colorama
init(autoreset=True)

class Main:
    def __init__(self):
        self.objetos = {}

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def ask(self, count):
        objeto = {}

        objeto['nombre'] = input(f"{Fore.YELLOW}Ingrese el nombre del objeto nº{count} -> {Fore.RESET}").strip().lower()
        
        while True:
            try:
                objeto['peso'] = float(input(f"{Fore.YELLOW}Ingrese el peso de {objeto['nombre']} -> {Fore.RESET}").strip())
                break
            except ValueError:
                print(f"{Fore.RED}Error: El peso debe ser un número.")
        
        while True:
            try:
                objeto['profit'] = float(input(f"{Fore.YELLOW}Ingrese el profit de {objeto['nombre']} -> {Fore.RESET}").strip())
                break
            except ValueError:
                print(f"{Fore.RED}Error: El profit debe ser un número.")
        
        return objeto

    def save_data(self, nombre_archivo):
        file = f"{nombre_archivo}.json"
        try:
            with open(file, 'w') as file_json:
                json.dump(self.objetos, file_json, indent=4)
            print(f"{Fore.GREEN}Base de datos (JSON) generado con éxito.")
        except Exception as e:
            print(f"{Fore.RED}Error al guardar el archivo JSON: {str(e)}")

    def menu(self):
        self.clear()

        while True:
            try:
                amount_o = int(input(f"{Fore.YELLOW}¿Cuántos objetos desea añadir? -> {Fore.RESET}"))
                if amount_o <= 0:
                    print(f"{Fore.RED}Debe ingresar al menos un objeto.")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}Error: La cantidad de objetos debe ser un número entero.")

        for count in range(1, amount_o + 1):
            objeto = self.ask(count)
            
            if objeto['nombre'] not in self.objetos:
                self.objetos[objeto['nombre']] = []
            
            self.objetos[objeto['nombre']].append({
                'Peso': objeto['peso'],
                'Profit': objeto['profit']
            })

        ask_name = input(f"{Fore.YELLOW}Con qué nombre quieres guardar la base de datos? -> {Fore.RESET}")
        self.save_data(ask_name)
        break

    def run(self):
        while True:
            self.menu()
                


if __name__ == "__main__":
    genjson = Main()
    genjson.run()
