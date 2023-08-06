#!/usr/bin/env python

import sys
#import time
#import abipy.data as abidata

from abipy.core.structure import Structure
from abipy.htc.base_models import MongoConnector, mng_insert_models
from abipy.htc.structure_models import StructureData
from abipy.htc.pseudos_models import PseudoSpecs
from abipy.htc.gs_flow_models import EbandsFlowModelWithParams
from abipy.htc.dfpt_flow_models import PhononFlowModelWithParams, PhononFlowModelWithInput
#from abipy.htc.worker import AbipyWorker

# Explicit options.
#mng_connector = MongoConnector(host="mongo.pcpm.ucl.ac.be",
#                                 db_name="abipy_GM",
#                                 collection_name="ebands",
#                                 username="gmatteo",
#                                 password="Ts5qb/UtB.22",
#                                 )

# Take options from ~/.abinit/abipy/config.yml configuration file.
mng_connector = MongoConnector.from_abipy_config(collection_name="ebands")

mng_connector = MongoConnector.for_localhost(collection_name="ebands")
print(mng_connector)

# Pseudopotential specifications.
# Note that we need to specify the table_name besides the repo name

pseudos_specs = PseudoSpecs.from_repo_table_name("ONCVPSP-PBE-SR-PDv0.4", "standard")
#pseudos_specs = PseudoSpecs.from_repo_table_name("ONCVPSP-PBE-FR-PDv0.4", "standard")


def build_collection(drop=False):
    """
    Fill a MongoDB collection with FlowModel instances defining the kind of
    calculation we want to perform and the schema used to store the output results.
    This step is mandatory before starting the AbipyWorker.
    """
    if drop:
        print(f"Building new collection {collection.full_name}")
        mng_connector.drop_collection(ask_for_confirmation=False)
    else:
        print(f"Adding documents to collection {collection.full_name}")

    # Generate list of structures.
    quick = True
    #quick = False
    if quick:
        from abipy.data.ucells import structure_from_ucell
        structures = [structure_from_ucell(name) for name in ("Si", "Si-shifted")]

    else:
        structures = [Structure.from_mpid(mpid) for mpid in (
            #"mp-149",   # Si2
            #"mp-2172",  # AlAs F-43m
            #"mp-2534",  # GaAs F-43m
            "mp-32",     # Ge-dia
            "mp-149",    # Si-dia
            "mp-2534",   # GaAs-zb
            "mp-406",    # CdTe-zb
            "mp-2691",   # CdSe-zb
            "mp-2172",   # AlAs-zb
            "mp-2176",   # ZnTe-zb
            "mp-8062",   # SiC-zb
            "mp-2469",   # CdS-zb
            "mp-1550",   # AlP-zb
            "mp-1190",   # ZnSe-zb
            "mp-2657",   # TiO$_2$-t
            "mp-5229",   # SrTiO$_3$-sc
            "mp-804",    # GaN-w
            "mp-830",    # GaN-zb
            "mp-2133",   # ZnO-w
            "mp-856",    # SnO$_2$-t
            "mp-10695",  # ZnS-zb
            "mp-1342",   # BaO-rs
            "mp-2472",   # SrO-rs
            "mp-66",     # C-dia
            "mp-661",    # AlN-w
            "mp-1639",   # BN-zb
            "mp-2605",   # CaO-rs
            "mp-1960",   # Li$_2$O
            "mp-1265",   # MgO-rs
            "mp-6947",   # SiO$_2$-t
            "mp-2542",   # BeO-w
            "mp-1138",   # LiF-rs
        )]

    # Get pseudopotential tables with hints.
    accuracy = "normal"
    #pseudos = pseudos_specs.get_pseudos()

    models = []
    for i, structure in enumerate(structures):
        in_structure_data = StructureData.from_structure(structure)

        if i == 0: EbandsFlowModelWithParams.init_collection(collection)
        model = EbandsFlowModelWithParams(in_structure_data=in_structure_data,
                                          pseudos_specs=pseudos_specs,
                                          #kppa=300,
                                          kppa=2000,
                                          with_gsr=True,
                                          with_out=True,
                                          with_log=True,
                                          )

        #if i == 0: RelaxFlowModel.init_collection(collection)
        #model = RelaxFlowModel(in_structure_data=in_structure_data, pseudos_specs=pseudos_specs,
        #                        kppa=300)

        #if i == 0: PhononFlowModelWithParams.init_collection(collection)
        #scf_input = make_scf_input(structure, pseudos, accuracy)
        #model = PhononFlowModelWithInput(in_structure_data=in_structure_data,
        #                                 pseudos_specs=pseudos_specs,
        #                                 scf_input=scf_input,
        #                                 with_becs=False,
        #                                 with_quad=False)

        #sys.exit(1)
        #print(model)
        models.append(model)

    mng_insert_models(models, collection, verbose=1)
    #mng_connector.insert_models(models, collection)


def aggregate():
    collection = mng_connector.get_collection()
    df = EbandsFlowModelWithParams.mng_aggregate_in_structures(collection)
    from abipy.abilab import print_dataframe
    print_dataframe(df)


def make_scf_input(structure, pseudos, accuracy, paral_kgb=0):
    """
    This function constructs the input file for the GS calculation:
    """
    # Crystalline AlAs: computation of the second derivative of the total energy
    from abipy import abilab
    #structure = abidata.structure_from_ucell("AlAs")
    gs_inp = abilab.AbinitInput(structure, pseudos=pseudos)

    #num_valence_electrons = gs_inp.structure.num_valence_electrons(pseudos)
    num_valence_electrons = gs_inp.num_valence_electrons
    nsppol = 2
    nband = num_valence_electrons // nsppol + 4
    nband += nband % 2

    gs_inp.set_vars(
        nband=nband,
        #nband=4,
        #ecut=2.0,
        ngkpt=[4, 4, 4],
        #nshiftk=4,
        #shiftk=[0.0, 0.0, 0.5,   # This gives the usual fcc Monkhorst-Pack grid
        #        0.0, 0.5, 0.0,
        #        0.5, 0.0, 0.0,
        #        0.5, 0.5, 0.5],
        shiftk=[0, 0, 0],
        paral_kgb=paral_kgb,
        tolvrs=1.0e-8,
        diemac=9.0,
    )

    gs_inp.set_cutoffs_for_accuracy(accuracy)
    #gs_inp.set_auto_scf_nband(nsppol=1, nspinor=1, nspden=1, occopt, tsmear)
    return gs_inp


if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except IndexError:
        print("Available commands: `build`, `add`")
        sys.exit(1)

    if command == "build":
        build_collection(drop=True)
    elif command == "add":
        build_collection(drop=False)
    elif command == "aggregate":
        aggregate()
    else:
        raise ValueError(f"Invalid command: {command}")
