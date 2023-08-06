from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, InputLayer
from Utils import get_labels

def load_data(directory, lenght, height):
    data = keras.preprocessing.image.ImageDataGenerator(
    rescale= 1/255, 
    validation_split = 0.2
    )
    train_generator = data.flow_from_directory(

        directory = directory,
        batch_size = 20,
        target_size = (height, lenght), # Image dimentions 
        shuffle=True,
        color_mode = 'rgb',
        class_mode = 'categorical', 
        subset = 'training'
    )

    test_generator = data.flow_from_directory(

        directory = directory,
        batch_size = 20,
        target_size = (height, lenght), # Image dimentions 
        color_mode = 'rgb',
        shuffle=False,
        class_mode = 'categorical', 
        subset = 'validation'
    )
    return train_generator, test_generator

def build_and_compile_cnn_model(input_shape,n_classes, show_sum = True):

    # Create model
    model = Sequential()
    # Input layer
    model.add(InputLayer(input_shape = input_shape)) 
    # Create hidden layers
    model.add(Conv2D(
        filters = 32, 
        activation="relu", 
        kernel_size = (3,3), 
        name = 'first'
        ))


    model.add(Conv2D(
        filters = 32, 
        activation="relu", 
        kernel_size = (3, 3),
        name = 'second'
        ))
    model.add(MaxPooling2D(pool_size=(2, 2), 
                        strides=None, 
                        padding="valid"))


    model.add(Conv2D(
        filters = 64, 
        activation="relu", 
        kernel_size = (3, 3), 
            name = 'third'
        ))
    model.add(MaxPooling2D(pool_size=(2, 2), 
                        strides=None, 
                        padding="valid"))


    model.add(Conv2D(
        filters = 64, 
        activation="relu", 
        kernel_size = (3, 3), 
            name = 'fourth'
        ))
    model.add(MaxPooling2D(pool_size=(2, 2), 
                        strides=None, 
                        padding="valid"))

    model.add(Conv2D(
        filters = 128, 
        activation="relu", 
        kernel_size = (3, 3), 
        name='visualized_layer'
        ))

    model.add(Flatten())
    model.add(Dense(n_classes, activation = 'softmax'))

    # Compile model
    model.compile(
        loss = 'categorical_crossentropy', 
        optimizer = "adam",               
        metrics = ['accuracy']
        )


    if show_sum:
        model.summary()
    
    return model





if __name__ == "__main__":
    pass