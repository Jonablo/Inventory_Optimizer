# Inventory Optimizer

Este proyecto implementa y expone un motor de optimización de inventarios basado en programación dinámica, con persistencia en PostgreSQL y una interfaz REST en Flask. Además incluye scripts de experimentación y un frontend básico para visualizar resultados.

---

## Requisitos previos

* Docker y Docker Compose (opcional, para levantar la base de datos)
* Python 3.11 y `venv`
* Node.js y npm (para frontend)

## 1. Clonar repositorio y crear entorno virtual

```bash
git clone <URL_DEL_REPO>
cd inventory_optimizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configurar y levantar PostgreSQL

### Opción A: Contenedor Docker

```bash
docker run -d --name inv_pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=inventory_optimizer -p 5432:5432 postgres:14
```

### Opción B: Devcontainer con feature PostgreSQL

Abre VSCode en Devcontainer y levanta el servicio de PostgreSQL.

## 3. Inicializar base de datos

```bash
python init_db.py
# Debe imprimir: "Tablas creadas en: postgresql://postgres:***@localhost:5432/inventory_optimizer"
```

## 4. Levantar API Flask

```bash
export FLASK_APP=src/web/app.py
export FLASK_ENV=development    # opcional: recarga automática y debug
flask run --host=0.0.0.0 --port=5000
```

### Endpoints disponibles:

* **POST** `/optimization/`
  Ejecuta optimización. Cuerpo JSON con campos: `initial_inventory`, `max_inventory`, `max_order`, `horizon`, `costs`, `demand_params`.
  **Ejemplo**:

  ```bash
  curl -X POST http://localhost:5000/optimization/ \
    -H "Content-Type: application/json" \
    -d '{
          "initial_inventory": 0,
          "max_inventory": 5,
          "max_order": 5,
          "horizon": 3,
          "costs": { "c": [1,1,1], "h": 2, "p": 10 },
          "demand_params": { "support": [0,1,2], "probabilities": [0.3,0.4,0.3] }
        }'
  ```

* **GET** `/optimization/<id>`
  Obtiene metadatos de la optimización.

* **GET** `/optimization/<id>/policy`
  Tabla completa de políticas \$(t,I)\to x\$.

* **GET** `/optimization/<id>/results`
  Detalle de costos por período y nivel de inventario.

* **GET** `/optimization/<id>/policy-summary`
  Resumen \$(s\_t,S\_t)\$ por período.

## 5. Ejecutar scripts de experimentación

Ejecuta cada script desde la raíz del proyecto:

```bash
python run_experiments.py         # Tabla 7.1 y regresión log-log
python run_scalability_avg.py     # Regresión log-log (promedios)
python run_specific_cases.py      # Casos particulares (constante, Poisson, variable)
python run_comparison_methods.py  # Comparación DP vs HS vs MC vs LP
python run_param_sensitivity.py   # Sensibilidad a p y h
python run_deterministic_scenarios.py  # Escenarios optimista/pesimista/realista
python run_value_at_risk.py       # Cálculo de VaR
```

> **Opcional:**
>
> ```bash
> python run_global_sensitivity.py # Sensibilidad global (SALib)
> ```

Cada script imprime en consola los resultados numéricos, listos para capturar como evidencia.

## 6. Levantar frontend local

```bash
cd src/web/frontend
npm install
npm run dev
```

Abre tu navegador en [http://localhost:3000](http://localhost:3000) para ver el formulario e interface.

---

## Capturas de Ejecución

Agrega aquí capturas de pantalla de cada sección (API, scripts, frontend) para documentar los resultados obtenidos.

---

> **Autor:** Grupo #, Investigación de Operaciones
> **Fecha:** Julio 18, 2025.