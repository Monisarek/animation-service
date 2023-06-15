import os
import json
import uuid
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Animation
from django.conf import settings


def upload_file(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        json_description = request.FILES['json_description']

        df = pd.read_csv(csv_file)
        description = json.load(json_description)

        fig, ax = plt.subplots()

        if description['type'] == 'histogram':
            anim = create_histogram_animation(df, description, ax, fig)
        elif description['type'] == 'line':
            anim = create_line_animation(df, description, ax, fig)

        animation_id = str(uuid.uuid4())

        animation_dir = os.path.join(settings.MEDIA_ROOT)
        if not os.path.exists(animation_dir):
            os.makedirs(animation_dir)

        gif_path = os.path.join(animation_dir, f'{animation_id}.gif')
        anim.save(gif_path, writer='pillow', fps=2)

        animation = Animation.objects.create(animation_id=animation_id, animation_path=gif_path, duration=2)

        return JsonResponse({'id': animation_id})

    return render(request, 'upload.html')


def view_animation(request, id):
    animation = get_object_or_404(Animation, animation_id=id)
    return render(request, 'animation.html', {'animation': animation})


def create_histogram_animation(df, description, ax, fig):
    data = df[description['data_column']].values

    bars = ax.bar([], [], color=description['color'])

    def update_hist(frame):
        bar_heights = data[:frame+1]
        for bar, height in zip(bars, bar_heights):
            bar.set_height(height)

    ax.set_xlim(0, len(data))
    ax.set_ylim(0, max(data))

    ax.set_xlabel(description['x_label'])
    ax.set_ylabel(description['y_label'])
    ax.set_title(description['title'])

    anim = animation.FuncAnimation(fig, update_hist, frames=len(data), interval=200, blit=False)

    return anim

def create_line_animation(df, description, ax, fig):
    x_data = df[description['x_data_column']].values
    y_data = df[description['y_data_column']].values

    line, = ax.plot([], [], color=description['color'], marker='o')

    def update_line(frame):
        line.set_data(x_data[:frame+1], y_data[:frame+1])

    ax.set_xlim(min(x_data), max(x_data))
    ax.set_ylim(min(y_data), max(y_data))

    ax.set_xlabel(description['x_label'])
    ax.set_ylabel(description['y_label'])
    ax.set_title(description['title'])

    fig.add_subplot(ax)

    ax.add_line(line)

    anim = animation.FuncAnimation(fig, update_line, frames=len(x_data), interval=200, blit=False)

    return anim
