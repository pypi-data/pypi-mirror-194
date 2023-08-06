from .data_extras import prepare_input_data
from .scaler_extras import rescale_output_data
from .encode_data_set import decode_output_data
import tensorflow as tf
import sklearn

def predict_proba(model, metadata, input_data):

    input_data_prepared = prepare_input_data(input_data, metadata)
    
    if isinstance(model, sklearn.ensemble.RandomForestClassifier) and metadata['scaler_config']['output']['feature_range'] is None:
        predicted_data = model.predict_proba(input_data_prepared)
    else:
        predicted_data = model.predict(input_data_prepared)
    # ANN predictions are matrices but RF and XGBOOST predictions are vectors, needs to be reshaped to matrices
    if not isinstance(model, tf.keras.Model):
        # Exclude multiclass case
        if predicted_data.ndim == 1:
            predicted_data = predicted_data.reshape(len(predicted_data), 1)
    
    return predicted_data

def predict(model, metadata, input_data):

    predicted_data = predict_proba(model, metadata, input_data)
    
    predicted_data = rescale_output_data(predicted_data, metadata)

    if 'output_encoding' in metadata:
        if 'metric_threshold' in metadata:
            if metadata['metric_threshold'] is None:
                threshold = 0.5
            else:
                threshold = metadata['metric_threshold']
        predicted_data = decode_output_data(predicted_data, metadata, threshold)

    return predicted_data