
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from Utils import get_labels

def plot_confusion_matrix(generator, y_pred,path_to_save, save = True):
    fig = px.imshow(confusion_matrix(generator.classes, y_pred),
                    text_auto=True,
                    
                    labels = dict(y = 'True label', 
                                  x = 'Predicted label'),
                    x = get_labels(generator),
                    y = get_labels(generator))
    fig.update_layout(

    width = 400, 
    height = 400, 
    title = "Confution Matrix")
    fig.update_xaxes(side = "bottom")
    if save: 
        fig.write_image(path_to_save)

def get_performance(history, path_to_save, save = True):

    plt.figure(figsize=(15, 4))
    ax = plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], 'go', label='training acc')
    plt.plot(history.history['val_accuracy'], 'g-', label='validation acc')
    plt.legend()
    plt.title('Accuracy')
    plt.xlabel('Epocs')
    ax = plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], 'go', label='training loss')
    plt.plot(history.history['val_loss'], 'g-', label='validation loss')
    plt.legend()
    plt.title('Loss')
    plt.xlabel('Epocs')
    if save: 
        plt.savefig(path_to_save)