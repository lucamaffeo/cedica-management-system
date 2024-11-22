from unittest import result
import matplotlib.pyplot as plt
from io import BytesIO
from sqlalchemy import func
from src.core.models.receipt import Receipt
from src.core.models.rider import Rider
from src.core.database import db
import matplotlib
matplotlib.use('Agg')

# Función para generar gráfico de barras (Ingresos por mes)


def generar_grafico_barras_ingresos_por_mes():
    # Consulta para obtener los ingresos por mes
    results = db.session.query(
        func.extract('year', Receipt.payment_date).label('year'),
        func.extract('month', Receipt.payment_date).label('month'),
        func.sum(Receipt.quantity).label('total')
    ).group_by('year', 'month').order_by('year', 'month').all()

    # Extraer datos para el gráfico
    # Formato: MM-YYYY
    months = [
        f"{int(result.month):02d}-{int(result.year)}" for result in results]
    totals = [float(result.total) for result in results]

    # Crear gráfico de barras
    plt.figure(figsize=(10, 6))  # Tamaño ajustado para que quepa todo
    plt.bar(months, totals, color='skyblue')
    plt.title('Ingresos por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Monto Total')
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas para mayor claridad

    # Guardar la imagen en un objeto BytesIO
    img = BytesIO()
    plt.tight_layout()  # Ajustar el diseño para evitar superposiciones
    plt.savefig(img, format='png')
    img.seek(0)  # Volver al inicio del archivo en memoria
    plt.close()  # Cerrar la figura después de guardar
    return img

# Función para generar gráfico de torta (Discapacidades)


def generar_grafico_torta_discapacidades():
    # Limpiar cualquier gráfico previo
    plt.clf()

    # Consulta para obtener la cantidad de discapacidades
    results = db.session.query(
        func.count(Rider.id).label('count'),
        Rider.disability_type
    ).group_by(Rider.disability_type).all()

    labels = [result.disability_type for result in results]
    sizes = [result.count for result in results]

    # Crear gráfico de torta
    plt.figure(figsize=(8, 6))  # Tamaño del gráfico
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    plt.title('Distribución por Tipo de Discapacidad', fontsize=14)

    # Asegurar que el diseño sea ajustado
    plt.tight_layout()

    # Guardar la imagen en un objeto BytesIO
    img = BytesIO()
    # bbox_inches ajusta los bordes
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)  # Volver al inicio del archivo en memoria
    plt.close()  # Cierra la figura para liberar memoria
    return img


def generar_grafico_barras_becados():
    # Consulta para obtener la cantidad de becados y no becados
    results = db.session.query(
        Rider.scholarship.label('scholarship_status'),
        func.count(Rider.id).label('count')
    ).group_by('scholarship_status').all()

    # Asignar valores de conteo a etiquetas específicas
    becados_count = next((int(result.count)
                         for result in results if result.scholarship_status), 0)
    no_becados_count = next(
        (int(result.count) for result in results if not result.scholarship_status), 0)

    # Hardcodear etiquetas de los estados
    statuses = ['Becados', 'No Becados']
    counts = [becados_count, no_becados_count]

    # Crear gráfico de barras
    plt.bar(statuses, counts, color=['#66b3ff', '#ff9999'])
    plt.title('Cantidad de Jinetes y Amazonas Becados')
    plt.xlabel('Estado de Becas')
    plt.ylabel('Cantidad de Personas')
    cantidad = max(counts)  # Usar el máximo conteo para el rango de y-axis
    plt.yticks(range(0, cantidad + 1, 1))

    # Guardar la imagen en un objeto BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

# Función para generar gráfico de barras apiladas (Ingresos por Año/Mes)


def generar_grafico_barras_apiladas_ingresos():
    # Consulta para obtener los ingresos por año y mes
    results = db.session.query(
        func.extract('year', Receipt.payment_date).label('year'),
        func.extract('month', Receipt.payment_date).label('month'),
        func.sum(Receipt.quantity).label('total')
    ).group_by('year', 'month').all()

    # Preparar datos
    data = {}
    for result in results:
        year = int(result.year)
        month = int(result.month)
        total = float(result.total)
        if year not in data:
            data[year] = [0] * 12
        data[year][month - 1] = total

    # Crear gráfico apilado
    plt.figure(figsize=(10, 6))
    months = [f'M{m + 1}' for m in range(12)]
    for year, values in sorted(data.items()):
        plt.bar(months, values, label=str(year), bottom=[sum(x) for x in zip(
            *[data[y] for y in sorted(data.keys()) if y < year])])

    plt.title('Ingresos por Año/Mes')
    plt.xlabel('Meses')
    plt.ylabel('Ingresos')
    plt.legend(title="Año", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Guardar la imagen en un objeto BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img
