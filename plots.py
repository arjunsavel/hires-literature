"""
Make the plots.

author: @arjunsavel
"""
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
import pandas as pd
import numpy as np
from matplotlib import rc
from datetime import date


rc('font', family='serif',
                  style='normal', variant='normal',
                  stretch='normal', weight='normal')

set_matplotlib_formats("svg")

# todo: add the correct zenodo

def add_copyright(ax, color='black', lower=False):
    today = date.today()
    
    if lower:
        xy1 = ((-.05, -.13))
        xy2 = ((-.05, -.18))
        xy3 = ((-.05, -.23))
    else:
        xy1 = ((-.05, -.12))
        xy2 = ((-.05, -.17))
        xy3 = ((-.05, -.22))

    url = 'https://zenodo.org/badge/latestdoi/527634198'
    ax.annotate("(c) Arjun Savel, Hayley Beltz, and Isaac Malsky 2022.", xy=xy1, xytext=xy1, zorder=100, 
                xycoords='axes fraction', annotation_clip=False, color=color)

    ax.annotate(f"Cite with Zenodo: {url}", xy=xy2, xytext=xy2,
                    url=url, color='navy',
                    bbox=dict(color='w', alpha=1e-6, url=url), zorder=100, annotation_clip=False,
               xycoords='axes fraction')
    
    ax.annotate(f"""Generated on {today.strftime("%m/%d/%Y")}""", xy=xy3, xytext=xy3,
                    url=url, color=color,
                    bbox=dict(color='w', alpha=1e-6, url=url), zorder=100, annotation_clip=False,
               xycoords='axes fraction')
    return

def papers_over_years(theory_frame, observe_frame):
    """
    inputs: the dataframes!
    """
    full_frame = pd.concat([observe_frame, theory_frame])
    full_papers_frame = full_frame.drop_duplicates(subset=['lead', 'planet', 'observation', 'instrument', 'year'])
    
    fig, ax =  plt.subplots(figsize=(10,6))
    theory_percent = len(theory_frame) / len(full_papers_frame)


    ax.hist(full_papers_frame['year'], color='goldenrod')
    ax.text(1998, 120, f'~{round(theory_percent * 100)}% of the {len(full_papers_frame)} high-res papers\nare theory papers',
            fontsize=14)
    ax.set_title('Hi-res papers', fontsize=25)
    ax.set_xlabel('Year', fontsize=25)
    ax.set_ylabel('Count', fontsize=25)
    
    add_copyright(ax, color='black')
    
    plt.savefig('plots/papers_over_years.jpg', dpi=300)
    

def water_detections(observe_frame):
    """
    takes all observations, cuts them into just the good SNR ones, and splits up into water.
    """
    
    hrs_frame = observe_frame[observe_frame.SNR > 4.5]
    water_frame = hrs_frame[hrs_frame.species=='H$_2$O']
    fig, ax = plt.subplots(figsize=(10,6), facecolor='#264e5a')

    hrs_frame.hist('year', bins=np.arange(2010, 2023), ax=ax, color='#264e5a', label='Detections')
    water_frame.hist('year', bins=np.arange(2010, 2023), ax=ax, color='gray', label='Water detections')
    ax.grid(False)
    ax.set_xlim([2010, 2022])
    ax.set_ylabel('Count', fontsize=25, color='white')
    ax.set_xlabel('Year', fontsize=25, color='white')
    ax.set_title('', fontsize=18)
    plt.legend(fontsize=25)
    plt.yticks((1, 10, 100), color='white')
    plt.xticks((2010, 2012, 2014, 2016, 2018, 2020, 2022), color='white')

    plt.yscale('log')
    
    add_copyright(ax, color='white')


    plt.savefig('plots/water.jpg', dpi=300)
    
