import random;
from sklearn.manifold import TSNE
from torchvision import datasets, transforms, torch, models;
from torch.hub import load_state_dict_from_url
from tqdm import tqdm;
import numpy as np;
import pickle;
import os;
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class ImageFolderWithPaths(datasets.ImageFolder):
    """Custom dataset that includes image file paths. Extends
    torchvision.datasets.ImageFolder
    """

    # override the __getitem__ method. this is the method that dataloader calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns 
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # the image file path
        path = self.imgs[index][0]
        # make a new tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path
    
def scale_to_01_range(arr):
    """Scales an array to the range [0, 1]."""
    return (arr - arr.min()) / (arr.max() - arr.min())

def compute_plot_coordinates(image, x, y):
    """Computes the plot coordinates for an image based on its t-SNE coordinates."""
    # compute the dimensions of the image
    height, width, _ = image.shape
    image_ratio = width / height

    # set the plot size
    plot_size = 2

    # compute the plot coordinates
    x = (x * plot_size) / image_ratio
    y = y * plot_size
    tl_x = int(x - (width / 2))
    tl_y = int(y - (height / 2))
    br_x = int(x + (width / 2))
    br_y = int(y + (height / 2))

    return tl_x, tl_y, br_x, br_y

class ResNet101(models.ResNet):
    """
    Reimplementing ResNet101 to allow for feature extraction.
    """
    def __init__(self, num_classes=1000, **kwargs):
        # Start with the standard resnet101
        super().__init__(
            block=models.resnet.Bottleneck,
            layers=[3, 4, 23, 3],
            num_classes=num_classes,
            **kwargs
        )
        state_dict = load_state_dict_from_url(
            models.resnet.model_urls['resnet101'],
            progress=True
        )
        self.load_state_dict(state_dict)
 
    # Reimplementing forward pass.
    # Replacing the forward inference defined here 
    # http://tiny.cc/23pmmz
    def _forward_impl(self, x):
        # Standard forward for resnet
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
 
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
 
        # Notice there is no forward pass through the original classifier.
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
 
        return x

# identify the path containing all your images
# if you want them to be labeled by country, you will need to sort them into folders

root_path = 'data';

root = os.path.expanduser(root_path)

# transform the data so they are identical shapes
transform = transforms.Compose([transforms.Resize((255, 255)), transforms.ToTensor()])
dataset = ImageFolderWithPaths(root, transform=transform)

# load the data
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

# initialize model
model = ResNet101()
model.eval()
model.to(device)

# initialize variables to store results
features = None
labels = []
image_paths = []

# run the model
for batch in tqdm(dataloader, desc='Running the model inference'):

    images = batch[0].to('cpu')
    labels += batch[1]
    image_paths += batch[2]

    output = model.forward(images)
    # convert from tensor to numpy array
    current_features = output.detach().numpy()

    if features is not None:
        features = np.concatenate((features, current_features))
    else:
        features = current_features

# return labels too their string interpretations
labels = [dataset.classes[e] for e in labels]

# save the data
np.save('images.npy', images)
np.save('features.npy', features)
with open('labels.pkl', 'wb') as f:
    pickle.dump(labels, f)
with open('image_paths.pkl', 'wb') as f:
    pickle.dump(image_paths, f)

  # the s in t-SNE stands for stochastic (random) 
# let's set a seed for reproducible results
seed = 10
random.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)

# run tsne
n_components = 2
tsne = TSNE(n_components=2)
tsne_result = tsne.fit_transform(features)

# scale and move the coordinates so they fit [0; 1] range
tx = scale_to_01_range(tsne_result[:, 0])
ty = scale_to_01_range(tsne_result[:, 1])

# initialize a matplotlib plot
fig = plt.figure()
ax = fig.add_subplot(111)

colors_per_class = {
    'jp': [255, 0, 0],  # red
    'gb': [0, 0, 255],  # blue
}

# for every class, we'll add a scatter plot separately
for label in colors_per_class:
    # find the samples of the current class in the data
    indices = [i for i, l in enumerate(labels) if l == label]
    # get image paths for the current class
    image_paths_per_label = np.take(image_paths, indices)
    # extract the coordinates of the points of this class only
    current_tx = np.take(tx, indices)
    current_ty = np.take(ty, indices)

    # convert the class color to matplotlib format
    color = np.array(colors_per_class[label], dtype=float) / 255
    # add a scatter plot with the corresponding color and label
    ax.scatter(current_tx, current_ty, c=color, label=label)
    for i in range(len(current_tx)):
        # remove ".png" from the image path and then remove the path before the image name
        ax.annotate(image_paths_per_label[i][:-4][8:], (current_tx[i], current_ty[i]))
# build a legend using the labels we set previously
ax.legend(loc='best')
# finally, show the plot
plt.show()

# Compute the coordinates of the image on the plot
def compute_plot_coordinates(image, x, y, image_centers_area_size, offset):
    """
    Compute the coordinates of the top left and bottom right corner
    of the image on the plot.
    
    :param image: the image
    :param x: the x coordinate of the image center
    :param y: the y coordinate of the image center
    :param image_centers_area_size: the size of the area where the image centers are plotted
    :param offset: the offset of the image center area on the plot
    """
    image_height, image_width, _ = image.shape
 
    # compute the image center coordinates on the plot
    center_x = int(image_centers_area_size * x) + offset
 
    # in matplotlib, the y axis is directed upward
    # to have the same here, we need to mirror the y coordinate
    center_y = int(image_centers_area_size * (1 - y)) + offset
 
    # knowing the image center,
    # compute the coordinates of the top left and bottom right corner
    tl_x = center_x - int(image_width / 2)
    tl_y = center_y - int(image_height / 2)
 
    br_x = tl_x + image_width
    br_y = tl_y + image_height
 
    return tl_x, tl_y, br_x, br_y