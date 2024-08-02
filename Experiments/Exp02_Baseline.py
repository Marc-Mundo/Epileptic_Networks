from neuron import h, units, coreneuron
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import pickle
import time
import random
from multiprocessing import Pool, cpu_count
from SynapticaSims import Cell, NetParams, Network, Simulator


h.nrn_load_dll(
    "../Models/Sanjay_model/x86_64/libnrnmech.so"
)

"""
h("strdef simname, allfiles, simfiles, output_file, datestr, uname, osname, comment")
h.simname=simname = "mtlhpc"
h.allfiles=allfiles = "geom.hoc pyinit.py geom.py network.py params.py run.py"
h.simfiles=simfiles = "pyinit.py geom.py network.py params.py run.py"
h("runnum=1")
runnum = 1.0
h.datestr=datestr = "11may20"
h.output_file=output_file = "data/11may20.05"
h.uname=uname = "x86_64"
h.osname=osname="linux"
h("templates_loaded=0")
templates_loaded=0
h("xwindows=1.0")
xwindows = 1.0
h.xopen("nrnoc.hoc")
h.xopen("init.hoc")

h.tstop=3e3
h.dt = 0.1
h.steps_per_ms = 1/h.dt
#h.cvode_local(1)
h.v_init = -65
"""


h.nrnmpi_init()
pc = h.ParallelContext()
if pc.nhost() == 1:
    pc.nthread(12)
pc.set_maxstep(10 * units.ms)

# Load std library
# h.load_file('stdrun.hoc')
h.celsius = 6.3

h.tstop = 5000  # ms
h.dt = 0.1  # ms
h.t = 0
h.steps_per_ms = 1 / h.dt

global_seed = 422
np.random.seed(global_seed)
rng = h.Random()
rng.Random123_globalindex(global_seed)
rng.Random123(global_seed, global_seed, global_seed)


# h.cvode.cache_efficient(1)


ALL_PYR = set(list(range(0, 800)))
ALL_BWB = set(list(range(800, 1000)))
ALL_OLM = set(list(range(1000, 1200)))


