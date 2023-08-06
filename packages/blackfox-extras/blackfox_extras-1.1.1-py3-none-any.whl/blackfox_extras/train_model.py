from .data_extras import prepare_input_data, prepare_output_data
import tensorflow
from sklearn.model_selection import train_test_split

def train_ann(
    model = None,
    metadata = None,
    input_set = None,
    output_set = None,
    input_validation_set = None,
    output_validation_set = None,
    batch_size = 512,
    epochs = 300,
    verbose = 'auto',
    callbacks = None,
    validation_split = 0.2,
    shuffle = True,
    class_weight = None,
    sample_weight = None,
    initial_epoch = 0,
    steps_per_epoch = None,
    validation_steps = None,
    validation_batch_size = None,
    validation_freq = 1,
    max_queue_size = 10,
    workers = 1,
    use_multiprocessing = False
):

    input_set = prepare_input_data(input_set, metadata)
    output_set = prepare_output_data(output_set, metadata)
    if input_validation_set is None and output_validation_set is None:
        input_set, input_validation_set, output_set, output_validation_set = train_test_split(
            input_set,
            output_set,
            test_size = validation_split,
            shuffle = True,
            random_state = 300,
            stratify = None
        )
    else:
        input_validation_set = prepare_input_data(input_validation_set, metadata)
        output_validation_set = prepare_output_data(output_validation_set, metadata)
    
    # Callbacks
    if callbacks is None:
        early_stopping = tensorflow.keras.callbacks.EarlyStopping(monitor = 'val_loss', restore_best_weights = True, patience = 500)
        csv_logger = tensorflow.keras.callbacks.CSVLogger('logger.csv', separator = ',', append = False) 
        callbacks = [early_stopping, csv_logger]
    
    # Fit
    model.fit(
        input_set,
        output_set,
        validation_data = (input_validation_set, output_validation_set),
        epochs = epochs,
        callbacks = callbacks,
        batch_size = batch_size,
        shuffle = shuffle,
        verbose = verbose,
        class_weight = class_weight,
        sample_weight = sample_weight,
        initial_epoch = initial_epoch,
        steps_per_epoch = steps_per_epoch,
        validation_steps = validation_steps,
        validation_batch_size = validation_batch_size,
        validation_freq = validation_freq,
        max_queue_size = max_queue_size,
        workers = workers,
        use_multiprocessing = use_multiprocessing
    )

    return model