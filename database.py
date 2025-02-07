import h5py

class Hdf5Client:
    def __init__(self, exchange: str):
        self.hf = h5py.File(name=f"data/{exchange}.h5", mode="a")
        self.hf.flush()  # persist in disk even if we dont close the file

