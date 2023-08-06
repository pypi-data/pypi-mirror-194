
def fit_model(model, train_generator, test_generator):

    history = model.fit(
        train_generator,
        validation_data = test_generator,
        steps_per_epoch = int(train_generator.samples) // int(train_generator.batch_size),
        validation_steps = int(test_generator.samples) // int(test_generator.batch_size),
        epochs=3, 
        verbose=1, 
        workers = 10,
        use_multiprocessing = True,
    ) 
    return history