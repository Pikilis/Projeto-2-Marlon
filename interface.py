import gradio as gr
import requests

# Função para adicionar uma nova entrada
def add_entry(mood, activities, sleep_hours, date):
    url = "http://127.0.0.1:5000/add_entry"
    data = {
        "mood": mood,
        "activities": activities,
        "sleep_hours": sleep_hours,
        "date": date
    }
    response = requests.post(url, json=data)
    return response.json()['message']

# Função para obter as entradas registradas
def get_entries():
    url = "http://127.0.0.1:5000/get_entries"
    response = requests.get(url)
    entries = response.json()
    if not entries:
        return []
    return [[entry[0], entry[1], entry[2], entry[3], entry[4]] for entry in entries]

# Função para calcular a média de humor
def get_average_mood():
    url = "http://127.0.0.1:5000/get_average_mood"
    response = requests.get(url)
    average = response.json()
    if average["average_mood"] is None:
        return "Nenhuma entrada encontrada."
    else:
        return f"A média do humor é: {average['average_mood']:.2f}"

# Função para obter o melhor dia
def get_best_day():
    url = "http://127.0.0.1:5000/get_best_day"
    response = requests.get(url)
    best_day = response.json()
    if best_day["best_day"] is None:
        return "Nenhum melhor dia encontrado."
    else:
        day = best_day["best_day"]
        return f"Data: {day['date']}\nHumor: {day['mood']}\nAtividades: {day['activities']}\nHoras de Sono: {day['sleep_hours']}"

# Criar a interface com Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Gerenciamento de Saúde Mental")

    with gr.Tab("Adicionar Entrada"):
        mood = gr.Slider(minimum=1.0, maximum=5.0, step=0.1, label="Humor (1.0 a 5.0)")
        activities = gr.Textbox(label="Atividades")
        sleep_hours = gr.Number(label="Horas de Sono", value=7.5)
        date = gr.Textbox(label="Data (Formato: YYYY-MM-DD)")

        message_output = gr.Textbox(label="Mensagem de confirmação", interactive=False)
        submit_button = gr.Button("Registrar Entrada")
        submit_button.click(add_entry, inputs=[mood, activities, sleep_hours, date], outputs=message_output)

    with gr.Tab("Ver Entradas"):
        entries_output = gr.Dataframe(headers=["ID", "Humor", "Atividades", "Horas de Sono", "Data"], row_count=5)
        refresh_button = gr.Button("Atualizar Entradas")
        refresh_button.click(get_entries, inputs=[], outputs=entries_output)

    with gr.Tab("Média de Humor"):
        average_output = gr.Textbox(label="Média de Humor", interactive=False)
        calculate_average_button = gr.Button("Calcular Média")
        calculate_average_button.click(get_average_mood, inputs=[], outputs=average_output)

    with gr.Tab("Melhor Dia"):
        best_day_output = gr.Textbox(label="Melhor Dia", interactive=False)
        show_best_day_button = gr.Button("Ver Melhor Dia")
        show_best_day_button.click(get_best_day, inputs=[], outputs=best_day_output)

# Iniciar a interface
demo.launch()
