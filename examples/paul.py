
from ansys.sherlock.core.launcher import connect_grpc_channel
from ansys.sherlock.core.lifecycle import Lifecycle
from ansys.sherlock.core.project import Project

# Name of the project in Sherlock
projectName = "pySherlockTest"
odbArchivePath = "C:/Users/pwalters/Source/Sherlock\dist/tutorial/ODB++ Tutorial.tgz"

sherlock = connect_grpc_channel()

try:
    sherlock.project.delete_project(projectName)
except Exception:
    pass

process_layer_thickness = True
include_other_layers = False
process_cutout_file = False
guess_part_properties = True

sherlock.project.import_odb_archive(
    odbArchivePath,
    process_layer_thickness,
    include_other_layers,
    process_cutout_file,
    guess_part_properties,
    project=projectName,
)

sherlock.lifecycle.create_life_phase(
    projectName,
    "Example",
    1.5,
    "year",
    4.0,
    "COUNT",
)
sherlock.lifecycle.add_thermal_event(
    projectName,
    "Example",
    "Event1",
    4.0,
    "PER YEAR",
    "OPERATING",
)
sherlock.lifecycle.add_thermal_event(
    projectName,
    "Example",
    "Event2",
    4.0,
    "PER YEAR",
    "OPERATING",
)

sherlock.lifecycle.add_thermal_profiles(
    projectName,
    [(
        "Example",
        "Event1",
        "Profile1",
        "sec",
        "F",
        [
            ("Steady1", "HOLD", 40, 40),
            ("Steady", "HOLD", 20, 20),
            ("Back", "RAMP", 20, 40),
        ],
    )]
)

sherlock.lifecycle.add_random_vibe_event(
    projectName,
    "Example",
    "Random Event 1",
    1.5, "sec",
    4.0, "PER MIN",
    "45,45",
    "Uniaxial",
    "2,4,5",
)

sherlock.lifecycle.add_random_vibe_profiles(
    projectName,
    [(
        "Example",
        "Random Event 1",
        "Profile1",
        "HZ",
        "G2/Hz",
        [(4, 8), (5, 50)],
    )]
)

sherlock.lifecycle.add_harmonic_event(
        projectName,
        "Example",
        "Harmonic Event 1",
        1.5, "sec",
        4.0, "PER MIN",
        5,
        "45,45",
        "Uniaxial",
        "2,4,5",
    )

sherlock.lifecycle.add_harmonic_vibe_profiles(
    projectName,
    [(
        "Example",
        "Harmonic Event 1",
        "Profile1",
        "HZ",
        "G",
        [
            (10, 1),
            (1000, 1),
        ],
        "",
    )]
)

sherlock.lifecycle.add_harmonic_event(
        projectName,
        "Example",
        "Harmonic Event 2",
        1.5, "sec",
        4.0, "PER MIN",
        5,
        "45,45",
        "Uniaxial",
        "2,4,5",
    )

sherlock.lifecycle.add_harmonic_vibe_profiles(
    projectName,
    [(
        "Example",
        "Harmonic Event 2",
        "Profile1",
        "HZ",
        "G",
        [
            (10, 1),
            (1000, 1),
        ],
        "",
    )]
)

sherlock.lifecycle.add_shock_event(
    projectName,
    "Example",
    "Shock Event 1",
    1.5,
    "sec",
    4.0,
    "PER MIN",
    "45,45",
    "2,4,5",
)

sherlock.lifecycle.add_shock_profiles(
    projectName,
    [(
        "Example",
        "Shock Event 1",
        "Profile1",
        10.0, "ms",
        0.1, "ms",
        "G",
        "HZ",
        [("HalfSine", 100.0, 100.0, 0)],  ## TODO MAKE THESE MORE LIFE LIKE
    )]
)