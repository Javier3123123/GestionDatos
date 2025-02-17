import json
import time
import os
import csv
import requests
import logging
from datetime import datetime
import matplotlib.pyplot as plt
from colorama import Fore, init

init(autoreset=True)

class Main:
    def __init__(self, config):
        self.config = config
        self.file_config = config['archivo_json']
        self.max_w = config['peso_maximo']
        self.type_save = config['guardar_como']
        self.debug = config['debug']
        self.save_errors = config['guardar_errores']
        self.save_final = config['guardar_resultado']
        self.medida = config['medida']
        self.savegrafic = config['generar_grafico']
        self.datos = {}
        self.valid_o = []
        self.objetos_filtrados = []

    def graficmetplotlib(self):
        try:
            objetos = [item['objeto'].capitalize() for item in self.objetos_filtrados]
            pesos = [item['Peso'] for item in self.objetos_filtrados]
            profits = [item['Profit'] for item in self.objetos_filtrados]

            type_g = self.config.get('grafico_tipo', 'barras')

            if type_g == 'barras':
                fig, ax = plt.subplots(figsize=(10, 6))
                bar_width = 0.35
                index = range(len(objetos))

                ax.bar(index, profits, bar_width, label='Profit', color='b')
                ax.bar([i + bar_width for i in index], pesos, bar_width, label='Peso', color='g')

                ax.set_xlabel('Objetos')
                ax.set_ylabel('Valor')
                ax.set_title('Gráfico')
                ax.set_xticks([i + bar_width / 2 for i in index])
                ax.set_xticklabels(objetos, rotation=45, ha='right')
                ax.legend()

            elif type_g == 'lineas':
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(objetos, profits, label='Profit', color='b', marker='o')
                ax.plot(objetos, pesos, label='Peso', color='g', marker='x')

                ax.set_xlabel('Objetos')
                ax.set_ylabel('Valor')
                ax.set_title('Gráfico')
                ax.legend()

            elif type_g == 'pastel':
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(profits, labels=objetos, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                ax.set_title('Gráfico')

            else:
                print(Fore.RED + "Tipo de gráfico no soportado en la configuración.")
                return

            nombre_archivo_imagen = f"grafico_{type_g}.{self.get_time()}.png"
            plt.tight_layout()
            plt.savefig(nombre_archivo_imagen)
            plt.close()

            print(Fore.GREEN + f"Gráfico guardado como '{nombre_archivo_imagen}'.")
        except Exception as e:
            error_msg = f"Error al generar el gráfico: {str(e)}"
            self.manejar_error(error_msg)

            
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def manejar_error(self, mensaje_error):
        if self.debug:
            print(Fore.RED + mensaje_error)
        if self.save_errors:
            log_filename = f"error_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
            logging.basicConfig(filename=log_filename, level=logging.ERROR, 
                                format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(mensaje_error)


    def load_data(self):
        try:
            if self.debug:
                print(Fore.YELLOW + "Cargando los datos sobre los objetos...")
            
            start_time = time.time()
            
            if self.file_config.startswith('http'):
                response = requests.get(self.file_config)
                response.raise_for_status()
                self.datos = response.json()
            else:
                with open(self.file_config, 'r') as archivo:
                    self.datos = json.load(archivo)
            
            carga_timesave = time.time() - start_time
            if self.debug:
                print(Fore.GREEN + f"Datos obtenidos en {carga_timesave:.2f} segundos.\n")
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Error al descargar el archivo JSON desde la URL: {str(e)}"
            self.manejar_error(error_msg)
        except FileNotFoundError as e:
            error_msg = f"Error al abrir el archivo local: {str(e)}"
            self.manejar_error(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"Error al parsear el archivo JSON: {str(e)}"
            self.manejar_error(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado al cargar los datos: {str(e)}"
            self.manejar_error(error_msg)

    def get_totalw(self):
        try:
            if self.debug:
                print(Fore.YELLOW + "Calculando peso total...")
            
            start_time = time.time()
            peso_total = sum(detalle['Peso'] for objeto, detalles in self.datos.items() for detalle in detalles)
            timesave = time.time() - start_time
            
            if self.debug:
                print(Fore.GREEN + f"Peso total calculado en {timesave:.2f} segundos: {peso_total} {self.medida}.\n")
            
            return peso_total
        
        except Exception as e:
            error_msg = f"Error al calcular el peso total: {str(e)}"
            self.manejar_error(error_msg)

    def filter_objects(self):
        try:
            if self.debug:
                print(Fore.YELLOW + "Filtrando objetos válidos...")
            
            start_time = time.time()
            for objeto, detalles in self.datos.items():
                for detalle in detalles:
                    if detalle['Peso'] <= self.max_w:
                        self.valid_o.append({
                            'objeto': objeto,
                            'Peso': detalle['Peso'],
                            'Profit': detalle['Profit']
                        })
            
            timesave = time.time() - start_time
            if self.debug:
                print(Fore.GREEN + f"Filtrado de objetos realizado en {timesave:.2f} segundos.\n")
        
        except Exception as e:
            error_msg = f"Error al filtrar los objetos: {str(e)}"
            self.manejar_error(error_msg)

    def order_o(self):
        try:
            if self.debug:
                print(Fore.YELLOW + "Ordenando objetos...")
            
            start_time = time.time()
            self.objetos_filtrados = sorted(self.valid_o, key=lambda item: (-item['Profit'], item['Peso']))
            timesave = time.time() - start_time
            
            if self.debug:
                print(Fore.GREEN + f"Objetos ordenados en {timesave:.2f} segundos.\n")
        
        except Exception as e:
            error_msg = f"Error al ordenar los objetos: {str(e)}"
            self.manejar_error(error_msg)

    def show_objects(self):
        try:
            print(Fore.YELLOW + "\nResultados:\n")
            for item in self.objetos_filtrados:
                print(Fore.BLUE + f"- Objeto: {item['objeto'].capitalize()}, Peso: {item['Peso']} KG, Profit: ${item['Profit']}")
                time.sleep(0.1)
        except Exception as e:
            error_msg = f"Error al mostrar los objetos: {str(e)}"
            self.manejar_error(error_msg)

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def save_csv(self):
        try:
            nombre_archivo = f"objetos_{self.get_time()}.csv"
            with open(nombre_archivo, mode='w', newline='') as archivo_csv:
                writer = csv.DictWriter(archivo_csv, fieldnames=['objeto', 'Peso', 'Profit'])
                writer.writeheader()
                for item in self.objetos_filtrados:
                    writer.writerow({'objeto': item['objeto'], 'Peso': item['Peso'], 'Profit': item['Profit']})
            print(Fore.GREEN + f"\nResultados guardados en '{nombre_archivo}'.")
        except Exception as e:
            error_msg = f"Error al guardar el archivo CSV: {str(e)}"
            self.manejar_error(error_msg)

    def json_save(self):
        try:
            nombre_archivo = f"objetos_{self.get_time()}.json"
            with open(nombre_archivo, mode='w') as file_config:
                json.dump(self.objetos_filtrados, file_config, indent=4)
            print(Fore.GREEN + f"Resultados guardados en '{nombre_archivo}'.")
        except Exception as e:
            error_msg = f"Error al guardar el archivo JSON: {str(e)}"
            self.manejar_error(error_msg)

    def save_txt(self):
        try:
            nombre_archivo = f"objetos_{self.get_time()}.txt"
            with open(nombre_archivo, mode='w') as archivo_txt:
                for item in self.objetos_filtrados:
                    archivo_txt.write(f"- Objeto: {item['objeto'].capitalize()}, Peso: {item['Peso']} KG, Profit: ${item['Profit']}\n")
            print(Fore.GREEN + f"Resultados guardados en '{nombre_archivo}'.")
        except Exception as e:
            error_msg = f"Error al guardar el archivo TXT: {str(e)}"
            self.manejar_error(error_msg)

    def save_results(self):
        if self.save_final:
            try:
                if self.type_save == 'csv':
                    self.save_csv()
                elif self.type_save == 'json':
                    self.json_save()
                elif self.type_save == 'txt':
                    self.save_txt()
                else:
                    print(Fore.RED + "Configuración de guardado inválida.")
            except Exception as e:
                error_msg = f"Error al guardar los resultados: {str(e)}"
                self.manejar_error(error_msg)
        else:
            pass

def config_l():
    try:
        with open('config.json', 'r') as file_config:
            return json.load(file_config)
    except Exception as e:
        print(Fore.RED + f"Error al cargar el archivo de configuración: {str(e)}")
        exit()

def main():
    try:
        config = config_l()

        gestion = Main(config)

        gestion.clear()

        gestion.load_data()

        gestion.get_totalw()

        gestion.filter_objects()

        gestion.order_o()

        gestion.show_objects()

        gestion.save_results()

        if gestion.savegrafic:
            gestion.graficmetplotlib()

    except KeyboardInterrupt:
        if gestion.debug:
            print(Fore.RED + "\nInterrupción detectada.")
        else:
            print(Fore.RED + "\nEl proceso fue interrumpido.")
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        gestion.manejar_error(error_msg)

if __name__ == "__main__":
    main()
