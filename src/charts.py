import plotly.graph_objects as go

# ── Design tokens ────────────────────────────────────────────────────────────
BG          = '#0a0a0a'
ROSE        = '#c4a090'
TEXT        = '#e8e0dc'
MUTED       = '#7a6a65'
CARD        = '#111111'
BAR_MUTED   = '#3a2e2a'
DONUT_DARK  = '#2a1f1c'
FONT        = 'Inter, system-ui, sans-serif'
MARGINS     = dict(l=20, r=40, t=50, b=30)
FILL_ROSE   = 'rgba(196,160,144,0.1)'


def _base_layout(title=''):
    return dict(
        title=dict(
            text=title,
            font=dict(color=TEXT, size=15, family=FONT),
            x=0,
            xanchor='left',
        ),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT, color=TEXT),
        margin=MARGINS,
        showlegend=False,
        hoverlabel=dict(
            bgcolor=CARD,
            bordercolor=MUTED,
            font=dict(family=FONT, color=TEXT, size=12),
        ),
    )


def _no_axes():
    return dict(showgrid=False, zeroline=False, showline=False, ticks='')


# ── 1. Conversion donut ───────────────────────────────────────────────────────

def chart_conversion_donut(overview_data):
    cr  = overview_data['conversion_rate']
    ncr = overview_data['non_conversion_rate']

    fig = go.Figure(go.Pie(
        labels=['Converted', 'Not Converted'],
        values=[cr, ncr],
        hole=0.65,
        sort=False,
        direction='clockwise',
        marker=dict(colors=[ROSE, DONUT_DARK], line=dict(width=0)),
        textinfo='none',
        hovertemplate='%{label}: %{value}%<extra></extra>',
    ))

    fig.add_annotation(
        text=f'<b>{cr}%</b>',
        x=0.5, y=0.56,
        xref='paper', yref='paper',
        showarrow=False,
        font=dict(size=38, color=ROSE, family=FONT),
    )
    fig.add_annotation(
        text='Conversion Rate',
        x=0.5, y=0.43,
        xref='paper', yref='paper',
        showarrow=False,
        font=dict(size=13, color=MUTED, family=FONT),
    )

    fig.update_layout(**_base_layout())
    return fig


# ── 2. Model comparison ───────────────────────────────────────────────────────

def chart_model_comparison(model_df):
    df     = model_df.sort_values('auc', ascending=True).reset_index(drop=True)
    champ  = float(df.loc[df['champion'], 'auc'].iloc[0])
    colors = [ROSE if c else BAR_MUTED for c in df['champion']]

    fig = go.Figure(go.Bar(
        x=df['auc'],
        y=df['model'].astype(str),
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f'{v:.4f}' for v in df['auc']],
        textposition='outside',
        textfont=dict(color=TEXT, size=12, family=FONT),
        cliponaxis=False,
        hovertemplate='%{y}<br>AUC: %{x:.4f}<extra></extra>',
    ))

    fig.add_vline(
        x=champ,
        line=dict(color=ROSE, width=1.5, dash='dot'),
        opacity=0.35,
    )

    fig.update_layout(**_base_layout('Model Performance — ROC AUC'))
    fig.update_xaxes(**_no_axes(), range=[0.920, 0.935], tickformat='.3f',
                     tickfont=dict(color=MUTED, size=11))
    fig.update_yaxes(**_no_axes(), tickfont=dict(color=TEXT, size=12))
    return fig


# ── 3. PageValues effect ──────────────────────────────────────────────────────

def chart_pagevalues_effect(pv_df):
    fig = go.Figure(go.Scatter(
        x=pv_df['pagevalue'],
        y=pv_df['conversion_prob'],
        mode='lines+markers',
        line=dict(color=ROSE, width=2.5),
        marker=dict(color=ROSE, size=6, line=dict(width=0)),
        fill='tozeroy',
        fillcolor=FILL_ROSE,
        hovertemplate='PageValue %{x}: %{y:.0%}<extra></extra>',
    ))

    fig.add_vline(x=1, line=dict(color=ROSE, width=1.5, dash='dash'), opacity=0.5)

    fig.add_annotation(
        x=1, y=0.55,
        text='Conversion jumps<br>from 8% → 55% here',
        showarrow=True,
        arrowhead=2,
        arrowcolor=ROSE,
        arrowwidth=1.5,
        arrowsize=0.8,
        ax=85, ay=-15,
        font=dict(size=11, color=TEXT, family=FONT),
        xanchor='left',
        bgcolor=BG,
        borderpad=5,
    )

    fig.update_layout(**_base_layout('PageValues Effect on Conversion'))
    fig.update_xaxes(**_no_axes(),
                     title=dict(text='PageValues', font=dict(color=MUTED, size=12)),
                     tickfont=dict(color=MUTED, size=11))
    fig.update_yaxes(**_no_axes(), tickformat='.0%',
                     title=dict(text='Conversion Probability', font=dict(color=MUTED, size=12)),
                     tickfont=dict(color=MUTED, size=11))
    return fig


