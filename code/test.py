from keras.models import model_from_json
from keras.optimizers import SGD

DATADIR = '/home/geena/projects/which_animal/data/selected/nparrays/'
FOLDER={'cat':'cat/dur1_win50_hop25_mfcc13/','dog':'dog/dur1_win50_hop25_mfcc13/','bird':'bird/dur1_win50_hop25_mfcc13/'}
X_train, X_test, y_train, y_test = load_data(0.2)
y_test = np.argmax(y_test,axis=1)

model = model_from_json(js)
model.load_weights("doublelayer_weights.h5py")
sgd = SGD(lr=0.0001, decay=0.00001, momentum=0.9)
model.compile(loss='categorical_crossentropy', optimizer='sgd')

y_pred=model.predict_classes(X_test)
print "Multipayer 2d-conv net Result"
print classification_report(y_test, y_pred)

# printing out weights and output dimensions from layers
for layer in model3.layers:
    print layer.get_config()['name']
    print layer.output_shape
    w =  layer.get_weights()
    if len(w)>0:
        print "weights"
        print 'W', w[0].shape
        print 'bias', w[1].shape

# intermediate layers visualization
## run three_animals.py

from keras import backend as K
import pylab as pl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy.ma as ma

def nice_imshow(ax, data, vmin=None, vmax=None, cmap=None):
    """Wrapper around pl.imshow"""
    if cmap is None:
        cmap = cm.jet
    if vmin is None:
        vmin = data.min()
    if vmax is None:
        vmax = data.max()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    im = ax.imshow(data, vmin=vmin, vmax=vmax, interpolation='nearest', cmap=cmap)
    pl.colorbar(im, cax=cax)

def make_mosaic(imgs, nrows, ncols, border=1):
    """
    Given a set of images with all the same shape, makes a
    mosaic with nrows and ncols
    """
    nimgs = imgs.shape[0]
    imshape = imgs.shape[1:]

    mosaic = ma.masked_all((nrows * imshape[0] + (nrows - 1) * border,
                            ncols * imshape[1] + (ncols - 1) * border),
                            dtype=np.float32)

    paddedh = imshape[0] + border
    paddedw = imshape[1] + border
    for i in xrange(nimgs):
        row = int(np.floor(i / ncols))
        col = i % ncols

        mosaic[row * paddedh:row * paddedh + imshape[0],
               col * paddedw:col * paddedw + imshape[1]] = imgs[i]
    return mosaic

inputs = [K.learning_phase()] + model3.inputs
#first conv
convout1 = model3.layers[1]
_convout1_f = K.function(inputs, [convout1.output])
out = _convout1_f([0] + [X_test]) ## out[0].shape -> (600,64,36,36)

nice_imshow(pl.gca(), make_mosaic(out[0][0], 8, 8), cmap=cm.binary)
pl.show()
#second conv
convout2 = model3.layers[3]
_convout_f = K.function(inputs, [convout2.output])
out = _convout_f([0] + [X_test]) ## out[0].shape -> (600,64,36,36)

nice_imshow(pl.gca(), make_mosaic(out[0][0], 8, 8), cmap=cm.binary)
pl.show()

def show_layer(layer_ind, input_ind=0, nrow=None, ncol=None):
    layer = model3.layers[layer_ind]
    print layer.name
    _out_f = K.function(inputs, [layer.output])
    out = _out_f([0] + [X_test]) ## out[0].shape -> (600,64,36,36)
    if (nrow == None)&(ncol == None):
        nrow = int(np.sqrt(layer.output_shape[1]))+1
        ncol = nrow
    nice_imshow(pl.gca(), make_mosaic(out[0][input_ind], nrow, ncol), cmap=cm.binary)
    pl.show()
#e.g. show_layer(1,nrow=8,ncol=8)

#showing the input image
nice_imshow(pl.gca(),make_mosaic(X_test[0],1,1), cmap=cm.binary)
