virtualenv -p python3.11 venv
source venv/bin/activate
pip install "pip==23.2.1" "setuptools==68.2.2"
pip install  --no-cache-dir  --force-reinstall --upgrade torch
pip install --no-cache-dir "h5py>=3.7.0" "netcdf4>=1.6.3" "ruamel.yaml>=0.17.22" "scikit-learn>=1.0.2" "cftime>=1.6.2" "einops>=0.7.0" "pyspng>=0.1.0"
pip install --no-cache-dir "hydra-core>=1.2.0" "termcolor>=2.1.1" "wandb>=0.13.7" "mlflow>=2.1.1" "pydantic>=1.10.2" "imageio>=2.28.1" "moviepy>=1.0.3" "tqdm>=4.60.0" "gcsfs==2024.2.0"
pip install --no-cache-dir --no-deps dgl==2.0.0 -f https://data.dgl.ai/wheels/cu121/repo.html
pip install --no-cache-dir "vtk>=9.2.6"
pip install --no-cache-dir "pyvista>=0.40.1"
pip install --no-cache-dir "onnx>=1.14.0"
pip install --no-cache-dir nvidia-modulus