def init_network(**kwargs):
    netParams = NetParams()
    netParams.simParams["tstop"] = h.tstop
    netParams.simParams["dt"] = h.dt
    netParams.simParams["t"] = 0.0
    netParams.seeds = {
        "net": 1011,
        "cell": kwargs.get("cell_seed", 404),
        "conn": kwargs.get("conn_seed", 89250),
        "stim": kwargs.get("stim_seed", 773956),
        "global": global_seed,
    }

    netParams.cellParams["Pyr"] = {
        "Cell": Cell.PyrAdr,
        "nCells": 800,
        "xrange": [0, 5],
        "yrange": [0, 5],
        "zrange": [0, 5],
    }
    netParams.cellParams["Bwb"] = {
        "Cell": Cell.Bwb,
        "nCells": 200,
        "xrange": [5, 7],
        "yrange": [5, 7],
        "zrange": [5, 7],
    }
    netParams.cellParams["OLM"] = {
        "Cell": Cell.Ow,
        "nCells": 200,
        "xrange": [5, 7],
        "yrange": [5, 7],
        "zrange": [5, 7],
    }

    # -------------
    # Connections
    # -------------

    # Pyr NMDA
    scale = kwargs.get("scale_conn_weight", 1.0)
    netParams.connParams["Pyr->Bwb NMDA"] = {
        "method": "many_to_one",
        "count": 100,
        "weight": scale * 1.15 * 1.2e-3,
        "synapse": "somaNMDA",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["Pyr->OLM NMDA"] = {
        "method": "many_to_one",
        "count": 10,
        "weight": scale * 1.0 * 0.7e-3,
        "synapse": "somaNMDA",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["Pyr->Pyr NMDA"] = {
        "method": "many_to_one",
        "count": 25,
        "weight": scale * 1.0 * 0.004e-3,
        "synapse": "BdendNMDA",
        "threshold": 0,
        "delay": 2,
    }

    # Pyr AMPA
    netParams.connParams["Pyr->Bwb AMPA"] = {
        "method": "many_to_one",
        "count": 100,
        "weight": scale * 0.3 * 1.2e-3,
        "synapse": "somaAMPAf",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["Pyr->OLM AMPA"] = {
        "method": "many_to_one",
        "count": 10,
        "weight": scale * 0.3 * 1.2e-3,
        "synapse": "somaAMPAf",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["Pyr->Pyr AMPA"] = {
        "method": "many_to_one",
        "count": 25,
        "weight": scale * 0.5 * 0.04e-3,
        "synapse": "BdendAMPA",
        "threshold": 0,
        "delay": 2,
    }

    # Basket GABA
    netParams.connParams["Bwb->Bwb GABA"] = {
        "method": "many_to_one",
        "count": 60,
        "weight": scale * 3 * 1.5 * 1.0e-3,
        "synapse": "somaGABAf",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["Bwb->Pyr GABA"] = {
        "method": "many_to_one",
        "count": 50,
        "weight": scale * 2 * 2 * 0.18e-3,
        "synapse": "somaGABAf",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["Bwb->OLM GABA"] = {
        "method": "many_to_one",
        "count": 17,
        "weight": scale * 0.05 * 2 * 2 * 0.18e-3,
        "synapse": "somaGABAf",
        "threshold": 0,
        "delay": 2,
    }

    # OLM GABA
    scale = 1.0
    netParams.connParams["OLM->Pyr GABA"] = {
        "method": "many_to_one",
        "count": 20,
        "weight": scale * 4 * 3 * 6.0e-3,
        "synapse": "Adend2GABAs",
        "threshold": 0,
        "delay": 2,
    }
    netParams.connParams["OLM->Pyr GABA 2"] = {
        "method": "many_to_one",
        "count": 10,
        "weight": scale * 0.08 * 4 * 3 * 6.0e-3,
        "synapse": "Adend2GABAs",
        "threshold": 0,
        "delay": 2,
    }
    """
    """

    # ================================================
    # ================== Stimulus ====================
    # ================================================
    # rate = 100 # Hz
    # size = int(rate * (h.tstop/1000))
    netParams.stimParams["Pyr 1"] = {
        "source": "NetStim",
        "targets": ALL_PYR,
        "seed": 4000,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.05e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaAMPAf",
        },
    }
    netParams.stimParams["Pyr 2"] = {
        "source": "NetStim",
        "targets": ALL_PYR,
        "seed": 4001,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.05e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "Adend3AMPAf",
        },
    }
    netParams.stimParams["Pyr 3"] = {
        "source": "NetStim",
        "targets": ALL_PYR,
        "seed": 4002,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.012e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaGABAf",
        },
    }
    netParams.stimParams["Pyr 4"] = {
        "source": "NetStim",
        "targets": ALL_PYR,
        "seed": 4003,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.012e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "Adend3GABAf",
        },
    }
    netParams.stimParams["Pyr 5"] = {
        "source": "NetStim",
        "targets": ALL_PYR,
        "seed": 4004,
        "stim": {
            "interval": 100,
            "number": (1e3 / 100) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 6.5e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "Adend3NMDA",
        },
    }

    # ===================== Noise to OLM ===================
    netParams.stimParams["OLM 1"] = {
        "source": "NetStim",
        "targets": ALL_OLM,
        "seed": 4005,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.0625e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaAMPAf",
        },
    }
    netParams.stimParams["OLM 2"] = {
        "source": "NetStim",
        "targets": ALL_OLM,
        "seed": 4006,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.2e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaGABAf",
        },
    }

    # ===================== Noise to BWB ===================
    netParams.stimParams["Bwb 1"] = {
        "source": "NetStim",
        "targets": ALL_BWB,
        "seed": 4007,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.02e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaAMPAf",
        },
    }
    netParams.stimParams["Bwb 2"] = {
        "source": "NetStim",
        "targets": ALL_BWB,
        "seed": 4008,
        "stim": {
            "interval": 1,
            "number": (1e3 / 1) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 1,
        },
        "conn": {
            "weight": 0.2e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaGABAf",
        },
    }
    # ===================== Noise from MS -> BWB & OLM ===================
    netParams.stimParams["OLM MS"] = {
        "source": "NetStim",
        "targets": ALL_OLM,
        "seed": 4009,
        "stim": {
            "interval": 150,
            "number": (1e3 / 150.0) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 0,
        },
        "conn": {
            "weight": 1.6e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaGABAss",
        },
    }
    netParams.stimParams["Bwb MS"] = {
        "source": "NetStim",
        "targets": ALL_BWB,
        "seed": 4010,
        "stim": {
            "interval": 150,
            "number": (1e3 / 150.0) * h.tstop,
            "start": h.dt * 2,
            "end": h.tstop,
            "noise": 0,
        },
        "conn": {
            "weight": 1.6e-3,
            "delay": 2 * h.dt,
            "threshold": 0,
            "target": "somaGABAss",
        },
    }
    return netParams


