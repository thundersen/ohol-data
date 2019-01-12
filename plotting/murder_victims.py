import collections
from functools import reduce
from datetime import date, timedelta

import plotly.graph_objs as go
import plotly.offline as py
from plotly import tools

from logreader.reader import read_history

SERVERS = [1, 2, 3, 4, 5, 6, 7]

START = date(2019, 1, 6)

END = date(2019, 1, 6)


def percentage_annotations(counts_by_label):
    total = sum(counts_by_label.values())

    result = []

    for label, count in counts_by_label.items():
        perc = float(count) / total * 100
        annotation = dict(x=count, y=label, text=f'{" " * 15}<b>{perc:.2f}%</b>', showarrow=False)
        result.append(annotation)

    return result


def cause_of_death_bar_trace(all_characters, trace_def):

    filter_func = trace_def[1]

    characters = [c for c in all_characters if filter_func(c)]

    baby_death_age = 1

    cause_of_death = [
        c.cause_of_death if c.age_at_death() > timedelta(minutes=baby_death_age)
        else 'baby death'
        for c in characters]

    raw_counts = collections.Counter(cause_of_death)

    counts = list(sorted(raw_counts.items(), key=lambda k: k[1]))
    cause_labels = [x[0] for x in counts]
    cause_counts = [x[1] for x in counts]

    total = len(characters)

    return {
        'title': f'{trace_def[0]}; Total: {total}',
        'trace': go.Bar(x=cause_counts, y=cause_labels, name='Cause of Death', orientation='h', showlegend=False),
        'annotations': percentage_annotations(raw_counts)
    }


def make_cause_of_death_traces():
    trace_defs = [
        ('All', lambda c: True),
        ('Female Non-Eves', lambda c: c.sex == 'F' and not c.is_eve),
        ('Males', lambda c: c.sex == 'M'),
        ('Eves', lambda c: c.is_eve),
    ]

    traces = [cause_of_death_bar_trace(characters, trace_def) for trace_def in trace_defs]

    xpos = 1
    for trace in traces:
        trace['xpos'] = xpos
        for a in trace['annotations']:
            a['xref'] = f'x{xpos}'
        xpos = xpos + 1

    return traces


if __name__ == '__main__':
    history = read_history(SERVERS, START, END)

    history.print_completeness_report()

    characters = history.complete_characters()

    cause_of_death_traces = make_cause_of_death_traces()

    fig = tools.make_subplots(
        rows=1,
        cols=len(cause_of_death_traces),
        shared_yaxes=True,
        subplot_titles=[trace['title'] for trace in cause_of_death_traces])

    for t in cause_of_death_traces:
        fig.append_trace(t['trace'], 1, t['xpos'])

    annotations = reduce(lambda l1, l2: l1 + l2,  [trace['annotations'] for trace in cause_of_death_traces])

    fig['layout']['annotations'] += tuple(annotations)

    py.plot(fig)

    # py.plot({
    #     'data': [cause_of_death_trace],
    #     'layout': go.Layout(annotations=percentage_annotations(raw_counts))
    # })

    # n_murders = [len(c.murder_victims) for c in characters if c.is_murderer()]

    # n_murders_histogram = go.Histogram(y=n_murders, name='N Murders')

    # py.plot([n_murders_histogram])

# fig['layout'].update(title=f'Players from {START} to {END} on Servers {", ".join([str(s) for s in SERVERS])}')
#
# first_birth_trace = go.Histogram(x=[p.first_birth() for p in players], showlegend=False)
#
# fig.append_trace(playtime_trace, 1, 1)
# fig.append_trace(first_birth_trace, 2, 1)
#
# py.plot(fig)