# ── 4. Monthly conversion ─────────────────────────────────────────────────────

def chart_monthly_conversion(monthly_df):
    months  = monthly_df['month'].astype(str)
    mean_cr = float(monthly_df['conversion_rate'].mean())
    colors  = [ROSE if m == 'Nov' else BAR_MUTED for m in months]

    fig = go.Figure(go.Bar(
        x=months,
        y=monthly_df['conversion_rate'],
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='%{x}: %{y:.1f}%<extra></extra>',
    ))

    fig.add_hline(
        y=mean_cr,
        line=dict(color=MUTED, width=1, dash='dash'),
        opacity=0.6,
    )

    nov = monthly_df[monthly_df['month'].astype(str) == 'Nov']
    if not nov.empty:
        nov_cr = float(nov['conversion_rate'].iloc[0])
        fig.add_annotation(
            x='Nov', y=nov_cr + 2.0,
            text='2.3× baseline',
            showarrow=False,
            font=dict(size=11, color=ROSE, family=FONT),
        )

    fig.update_layout(**_base_layout('Conversion Rate by Month'))
    fig.update_xaxes(**_no_axes(), tickfont=dict(color=MUTED, size=11))
    fig.update_yaxes(**_no_axes(), ticksuffix='%', tickfont=dict(color=MUTED, size=11))
    return fig


# ── 5. Exit rate ──────────────────────────────────────────────────────────────

def chart_exit_rate(exit_df):
    fig = go.Figure(go.Scatter(
        x=exit_df['exit_rate'],
        y=exit_df['conversion_prob'],
        mode='lines',
        line=dict(color=ROSE, width=2.5),
        fill='tozeroy',
        fillcolor=FILL_ROSE,
        hovertemplate='Exit Rate %{x:.0%}: %{y:.0%}<extra></extra>',
    ))

    fig.add_annotation(
        x=float(exit_df['exit_rate'].iloc[-1]),
        y=float(exit_df['conversion_prob'].iloc[-1]),
        text='−30% conversion<br>at high exit rates',
        showarrow=True,
        arrowhead=2,
        arrowcolor=MUTED,
        arrowwidth=1,
        ax=-70, ay=-45,
        font=dict(size=11, color=TEXT, family=FONT),
        xanchor='right',
        bgcolor=BG,
        borderpad=5,
    )

    fig.update_layout(**_base_layout('Exit Rate vs Conversion'))
    fig.update_xaxes(**_no_axes(), tickformat='.0%',
                     title=dict(text='Exit Rate', font=dict(color=MUTED, size=12)),
                     tickfont=dict(color=MUTED, size=11))
    fig.update_yaxes(**_no_axes(), tickformat='.0%',
                     title=dict(text='Conversion Probability', font=dict(color=MUTED, size=12)),
                     tickfont=dict(color=MUTED, size=11))
    return fig


# ── 6. Browsing depth ─────────────────────────────────────────────────────────

def chart_browsing_depth(browsing_df):
    fig = go.Figure(go.Scatter(
        x=browsing_df['product_pages'],
        y=browsing_df['conversion_prob'],
        mode='lines',
        line=dict(color=ROSE, width=2.5),
        fill='tozeroy',
        fillcolor=FILL_ROSE,
        hovertemplate='%{x} pages: %{y:.0%}<extra></extra>',
    ))

    fig.add_vline(x=5, line=dict(color=MUTED, width=1, dash='dash'), opacity=0.5)

    fig.add_annotation(
        x=72, y=0.168,
        text='Window shoppers convert less',
        showarrow=False,
        font=dict(size=11, color=TEXT, family=FONT),
        bgcolor=BG,
        borderpad=5,
    )

    fig.update_layout(**_base_layout('Browsing Depth vs Conversion'))
    fig.update_xaxes(**_no_axes(),
                     title=dict(text='Product Pages Viewed', font=dict(color=MUTED, size=12)),
                     tickfont=dict(color=MUTED, size=11))
    fig.update_yaxes(**_no_axes(), tickformat='.0%',
                     title=dict(text='Conversion Probability', font=dict(color=MUTED, size=12)),
                     tickfont=dict(color=MUTED, size=11))
    return fig
