import pickle
import cloudpickle


PICKLE = 'pickle'
CLOUDPICKLE = 'cloudpickle'
pickling = {
    PICKLE: pickle,
    CLOUDPICKLE: cloudpickle
}


def load_model(file_name, pickling_type=PICKLE):
    if pickling.get(pickling_type):
        with open(file_name, 'rb') as f_in:
            model = pickling[pickling_type].load(f_in)
        return model


def save_model(model, file_name, pickling_type=PICKLE):
    if pickling.get(pickling_type):
        with open(file_name, 'wb') as f_out:
            pickling[pickling_type].dump(model, f_out)
