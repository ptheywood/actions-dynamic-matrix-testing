# actions-dynamic-matrix-testing

Repo for testing/prototyping dynamic matrix CI

This is (currently) being used as a prototype for refactoring CI on a CUDA/C++ library with python bindings, built using CMake.

- Linting must be performed on push/pr/manual.
    - A single run is fine (maybe one per OS) but CMake and a compiler toolchain are required.
- Documentation must be built on push/pr/manual
    - A single run is fine (maybe one per OS) but CMake and a compiler toolchain are required.
- "Regular" CI which builds all targets in the CMake project on push / pull request
    - Multiple OS
    - Containerised builds (Manylinux)
    - Multiple CUDA compilers and cuda architectures
    - Multiple host compilers
    - Multiple python versions
    - Multiple build configurations (Release, debug, seatbelts, vis, MPI)
    - Optional compilation targets (test suite compilation is very time consuming on windows)
    - Tests are not executed, as a NVIDIA GPU is required.
    - Multiple CMake Versions
        - Compilation not strictly required
- Release CI on matching tag push
    - Run thorough build testing
    - Build (python) binary artifacts
    - Create a draft github release?
- Post-Release CI
    - On Release push, invoke CI in other repos.

A full "ideal" thorough build matrix would be 100s of jobs:

- 2 windows images (`windows-2022`, `windows-2025`) with 1 host compiler `VS 2022`
- 3 linux images (`ubuntu-22.04`, `ubuntu-24.04`, `manylinux_2_28`) with up to 5 (ideally 10+) (GCC 9+, Clang 12+ in the future?)
- Multiple MPI versions on linux (~5)
- Up to ~16 (11.2-12.9) CUDA versions, 2 required, 4 as a sensible compromise.
- 5 currently supported python versions (3.9-3.13)
- 3 build configurations (Release, Debug, Seatbelts)
- With and without visualisation
- Cmake >= 3.18. 17? 3 for minimal coverage. (3.18, 4.0, latest)

This would be ~`1240320` combinations in a dense matrix (give or take a bit)
<!-- (2 + (3 * 10 * 5)) * 16 * 5 * 3 * 2 * 17 -->

This is far too many jobs, so much smaller subset(s) should be used and should be context dependent. A change which only modifies markdown files does not need to test every possible host compiler combination for instance.

- Depending on what was changed, some jobs could be skipped, or a smaller matrix used.
- Depending on what triggered the job, some jobs could be skipped, or a smaller matrix used.

Github events which trigger CI should include:

- Pushes to `main`/`master`
- Pushes and/or pull_requests.
    - push and pull_request events test different states of the repo but both can be triggered for the same commit (if it belongs to a PR), and although this checks both sides of the potential merge, it would usually be redundant work.
- Pushes of tags which start with `v[0-9]`
- Release creation
- workflow_dispatch

There should be a way to mark pull requests as requiring thorough CI, which registers as a (non compulsory) check.

Composite actions and reusable workflows could be leveraged, as the current setup with different workflows has a lot of common elements, and/or combined with the dynamic matrix to select an appropriate CI matrix.
Investigation is needed to see if composite actions / reusable workflows can be made to play nicely with container and non-container workflows.

The dynamic matrix could? include:

- `single` - a single configuration of os/compilers/options
- `minimal`- the minimal configuration from the ideal matrix, to cover min/max versions of os/compiler set
- `regular` - minimal set with some extras
- `thorough` - a thorough matrix, not fully dense but the largest matrix to use. Possiblyt excluding  the "regular" matrix to avoid duplicates?
- `wheels` - the matrix to use for producing ci wheels?

This could be an explicit list in a yaml file, or it might be scripting generation of the dynamic matrix so version dependencies are simpler to change?


## Matrix members

The following are all of the matrix elements required for jobs:

- OS/image
    - The runs-on or container value. 
- CUDA
    - The CUDA version. 12.0-13.x Currently 10 versions
- cuda_arch
    - The target compute capability, which is tied to the cuda version (but could be multiple options per CUDA)
- Host compiler
    - multiple os-specific compiler versions, with the supported 
- MPI?
    - Mpi under ubuntu is also image specific.

- Python
    - The python version, generally multiplicative.
- Configuration
    - The cmake build config. Release, RelWithDebInfo, MinSizeRel, Debug
- cmake
    - The cmake version, usually only 1 value.
- Visualistaion
    - If vis is wanted or not. ON or OFF. Sometimes always want both, sometimes just one.
- ...


## Job classifications / how many matrices?

- Minimal
    - Single job, single platform, might still need full version specification. I.e. docs, linting. Multiple platforms might be useful but not required
- Small
    - Job per OS/platform. Oldest supported compilers only.
- Medium
    - 'regular' CI. Min/Max compilers/tools.
- Large / Thorough
    - Lots of versions
- Wheels
    - Configurations to produce wheels.


This will still include a lot of duplication. Might be worth having a script instead which produces the requested matrix. I.e. so that the source of which cuda versions etc is only included once (as an explicit list, with a function extracting the min / min per major or min/max per major when required? ) Some complexity with host compilers then though