def make_spikes(net, po, syn, w, cellN, comp, ISI, eventN, noise, time_limit):
    np.random.seed(1)
    events = np.random.exponential(ISI, (cellN, eventN)) * noise + np.repeat(
        ISI, cellN * eventN
    ).reshape((cellN, eventN)) * (1 - noise)
    events = np.cumsum(events, axis=1)
    for i, ii in enumerate(events):
        ii = ii[ii <= time_limit]
        for gid in net.populations[po].cellgids:
            net.populations[po].cells[gid].__dict__[syn].Vwt = w
        # po.cell[i].__dict__[syn].append(ii)
        # po.cell[i].__dict__[syn].Vwt = w
    return net, events


def add_syn_noise(net: Network.Network):
    fctr = (h.tstop + h.tstop / 2) / 10_000.0
    net, events = make_spikes(
        net,
        "Pyr",
        "somaAMPAf",
        0.05e-3,
        len(ALL_PYR),
        "soma",
        1,
        math.ceil(10_000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "Pyr",
        "Adend3AMPAf",
        0.05e-3,
        len(ALL_PYR),
        "Adend3",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "Pyr",
        "somaGABAf",
        0.012e-3,
        len(ALL_PYR),
        "soma",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "Pyr",
        "Adend3GABAf",
        0.012e-3,
        len(ALL_PYR),
        "Adend3",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "Pyr",
        "Adend3NMDA",
        6.5e-3,
        len(ALL_PYR),
        "Adend3",
        100,
        math.ceil(100 * fctr),
        1,
        h.tstop,
    )

    net, events = make_spikes(
        net,
        "Bwb",
        "somaAMPAf",
        0.02e-3,
        len(ALL_BWB),
        "soma",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "Bwb",
        "somaGABAf",
        0.2e-3,
        len(ALL_BWB),
        "soma",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "Bwb",
        "somaGABAss",
        1.6e-3,
        len(ALL_BWB),
        "soma",
        150,
        math.ceil(65 * fctr),
        0,
        h.tstop,
    )

    net, events = make_spikes(
        net,
        "OLM",
        "somaAMPAf",
        0.02e-3,
        len(ALL_OLM),
        "soma",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "OLM",
        "somaGABAf",
        0.2e-3,
        len(ALL_OLM),
        "soma",
        1,
        math.ceil(10000 * fctr),
        1,
        h.tstop,
    )
    net, events = make_spikes(
        net,
        "OLM",
        "somaGABAss",
        1.6e-3,
        len(ALL_OLM),
        "soma",
        150,
        math.ceil(65 * fctr),
        0,
        h.tstop,
    )
    return net


def plot_soma_volt(simData: dict):
    plt.figure(figsize=(15, 10))
    idx = 0
    for gid, cell in simData.items():
        gids = (
            random.sample(ALL_PYR, 25)
            + random.sample(ALL_OLM, 25)
            + random.sample(ALL_BWB, 25)
        )
        if cell._gid in gids:
            plt.plot(np.array(cell.sim_time), np.array(cell.soma_v) + 40 * idx)
            idx += 1


def scatter_plot(simData: dict):
    colors = {"Pyr": "blue", "Olm": "red", "Bwb": "green"}

    plt.figure(figsize=(13, 8))
    gids = {"Pyr": range(800), "Bwb": range(800, 1000), "Olm": range(1000, 1200)}
    for k, color in colors.items():
        xs = []
        ys = []
        for gid in gids[k]:
            st = simData[gid].spike_times
            xs.extend(st)
            ys.extend(np.ones_like(st) + gid)
        plt.scatter(xs, ys, color=color, marker=",", s=1, alpha=1.0)
    plt.title("Pyr-blue | OLM-red | Bwb-green")


def print_firing_rate(simData: dict):
    pyr = []
    bwb = []
    olm = []
    for gid, cell in simData.items():
        if cell._gid < 800:
            pyr.append(cell.compute_firing_rate())
        elif 800 <= cell._gid < 1000:
            bwb.append(cell.compute_firing_rate())
        elif 1000 <= cell._gid < 1200:
            olm.append(cell.compute_firing_rate())
    print(f"Pyr :: {np.mean(pyr):.2f} Hz +- {np.std(pyr):.2f} Hz (std)")
    print(f"Bwb :: {np.mean(bwb):.2f} Hz +- {np.std(bwb):.2f} Hz (std)")
    print(f"Olm :: {np.mean(olm):.2f} Hz +- {np.std(olm):.2f} Hz (std)")


def baseline():
    netParams = init_network(
        cell_seed=404, conn_seed=123, stim_seed=456, scale_conn_weight=1.0
    )

    net = Network.Network(
        netParams,
        rng=rng,
    ).create()

    for gid, cell in net.populations["Pyr"].cells.items():
        for sect in cell.all:
            for seg in sect:
                # seg.nacurrent.g *= netParams.nps['cell_mod']['gna']
                pass

    """
    for popname, pop in net.populations.items():
        for gid, cell in pop.cells.items():
            if popname == 'OLM':
                cell.__dict__['somaNMDA'].r = 1
            if popname == 'Bwb':
                cell.__dict__['somaNMDA'].r = 1
            if popname == 'Pyr':
                cell.__dict__['BdendNMDA'].r = 1
                cell.__dict__['Adend3NMDA'].r = 1
    """

    for gid, cell in net.populations["Pyr"].cells.items():
        cell.add_iclamp(section="soma", amp=50e-3, dur=1e9, delay=2 * h.dt)

    for gid, cell in net.populations["OLM"].cells.items():
        cell.add_iclamp(section="soma", amp=-25e-3, dur=1e9, delay=2 * h.dt)

    sim = Simulator.Simulator(net, coreneuron=False, verbose=True)
    simData = sim.run(return_pkl=False)

    save_folder = (
        "/home/Marc/Documents/internship/python_analysis/data/Data02_Baseline/"
    )
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    save_path = os.path.join(save_folder, "baseline.pkl")  # ///Change file name///

    output = {"netParams": netParams, "simData": simData}  # save netParams and simData

    with open(save_path, "wb") as f:
        pickle.dump(output, f)

    print_firing_rate(simData)
    scatter_plot(simData)

    print("DONE")
    return


def createRun(nps_seeds_trials):
    nps, seeds, trial = nps_seeds_trials
    print(f"Epoch:{trial} || {seeds}")

    cell_seed, conn_seed, stim_seed = seeds
    nps["cell_seed"] = seeds[0]
    nps["conn_seed"] = seeds[1]
    nps["stim_seed"] = seeds[2]
    data_path = nps["data_path"]

    netParams = init_network(
        cell_seed=cell_seed, conn_seed=conn_seed, stim_seed=stim_seed
    )
    netParams.nps = nps

    net = Network.Network(
        netParams,
        rng=rng,
    ).create()

    for gid, cell in net.populations["Pyr"].cells.items():
        for sect in cell.all:
            for seg in sect:
                # seg.nacurrent.g *= netParams.nps['cell_mod']['gna']
                seg.nacurrent.g *= 1

    for popname, pop in net.populations.items():
        for gid, cell in pop.cells.items():
            if popname == "OLM":
                cell.__dict__["somaNMDA"].r = 1
            if popname == "Bwb":
                cell.__dict__["somaNMDA"].r = 1
            if popname == "Pyr":
                cell.__dict__["BdendNMDA"].r = 1
                cell.__dict__["Adend3NMDA"].r = 1

    for gid, cell in net.populations["Pyr"].cells.items():
        cell.add_iclamp(amp=50e-3, dur=1e9, delay=2 * h.dt)

    for gid, cell in net.populations["OLM"].cells.items():
        cell.add_iclamp(amp=-25e-3, dur=1e9, delay=2 * h.dt)

    sim = Simulator.Simulator(net, coreneuron=False, verbose=True)
    simData = sim.run(return_pkl=False)

    """
    out = {'netParams': netParams, 'simData': simData}
    file_name = f'{trial:02}'
    with open(f"{data_path}/{file_name}.pkl", 'wb') as f:
        pickle.dump(out, f)
        print(f'Data saved to: {f.name}')
    """

    print_firing_rate(simData)
    scatter_plot(simData)
    return


def run_many(varient: str):
    sodium = varient
    mods = {"NA": 1.0, "NA+": 1.1, "NA-": 0.9}

    data_path = (
        f"/home/Marc/Documents/internship/python_analysis/data/various/{varient}/"
    )
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    nps = {}
    nps["cell_mod"] = {"gna": mods[sodium]}
    nps["data_path"] = data_path
    nps["trials"] = 50
    nps["profile"] = varient
    nps["start_seed"] = global_seed

    n_runs = nps["trials"]
    trials = list(range(0, n_runs))
    seed_gen = np.random.default_rng(global_seed)
    seeds = []
    epochs = []
    for e in range(n_runs):
        cell_seed = 404
        conn_seed = seed_gen.integers(0, 1_000_000, dtype=np.int32)
        stim_seed = seed_gen.integers(0, 1_000_000, dtype=np.int32)
        seeds.append((cell_seed, conn_seed, stim_seed))
        epochs.append(e)

    nps_seeds_trials = list(zip([dict(nps) for _ in range(len(seeds))], seeds, epochs))

    n_processes = min(12, cpu_count())
    with Pool(processes=n_processes) as pool:
        pool.map(createRun, nps_seeds_trials)


def run_varients():
    gs = ["NA", "NA+", "NA-"]
    for g in gs:
        run_many(g)


if __name__ == "__main__":
    # run_varients()
    baseline()


plt.show()