def hrs_obs_latest_gridded(observe_frame):
    """
    todo: maybe just hrs_frame once.
    """
    hrs_frame = observe_frame[observe_frame.SNR > 4.5]
    hrs_frame = hrs_frame.sort_values(by=['planet'])
    hrs_frame = hrs_frame.replace({'species': 'C2H2'}, {'species': r'C$_2$H$_2$'}, regex=True)
    hrs_frame = hrs_frame.replace({'species': 'NH3'}, {'species': r'NH$_3$'}, regex=True)
    hrs_frame = hrs_frame.replace({'species': 'CH4'}, {'species': r'CH$_4$'}, regex=True)
    hrs_frame = hrs_frame.replace({'species': 'H2O'}, {'species': r'H$_2$O'}, regex=True)
    hrs_frame = hrs_frame.replace({'species': 'Na D1'}, {'species': r'Na'}, regex=True)
    hrs_frame = hrs_frame.replace({'species': 'Na D2'}, {'species': r'Na'}, regex=True)
    hrs_frame = hrs_frame.replace({'species': 'Ca+ H'}, {'species': r'Ca+'}, regex=False)
    hrs_frame = hrs_frame.replace({'species': 'Ca+ K'}, {'species': r'Ca+'}, regex=False)
    hrs_frame = hrs_frame.replace({'species': 'H alpha'}, {'species': r'H$\alpha$'})
    hrs_frame = hrs_frame.replace({'species': 'H beta'}, {'species': r'H$\beta$'})
    hrs_frame = hrs_frame.replace({'species': 'H gamma'}, {'species': r'H$\gamma$'})
    
    year = 2022


    fig, ax = plt.subplots(figsize=(22,10))
    # ax.grid(True)
    p = ax.scatter(hrs_frame['planet'], hrs_frame['species'], c='white')
    p = ax.scatter(hrs_frame[hrs_frame.year <= year]['planet'], hrs_frame[hrs_frame.year <= year]['species'], 
                   c=hrs_frame[hrs_frame.year <= year]['SNR'], s=80)
    c = plt.colorbar(p,  pad=0)
    c.set_label(label='SNR', fontsize=25)
    # ax.xticks(rotation = 45);

    ax.set_title(f'The state of HRS detections: {year}', fontsize=25)
    ax.set_xlabel(f'Planet', fontsize=25)
    ax.set_ylabel(f'Species', fontsize=25)

    ax.tick_params(axis='x', which='major', labelsize=12, rotation = 35)
    ax.tick_params(axis='y', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=8)


    left, bottom, width, height = [.16, 0.45, 0.2, 0.4]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Year')

    ax.grid(True)


    hrs_frame.hist('year', bins=np.arange(2010, 2024), ax=ax2, color='goldenrod', label='Detections',
                  grid=False)
    ax2.set_xlim([2010, 2023])
    ax2.set_title('')
    add_copyright(ax, color='black', lower=True)
#     ax.text(-2, -10, f"""Arjun Savel — {datetime.today().strftime('%Y-%m-%d')}""", fontsize=15)


    plt.savefig('plots/2022_histogram.jpg', bbox_inches='tight', dpi=300)
    
def theory_plot(theory_frame):
    three_d_percent = len(theory_frame[theory_frame.dimensions==3])/len(theory_frame)


    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(theory_frame.year, color='teal')
    ax.set_xlabel('Year', fontsize=25)
    ax.set_ylabel('Count', fontsize=25)

    ax.text(2008, 12, f'~{round(three_d_percent * 100)}% of the {len(theory_frame)} theory papers\nuse 3D models',
            fontsize=14)

    ax.set_title('Hi-res theory papers', fontsize=25)
    add_copyright(ax, color='black')
    plt.savefig('plots/theory_plot.jpg', bbox_inches='tight', dpi=300)


if __name__=='__main__':
    # load the frames
    theory_frame = pd.read_csv('data/theory_frame.csv')
    observe_frame = pd.read_csv('data/observe_frame.csv')
    
    # run the plots
    theory_plot(theory_frame)
    hrs_obs_latest_gridded(observe_frame)
    water_detections(observe_frame)
    papers_over_years(theory_frame, observe_frame)
    # todo: papers by each year
