# pylint: disable=invalid-name
"""
Este módulo contiene la lógica para calcular
el total de ventas basándose en un catálogo de
precios y un registro de ventas en formato JSON.
Cumple con los estándares PEP-8 y manejo de errores.
"""

import json
import sys
import time


def load_json_file(filename):
    """
    Carga un archivo JSON y devuelve su contenido.
    Maneja errores de archivo no encontrado y JSON inválido.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(
            f"Error: El archivo '{filename}'"
            " no tiene un formato JSON válido."
        )
        return None
    except (OSError, TypeError) as e:
        print(
            f"Error inesperado al leer '{filename}': {e}"
        )
        return None


def create_price_catalogue(product_list):
    """
    Convierte la lista de productos en un diccionario para búsqueda rápida.
    Clave: título del producto, Valor: precio.
    """
    catalogue = {}
    for product in product_list:
        title = product.get("title")
        price = product.get("price")
        if title and price is not None:
            catalogue[title] = price
    return catalogue


def compute_total_sales(price_catalogue, sales_record):
    """
    Calcula el costo total de las ventas.
    Imprime advertencias en consola si hay datos
    inválidos o productos faltantes.
    """
    total_cost = 0.0

    for sale in sales_record:
        product_name = sale.get("Product")
        quantity = sale.get("Quantity")

        # Validación de datos básicos
        if not product_name or quantity is None:
            print(
                "Error de datos: Registro de"
                f" venta inválido o incompleto: {sale}"
            )
            continue

        # Validación de tipos de datos y valores numéricos
        try:
            quantity = float(quantity)
        except ValueError:
            print(
                f"Error de datos: Cantidad no válida"
                f" para '{product_name}': {quantity}"
            )
            continue

        if product_name in price_catalogue:
            price = price_catalogue[product_name]
            cost = price * quantity
            total_cost += cost
        else:
            print(
                f"Advertencia: El producto"
                f" '{product_name}' no se encuentra"
                " en el catálogo de precios."
            )

    return total_cost


def main():
    """
    Función principal que orquesta la carga de
    archivos, el cálculo y la salida.
    """
    if len(sys.argv) != 3:
        print(
            "Uso: python computeSales.py"
            " priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    # Cargar datos
    product_list = load_json_file(price_file)
    sales_record = load_json_file(sales_file)

    if product_list is None or sales_record is None:
        sys.exit(1)

    # Procesar datos
    price_catalogue = create_price_catalogue(product_list)
    total_cost = compute_total_sales(price_catalogue, sales_record)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formatear resultados
    results_str = (
        f"TOTAL VENTAS\n"
        f"------------\n"
        f"Costo Total: ${total_cost:,.2f}\n"
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos\n"
    )

    # Imprimir en pantalla
    print(results_str)

    # Guardar en archivo
    try:
        with open("SalesResults.txt", "w", encoding='utf-8') as result_file:
            result_file.write(results_str)
    except (OSError, IOError) as e:
        print(
            "Error al escribir en el archivo"
            f" de resultados: {e}"
        )


if __name__ == "__main__":
    main()
