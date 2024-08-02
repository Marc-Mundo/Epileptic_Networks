if __name__ == "__main__":
    import sys
    import os
    import string

    original_folder_path = "/home/Marc/Documents/internship/models/Sanjay_model"  # mosinit.py is the original file that runs the baseline simulation, did not test yet
    sys.path.append(original_folder_path)

    from neuron import *

    h(
        "strdef simname, allfiles, simfiles, output_file, datestr, uname, osname, comment"
    )
    h.simname = simname = "mtlhpc"
    h.allfiles = allfiles = "geom.hoc pyinit.py geom.py network.py params.py run.py"
    h.simfiles = simfiles = "pyinit.py geom.py network.py params.py run.py"
    h("runnum=1")
    runnum = 1.0
    h.datestr = datestr = "11may20"
    h.output_file = output_file = "data/11may20.05"
    h.uname = uname = "x86_64"
    h.osname = osname = "linux"
    h("templates_loaded=0")
    templates_loaded = 0
    h("xwindows=1.0")
    xwindows = 1.0

    h.xopen("nrnoc.hoc")
    h.xopen("init.hoc")

    from pyinit import *
    from geom import *
    from networkmsj import *
    from params import *
    from run import *

    print("======================= hello ================")
    print(net)
    print("======================= bye ==================")

    # setup washin,washout
    """
    import run as Run
    Run.olmWash =  [0, 1]
    Run.basWash =  [1, 1]
    Run.pyrWashA = [1, 1]
    Run.pyrWashB = [1, 1]
    Run.washinT  = 1e3
    Run.washoutT = 2e3
    Run.fiwash = h.FInitializeHandler(1,Run.setwash)
    """

    # try:
    #     fp = open("./rseed.txt", "r")
    #     ls = fp.readlines()
    #     ISEED = int(ls[0])
    #     WSEED = int(ls[1])
    #     MSG = 1.0
    #     if len(ls) > 2:
    #         MSG = float(ls[2])
    #     fp.close()
    #     # create the network
    #     net = Network(
    #         noise=True,
    #         connections=True,
    #         DoMakeNoise=True,
    #         iseed=ISEED,
    #         UseNetStim=True,
    #         wseed=WSEED,
    #         scale=1.0,
    #         MSGain=MSG,
    #     )
    #     print(
    #         "set network from rseed.txt : iseed=",
    #         ISEED,
    #         ", WSEED=",
    #         WSEED,
    #         ", MSG = ",
    #         MSG,
    #     )
    # except:
    #     net = Network()
    #     print("set network from default constructor")

    # # setup some variables in hoc
    # def sethocix():
    #     h("PYRt=0")
    #     h("BASKETt=1")
    #     h("OLMt=2")
    #     h("PSRt=3")
    #     h('CTYP.o(PYRt).s="PYRt"')
    #     h('CTYP.o(BASKETt).s="BASKETt"')
    #     h('CTYP.o(OLMt).s="OLMt"')
    #     h('CTYP.o(PSRt).s="PSRt"')
    #     h("ix[PYRt]=0")
    #     h("ixe[PYRt]=799")
    #     h("ix[BASKETt]=800")
    #     h("ixe[BASKETt]=999")
    #     h("ix[OLMt]=1000")
    #     h("ixe[OLMt]=1199")
    #     h("ix[PSRt]=1200")
    #     h("ixe[PSRt]=1200")
    #     h("numc[PYRt]=800")
    #     h("numc[BASKETt]=200")
    #     h("numc[OLMt]=200")
    #     h("numc[PSRt]=1")

    # sethocix()

    h.tstop = 5e3
    h.run()
    net.rasterplot()
    net.calc_lfp()
    net.pravgrates()
    myg = h.Graph()
    net.vlfp.plot(myg, h.dt)
    myg.exec_menu("View = plot")
    myg.exec_menu("New Axis")

    # specifiy the path where to save the network
    data_folder = (
        "/home/Marc/Documents/internship/python_analysis/data/Data01_Baseline_Sanjay/"
    )
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    pickle_file_path = os.path.join(
        data_folder,
        "ka_g_200_pops.pkl",  # down or up based on percentage change
    )  # change the name of population file if needed, based on the changes made in the simulation

    # save the network
    with open(pickle_file_path, "wb") as f:
        pickle.dump(net.cells, f)

        # specifiy the path where to save the text file
        text_file_path = os.path.join(
            data_folder, "changes_8.txt"
        )  # change the name of the file if needed

        # write the changes to the text file
        with open(text_file_path, "w") as f:
            f.write("List of changes made in the simulation:\n")
            f.write(
                "- Potassium conductance increase by 200 percent in pyr cells in geom.py\n"
            )
            # Add more changes as needed
            # f.write("- Change 2\n")
            # f.write("- Change 3\n")

# print(state_dict)
print("done")
