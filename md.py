from OpenSMOG import SBM
import os
import sys
import argparse

def main():
    """
    Runs an OpenSMOG simulation with user-defined parameters.

    Args:
        xml_file: Path to the XML file containing the system parameters.
        system_name: Name of the simulation system.
        output_dir: Diretory for output files.
        temperature: Simulation temperature.
        interval: Reporting interval.
    """

    parser = argparse.ArgumentParser(description="Run an OpenSMOG simulation.")
    parser.add_argument("-i", "--xml_file", required=True, help="Path to the XML file containing the system parameters.") 
    parser.add_argument("-n", "--system_name", required=True, help="Name of the simulation system") 
    parser.add_argument("-o", "--output_dir", default="output", help="Directory for output files.")
    parser.add_argument("-t", "--temperature", type=float, default=0.5, help="Simulation temperature.")
    parser.add_argument("-interval", type=int, default=1000, help="Reporting interval.")
    args = parser.parse_args()

    SMOGrun = SBM(
        name=args.system_name, 
        time_step=0.0005, 
        collision_rate=1.0, 
        r_cutoff=1.1, 
        temperature=args.temperature
    )

    # Select a platform and GPU IDs (if needed)
    # We will use opencl.  If you want to perform CPU-only calculations, set platform to 'CPU'.
    SMOGrun.setup_openmm(platform='cuda', GPUindex='default')

    # Decide where to save your data
    SMOGrun.saveFolder(f"./{args.output_dir}")

    # You may optionally set some input file names to variables
    SMOG_grofile = '../prep1/CA_gau.gro'
    SMOG_topfile = '../prep1/CA_gau.top'

    # Load your force field data
    SMOGrun.loadSystem(Grofile=SMOG_grofile, Topfile=SMOG_topfile, Xmlfile=args.xml_file)

    # Create the context, and prepare the simulation to run
    SMOGrun.createSimulation()

    # Perform L-BFGS energy minimization
    SMOGrun.minimize(tolerance=1)

    # Decide how frequently to save data
    SMOGrun.createReporters(trajectory=True, 
                            trajectoryFormat='dcd',
                            energies=True, 
                            energy_components=True, 
                            logFileName=f"{args.system_name}.log", 
                            interval=args.interval, 
                            checkpoint=True, 
                            checkpointName=f"{args.system_name}.chk", 
                            checkpointInterval=1000000)

    # Launch the simulation
    SMOGrun.run(nsteps=10**7, report=True, interval=args.interval)

if __name__ == "__main__":
    main()
