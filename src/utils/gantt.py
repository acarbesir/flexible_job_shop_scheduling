#!/usr/bin/env python

# This module helps creating Gantt from a dictionary or a text file.

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from datetime import datetime, timedelta
import plotly.express as px

def generate_colors(n):
    cmap = plt.cm.get_cmap('tab20c', n)
    return [mcolors.to_hex(cmap(i)) for i in range(cmap.N)]

def draw_chart(data):
    job_colors = {}
    color_index = 0
    tasks = []
    start_time = datetime.now()

    unique_job_ids = set(op[2].split('-')[0] for ops in data.values() for op in ops)
    colors = generate_colors(len(unique_job_ids))

    for machine, operations in sorted(data.items()):
        for op in operations:
            job_id = op[2].split('-')[0]
            if job_id not in job_colors:
                job_colors[job_id] = colors[color_index % len(colors)]
                color_index += 2

            start_second = start_time + timedelta(minutes=op[0])
            end_second = start_time + timedelta(minutes=op[1])
            hover_text = f"{op[3].split('/')[1]}"

            tasks.append(dict(
                Machine=machine,
                Start=start_second,
                Finish=end_second,
                Resource=op[3].split('/')[1].split('_')[0],
                Color=job_colors[job_id],
                Text=hover_text
            ))

    df = pd.DataFrame(tasks)

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Machine",
        color="Resource",
        color_discrete_map={job_id: color for job_id, color in job_colors.items()},
        hover_name="Text",
        title="FJSS Gantt"
    )

    fig.update_yaxes(categoryorder='category descending')
    fig.update_layout(showlegend=True)
    fig.update_traces(marker=dict(line=dict(color='black', width=1)))
    fig.show()
